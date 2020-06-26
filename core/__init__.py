#!/usr/bin/python
# -*- coding: UTF-8 -*-
'EvrSim Core;'
# system libs;
import sys
import os
import re
import shutil
# Terminal needed variable;
import mod

class EvrSimCore(object):
    ''' EvrSim Core class.

        Communicate with memory and files;'''
    def __init__(self):
        global ESC
        ESC=self
        # Core global var;
        self.CORE_STAUS='READY'     # ['READY','BUSY','STOP','STEP']
        self.SIM_NAME=''
        self.SIM_FD=None
        self.MOD_LIST=[]
        self.USER_SETTING={}

        # User changeable setting;
        self.SIM_REALTIME=True
        self.SIM_RECORD=False
        self.SIM_QUEUE_LEN=1
        self.ACP_DEPTH=20
        self.TIME_STEP=0.1
        self.MODEL_DISABLE=[]

        # Maps and models;
        self.ARO_MAP=[]
        self.ARO_QUEUE=[]
        self.ARO_MAP_NAME=''
        self.ARO_MAP_LIST=[]
        self.AROID_MAX=0

        self.ACP_MAP={}     # {'modName.modelName':[acplist...]} | {'simInModelName':[...]}
        self.ACPID_MAX={}

        return

    def bug(self,bugstr,report=True):
        'Lv0: Report bug str;'
        if report: print(bugstr)
        return bugstr

# Sim relavant;
    def newSim(self,simname):
        'Lv1: Create new sim by copying _Template dir without opening;'
        file_list=os.listdir('sim/')
        for f in file_list:
            if simname==f: return self.bug('E: Sim existed.')
        tar_path='sim/'+simname+'/'
        src_path='sim/_Template/'
        shutil.copytree(src_path,tar_path)
        return

    def delSim(self,simname):
        'Lv1: ;'
        if self.SIM_FD is not None: return self.bug('E: Sim opened.')
        if simname in os.listdir('sim/'):
            shutil.rmtree('sim/'+simname)
        else: return self.bug('E: Sim not found.')
        return

    def openSim(self,simname):
        'Lv2: Open sim, and load mod and setting;'
        self.__init__()
        if self.SIM_FD is not None: return self.bug('E: Sim already opened.')

        self.SIM_NAME=simname
        if simname in os.listdir('sim/'):
            shutil.copy('sim/'+simname+'/sim.py','sim/'+simname+'/_sim.py')
            self.SIM_FD=open('sim/'+simname+'/_sim.py','r+')
        else: return self.bug('E: Sim not found.')

        # Read sim index;
        simtxt=self.SIM_FD.read()
        _locals=dict()
        exec(simtxt,globals(),_locals)

        # Setting;
        self.setSim(_locals['USER_SETTING'])

        # Mod;
        self.loadMod(_locals['MOD_INDEX'])
        # Map;
        self.ARO_MAP_LIST=_locals['MAP_INDEX']
        self.ARO_MAP_NAME=self.ARO_MAP_LIST[0]
        self.loadMapFile(self.ARO_MAP_LIST[0])
        # Models;
        for model in _locals['MODEL_INDEX']:
            self.loadModelFile((self.SIM_NAME,model))
        return

    def closeSim(self,save=False):
        'Lv2: Close current sim and load default setting;'
        if self.SIM_FD is None: return self.bug('E: Sim not opened.')

        if save:self.saveSim()

        self.SIM_FD.close()
        os.remove('sim/'+self.SIM_NAME+'/_sim.py')

        self.__init__()
        return

    def setSim(self,setdict={},usercall=True):
        ''' Lv1: Load setting.

            Wouldnt change which in USER_SETTING.

            Empty setdict to reset all to default;'''
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        if setdict=={}:
            'todo:load dafault;'
        else:
            for k,v in setdict.items():
                if k not in self.USER_SETTING or usercall:
                    self.__dict__[k]=v
                    if usercall:self.USER_SETTING[k]=v
        return

    def saveSim(self):
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        self.updateModelFile()
        self.updateMapFile()

        simtxt='SIM_NAME="'+self.SIM_NAME+'"\n'
        simtxt+='USER_SETTING='+self.USER_SETTING.__str__()+'\n'
        simtxt+='MOD_INDEX='+self.MOD_LIST.__str__()+'\n'
        simtxt+='AROCLASS_INDEX=[]\n'
        simtxt+='ACPCLASS_INDEX=[]\n'
        simtxt+='TOOL_INDEX=[]\n'
        simtxt+='MAP_INDEX='+self.ARO_MAP_LIST.__str__()+'\n'
        model_index=[]
        for model in self.ACP_MAP.keys():
            if model[0]==self.SIM_NAME:
                model_index.append(model[1])
        simtxt+='MODEL_INDEX='+model_index.__str__()+'\n'
        simtxt+='COM_INDEX=["com"]\n'
        self.SIM_FD.seek(0,0)
        self.SIM_FD.truncate()
        self.SIM_FD.write(simtxt)
        self.SIM_FD.flush()
        shutil.copy('sim/'+self.SIM_NAME+'/_sim.py','sim/'+self.SIM_NAME+'/sim.py')

        return

    def comSim(self):
        'todo'
        ESC.ARO_MAP=[]
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        self.SIM_FD.seek(0,0)
        line=self.SIM_FD.readline()
        while line!='# START\n':
            line=self.SIM_FD.readline()
        while line!='# END\n':
            try:exec(line)
            except BaseException as e:print('Ex:',e)
            line=self.SIM_FD.readline()
        self.SIM_FD.seek(0,0)
        return

    def runSim(self,itorlist=['time']):
        'Lv1: Run Sim with iterators, time default;'
        if self.SIM_FD is None: return self.bug('E: Sim not opened.')
        if self.CORE_STAUS=='BUSY':return self.bug('E: Core busy.')
        self.CORE_STAUS='BUSY'

        # Collect providers and iterators;
        pvdrs=dict()
        itors=dict()
        for model,acplist in self.ACP_MAP.items():
            if model in self.MODEL_DISABLE:continue
            for acp in acplist:
                if isinstance(acp,mod.AroCore.AcpIterator) and acp.item in itorlist:
                    if model not in itors and model not in self.MODEL_DISABLE:
                        itors[model]=list()
                    if acp not in itors[model]:
                        # All models use the same iterators;
                        itors[model].append(acp)
                elif isinstance(acp,mod.AroCore.AcpProvider) and model not in self.MODEL_DISABLE:
                    if model not in pvdrs:
                        pvdrs[model]=list()
                    pvdrs[model].append(acp)

        # Snapshot preparing;
        self.ARO_QUEUE.append(list(self.ARO_MAP))
        if len(self.ARO_QUEUE)>self.SIM_QUEUE_LEN:
            self.ARO_QUEUE=self.ARO_QUEUE[1:]

        if len(itors)==0:
            # Static;
            self.travesalPvdrs(pvdrs)
            'todo: convergence check;'
            self.CORE_STAUS='STOP'
        elif len(itors)==1:
            # Single dimension;
            itor=list(itors.values())[0][0]
            if self.SIM_REALTIME:
                itor.iterate()
                self.travesalPvdrs(pvdrs)
            else:
                while not itor.iterate():
                    self.travesalPvdrs(pvdrs)
            self.CORE_STAUS='READY'
        else:
            # Multi-dimension;
            pass

        return

    def runSimStep(self):

        return

# Aro relavant;
    def getAro(self,aroid):
        'Lv1: Get Aro by ID. Return Aro if succeed;'
        for aro in self.ARO_MAP:
            if aro.AroID==aroid:
                return aro
        e='E: Aro not found.'
        return e

    def getAroByName(self,aroname):
        return

    def addAro(self,aroclass):
        ''' Lv1: Add an Aro without initilization.
            Return Aro if succeed;'''
        if type(aroclass)==str:
            expr='aro='+aroclass+'()'
            _locals=dict(locals())
            exec(expr,globals(),_locals)
            aro=_locals['aro']
        else:aro=aroclass()
        self.AROID_MAX+=1
        aro.AroID=self.AROID_MAX
        self.ARO_MAP.append(aro)
        return aro

    def delAro(self,aroid):
        'Lv2: Return deleted Aro if succeed;'
        aro=self.getAro(aroid)
        if type(aro)!=str:
            self.ARO_MAP.remove(aro)
        return aro

    def initAro(self,aroclass,arove):
        'Lv3: Add an Aro with initilization;'
        aro=self.addAro(aroclass)
        if type(aro)!=str:
            self.setArove(aro.AroID,arove)
        return aro

    def setArove(self,aroid,arove):
        ''' Lv2: Set Arove with Arove dict.

            AroID, AroClass shouldnt be set;'''
        aro=self.getAro(aroid)
        if type(aro)!=str:
            aro.__dict__.update(arove)
            if 'AroID' in arove:
                self.AROID_MAX=max(arove['AroID'],self.AROID_MAX)
        return aro

    def delArove(self,aroid,anl):
        'Lv2: Delete Arove by name list;'
        aro=self.getAro(aroid)
        if type(aro)!=str:
            for kw in anl:
                aro.__dict__.pop(kw,None)
        return

    def getArove(self,aroid,anl=[]):
        'Lv2: Get Arove by name list, empty for all;'
        aro=self.getAro(aroid)
        if type(aro)==str: return aro

        if anl==[]: return aro.__dict__
        tmpdict={}
        for an in anl:
            v=aro.__dict__.get(an,'NA')
            if v!='VA':tmpdict[an]=v

        if tmpdict=={}: return self.bug('E: Arove not found.')
        else: return tmpdict
        return

# Acp relavant;
    def getAcp(self,acpid,acpmodel):
        'Lv1: Get Acp by AcpID;'
        for model,acplist in self.ACP_MAP.items():
            if model==acpmodel:
                for acp in acplist:
                    if acp.AcpID==acpid: return acp
        # self.bug('E: Acp not found.')
        return 'E: Acp not found.'

    def addAcp(self,acpclass,acpmodel):
        'Lv1: Add an Acp into list. Return added Acp;'
        if type(acpclass)==str:
            expr='acp='+acpclass+'()'
            _locals=dict(locals())
            exec(expr,globals(),_locals)
            acp=_locals['acp']
        else:acp=acpclass()
        if acpmodel not in self.ACP_MAP:
            self.ACP_MAP[acpmodel]=[]
            self.ACPID_MAX[acpmodel]=0
        self.ACPID_MAX[acpmodel]+=1
        acp.AcpID=self.ACPID_MAX[acpmodel]
        self.ACP_MAP[acpmodel].append(acp)
        return acp

    def setAcp(self,acpid,acpo,acpmodel):
        '''Lv2: Set Acp with acpo dict.

            AcpID shouldnt be set manually;'''
        acp=self.getAcp(acpid,acpmodel)
        if type(acp)!=str:
            acp.__dict__.update(acpo)
            # AcpID has changed;
            if 'AcpID' in acpo:
                self.ACPID_MAX[acpmodel]=max(acpo['AcpID'],self.ACPID_MAX[acpmodel])
        return acp

    def delAcp(self,acpid,acpmodel):
        'Lv2: Deleted an Acp. Return deleted Acp;'
        acp=self.getAcp(acpid,acpmodel)
        if type(acp) is str:return acp
        for ip,ip_tar in acp.inport.items():
            if ip_tar is None:continue
            acpid=ip_tar[0]
            port=ip_tar[1]
            tar_acp=self.getAcp(acpid,acpmodel)
            tar_acp.outport[port].remove((acp.AcpID,ip))
        for op,op_tar_list in acp.outport.items():
            if op_tar_list==[]:continue
            for op_tar in op_tar_list:
                acpid=op_tar[0]
                port=op_tar[1]
                tar_acp=self.getAcp(acpid,acpmodel)
                tar_acp.inport[port]=None
        self.ACP_MAP[acpmodel].remove(acp)
        return acp

    def initAcp(self,acpclass,acpo,acpmodel):
        '''Lv3: Add an Acp with initilization.

            Acpo must contain AcpID;'''
        acp=self.addAcp(acpclass,acpmodel)
        if type(acp)!=str:
            acp=self.setAcp(acp.AcpID,acpo,acpmodel)

        return acp

    def connectAcp(self,sid,stport,eid,edport,acpmodel):
        ''' Lv.2: Connect Acp port.

            Return 1 for connection while 0 for disconnetion.

            Repeat ports to remove this connection.

            Inport only accepts one while outport can accept more;'''
        sacp=self.getAcp(sid,acpmodel)
        eacp=self.getAcp(eid,acpmodel)
        s_combo=(sid,stport)
        e_combo=(eid,edport)
        if stport in sacp.outport:
            # Outport to inport;
            if edport in eacp.inport:
                if eacp.inport[edport] is None:
                    # New connection;
                    eacp.inport[edport]=s_combo
                    sacp.outport[stport].append(e_combo)
                    return 1
                elif eacp.inport[edport]==s_combo:
                    # Delete connection;
                    eacp.inport[edport]=None
                    sacp.outport[stport].remove(e_combo)
                    return 0
                else:self.bug('E: End inport already connected.')
            else:return self.bug('E: End inport not existed.')
        elif stport in sacp.inport:
            # Inport to outport;
            if edport in eacp.outport:
                if s_combo not in eacp.outport[edport]:
                    # New connection;
                    eacp.outport[edport].append(s_combo)
                    sacp.inport[stport]=e_combo
                    return 1
                else:
                    # Delete connection;
                    eacp.outport[edport].remove(s_combo)
                    sacp.inport[stport]=None
                    return 0
            else:return self.bug('E: End outport not existed.')
        else:return self.bug('E: Start port not existed.')
        return

    def reqAcp(self,acp,acpmodel,paradict={}):
        ''' Lv2: Request Acp.

            Para acp accepts str for mark,

            int for AcpID or Acp self;'''
        # Para check;
        if type(acp) is str:
            for anl in self.ACP_MAP[acpmodel]:
                if anl.AcpName==acp:
                    acp=anl
                    break
            if type(acp) is str:return self.bug('E: AcpName not existed.')
        elif type(acp) is int:
            acp=self.getAcp(acp,acpmodel)
            if type(acp) is str:return self.bug(acp)

        # Needed var;
        acproot=acp
        stack=list()
        stack.append(acproot)
        datadict=dict()
        datadict.update(paradict)
        if len(self.ARO_QUEUE)==0:self.ARO_QUEUE.append(list(self.ARO_MAP))

        # Main travesal;
        while len(stack)!=0:
            if len(stack)>self.ACP_DEPTH:return self.bug('E: Acp too deep.')
            acp=stack[-1]
            # Requesting check;
            datadict.update(acp.preProgress(datadict))
            # IOports check;
            out_ready=True
            for port in acp.outport.keys():
                if (acp.AcpID,port) not in datadict:
                    out_ready=False
                    break
            in_ready=True
            for vout in acp.inport.values():
                if vout not in datadict:
                    in_ready=False
                    stack.append(self.getAcp(vout[0],acpmodel))
                    break
            # Checked;
            if out_ready and in_ready:
                # All ready, post progress;
                datadict.update(acp.postProgress(datadict))
                stack.pop()
            elif in_ready:
                # Inport all ready, calculate Acp;
                try:ret=acp.AcpProgress(datadict)
                except BaseException as e:
                    self.bug('E: Acp Calculation.'+e.__str__())
                    self.CORE_STAUS='STOP'
                    return None,None
                datadict.update(ret)
            continue

        # End travesal and return;
        retdict=dict()
        for k,v in datadict.items():
            acpid=k[0]
            if acpid==acproot.AcpID:
                acpport=k[1]
                retdict[acpport]=v
        return retdict,datadict

# Model reravant;
    def getModelPath(self,acpmodel):
        'Lv1: Get model path even not existed.'
        if acpmodel[0]==self.SIM_NAME:
            path='sim/'+acpmodel[0]+'/model/'+acpmodel[1]+'.py'
        else:
            path='mod/'+acpmodel[0]+'/model/'+acpmodel[1]+'.py'
        return path

    def newModelFile(self,modelname):
        'Lv2: Create a new model in opened sim.'
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        if modelname not in self.ACP_MAP:
            self.ACP_MAP[(self.SIM_NAME,modelname)]=list()
            self.ACPID_MAX[(self.SIM_NAME,modelname)]=0
        else:
            return self.bug('E: Model name already existed.')
        return

    def updateModelFile(self,acpmodel=None):
        ''' Lv2: Update model files by ESC.ACP_MAP.

            Empty para acpmodel for all models;'''
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        if acpmodel is None:
            models=list(self.ACP_MAP.keys())
        else: models=[acpmodel]

        for model in models:
            # Build index and key dict;
            acp_index=[]
            key_dict=dict()
            for acp in self.ACP_MAP[model]:
                acp_index.append(acp.AcpID)
                for k,v in acp.__dict__.items():
                    if k not in key_dict.values():
                        key_dict[len(key_dict)+1]=k
            # Complete building;
            txt='ACP_INDEX='+acp_index.__str__()+'\n'
            txt+='KEY_DICT='+key_dict.__str__()+'\n'
            # Replace key;
            for acp in self.ACP_MAP[model]:
                temp_dict=dict(acp.__dict__)
                for k,v in key_dict.items():
                    if v in temp_dict:
                        temp=temp_dict[v]
                        del temp_dict[v]
                        temp_dict[k]=temp
                txt+='Acp_'+str(acp.AcpID)+'='+temp_dict.__str__()+'\n'

            path=self.getModelPath(model)
            with open(path,'w+') as model_fd:
                model_fd.truncate()
                model_fd.write(txt)
        return

    def loadModelFile(self,acpmodel):
        ''' Lv2: Load model from file;'''
        if self.SIM_FD is None:return self.bug('E: Sim not opened.')
        path=self.getModelPath(acpmodel)
        with open(path,'r') as model_fd:
            content=model_fd.read()
        _locals=dict(locals())
        exec(content,globals(),_locals)
        ACP_INDEX=_locals['ACP_INDEX']
        KEY_DICT=_locals['KEY_DICT']
        for acpid in ACP_INDEX:
            acp=_locals['Acp_'+str(acpid)]
            for k,v in KEY_DICT.items():
                if k in acp:
                    temp=acp[k]
                    del acp[k]
                    acp[v]=temp
            self.initAcp(acp['AcpClass'],acp,acpmodel)
        return

# Map relavant;
    def newMapFile(self,mapname):

        return

    def updateMapFile(self,mapname=''):
        'Lv1: Update map;'
        if self.SIM_FD is None: return self.bug('E: Sim not opened.')
        if mapname=='': mapname=self.ARO_MAP_NAME
        # Build index and key dict;
        aro_index=[]
        key_dict=dict()
        for aro in self.ARO_MAP:
            aro_index.append(aro.AroID)
            for k,v in aro.__dict__.items():
                if k not in key_dict.values():
                    key_dict[len(key_dict)+1]=k
        # Complete building;
        txt='ARO_INDEX='+aro_index.__str__()+'\n'
        txt+='KEY_DICT='+key_dict.__str__()+'\n'
        # Replace key;
        for aro in self.ARO_MAP:
            temp_dict=dict(aro.__dict__)
            for k,v in key_dict.items():
                if k in temp_dict:
                    temp=temp_dict[k]
                    del temp_dict[k]
                    temp_dict[v]=temp
            txt+='Aro_'+str(aro.AroID)+'='+temp_dict.__str__()+'\n'

        with open('sim/'+self.SIM_NAME+'/map/'+mapname+'.py','r+') as map_fd:
            map_fd.truncate()
            map_fd.write(txt)
        return

    def loadMapFile(self,mapname=''):
        'Lv1: Read existed map.py;'
        if self.SIM_FD is None: return self.bug('E: Sim not opened.')
        if mapname=='': mapname=self.ARO_MAP_NAME
        self.ARO_MAP=list()
        with open('sim/'+self.SIM_NAME+'/map/'+mapname+'.py','r') as map_fd:
            txt=map_fd.read()
        _locals=dict(locals())
        exec(txt,globals(),_locals)
        aro_index=_locals['ARO_INDEX']
        key_dict=_locals['KEY_DICT']
        for aroid in aro_index:
            aro=_locals['Aro_'+str(aroid)]
            for k,v in key_dict.items():
                if k in aro:
                    temp=aro[k]
                    del aro[k]
                    aro[v]=temp
            self.initAro(aro['AroClass'],aro)
        return

# Other relavant;
    def loadMod(self,modlist):
        ''' Lv1: Load Mod from MOD_LIST.

            Include models and setting;'''
        global mod
        for m in modlist:
            if m not in self.MOD_LIST:
                self.MOD_LIST.append(m)
                _locals=dict(locals())
                exec('import mod.'+m,globals(),_locals)
                exec('from mod.'+m+' import MODEL_INDEX as models',globals(),_locals)
                exec('from mod.'+m+' import MOD_SETTING as mod_setting',globals(),_locals)

            mod_setting=_locals['mod_setting']
            self.setSim(mod_setting,usercall=False)

            models=_locals['models']
            for model in models:
                self.loadModelFile((m,model))
        return

    def travesalPvdrs(self,pvdrs):
        for model,pvdrlist in pvdrs.items():
            for pvdr in pvdrlist:
                ret,data=self.reqAcp(pvdr,model)
                if self.CORE_STAUS=='STOP':
                    return None,None
        return ret,data

    pass

ESC=EvrSimCore()
