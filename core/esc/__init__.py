import os,numpy,shutil,interval
import mod,app
inf=numpy.inf
# from .aro import Aro
# from .acp import Acp
class EvrSimCore(object):
    ''' ## EvrSim Core
        Communicate with memory and files.
        '''
    from .cls import EsTree,TreeNode,EsProcess,EsQueue,SimTree,ModTree,EsEnum
    from .aro import Aro,AroNode,AroGroup,AroSpace
    from .acp import Acp,AcpAttr,AcpPort
    from .acp import AcpSelector,AcpProvider,AcpIterator,AcpExecutor,AcpSetter,AcpGetter
    from .acp import AcpLimitor,AcpEval,AcpVector3,AcpDepartor3,AcpConst,AcpCross
    Itv=interval.Interval

    def __init__(self):
        self.ES_APP=''
        self.CORE_STATUS=0    # Enum for ['READY':0,'BUSY':1,'STOP':2,'STEP':3];
        self.SIM_NAME=''
        self.SIM_TREE=None
        self.MOD_TREE_DICT=dict()
        self.TIME_RATE=1
        self.MODEL_ENABLE=list()
        # Maps and models;
        self.MAP_ORDER=list()
        self.MAP_QUEUE=[dict()]
        self.MAP_ACTIVE=''
        self.MAP_LIST=list()
        self.ACP_MODELS=dict()     # {(modName,modelName):[acplist...]} | {'simInModelName':[...]}
        self.ACPS_PREPARED={'Providers':dict(),'Executors':dict(),'Iterators':dict()}
        self.DATADICT=dict()
        self.COMPILED_MODEL=None
        # User changeable setting;
        self.flag_realtime=True
        self.flag_record=False
        self.len_sim_queue=2
        self.fps=30
        self.max_acp_depth=20
        self.SETTING_DICT={
            'Simulate realtime':'flag_realtime',
            'Record data':'flag_record',
            'Queue length':'len_sim_queue',
            'Max Acp depth':'max_acp_depth',
            'Time step':'fps'}
        return

# Static
    @staticmethod
    def info(string,level='[Info] ',record=False):
        string=level+str(string)
        print(string)
        if record:pass
        return string
    @staticmethod
    def err(errstr,record=False):
        'Report error.'
        EvrSimCore.info(errstr,level='[Err] ',record=record)
        raise BaseException(errstr)
    @staticmethod
    def warn(warnstr,record=False):
        'Report warning.'
        EvrSimCore.info(warnstr,level='[Warn] ',record=record)
        return warnstr
    @staticmethod
    def getCls(cls)->str:
        module=cls.__module__
        name=type(cls).__name__
        if name=='type':
            name=cls.__name__

        return module[0:module.rfind('.')]+'.'+name

# Method
    def initCore(self):
        self.CORE_STATUS=0
        self.SIM_NAME=''
        self.SIM_TREE=None
        self.MOD_TREE_DICT=dict()
        self.TIME_RATE=1
        self.MODEL_ENABLE=list()
        self.MAP_QUEUE=[dict()]
        self.MAP_ACTIVE=''
        self.MAP_LIST=list()
        self.ACP_MODELS=dict()
        self.flag_realtime=True
        self.flag_record=False
        self.len_sim_queue=1
        self.max_acp_depth=20
        self.fps=30
        return
    def getFullMap(self):
        return self.MAP_QUEUE[-1].values()
    def isSimOpened(self):
        return self.SIM_NAME!=''
    def setApp(self,app):
        self.ES_APP=app
        return

# Core status
    def isCoreReady(self):return self.CORE_STATUS==0
    def isCoreBusy(self):return self.CORE_STATUS==1
    def isCoreStop(self):return self.CORE_STATUS==2
    def setCoreReady(self):self.CORE_STATUS=0
    def setCoreBusy(self):self.CORE_STATUS=1
    def setCoreStop(self):self.CORE_STATUS=2

# Aro
    def addAro(self,oncall=True,**arove):
        ''' Add an Aro. Return Aro if succeed.
            * Arove AroClass: Necessary. Accept string/Class;
            * Arove AroID: -1 default for distributing by system;'''
        if 'AroClass' not in arove:EvrSimCore.err('No AroClass.')
        else:aroclass=arove['AroClass']
        if not isinstance(aroclass,str):
            aroclass=self.getCls(aroclass)
            arove['AroClass']=aroclass
        aro:EvrSimCore.Aro=eval(aroclass+'()')
        aroid=arove.get('AroID',-1)
        if aroid==-1:
            if len(self.MAP_ORDER)==0:aro.AroID=1
            else:aro.AroID=max(self.MAP_ORDER)+1
        else:aro.AroID=aroid
        self.setAro(aro,**arove)
        self.MAP_QUEUE[-1][aro.AroID]=aro
        if aro.AroID not in self.MAP_ORDER:
            self.MAP_ORDER.append(aro.AroID)
        if oncall:aro.onAdd()
        return aro
    def getAro(self,idx,queue=-1):
        ''' Get Aro or check parameter.
            Return Aro if succeed, None if failed.
            * Para idx: Accept AroID/Aro/AroName;
            * Para queue: -1 default for getting from the last map snapshot;
            '''
        out:EvrSimCore.Aro=None
        if isinstance(idx,EvrSimCore.Aro):out=idx
        elif isinstance(idx,int):
            if idx in self.MAP_QUEUE[queue]:
                out=self.MAP_QUEUE[queue][idx]
        elif isinstance(idx,str):
            for aro in self.getFullMap():
                if aro.AroName==idx:out=aro
        return out
    def setAro(self,aro,oncall=True,**arove):
        ''' Set Arove with Arove dict.
            Invisible or uneditable Arove wont be set, eg: AroID/AroClass.
            Special var name: inf.
            * Argkw `arove`: A dict is acceptable;
            '''
        aro=self.getAro(aro)
        if 'arove' in arove:arove.update(arove['arove'])
        for k,v in arove.items():
            if not hasattr(aro,k):continue
            setattr(aro,k,v)
        if oncall:aro.onSet()
        return
    def sortAro(self,srcs,tar,direction='after'):
        ''' Para srcs/tar: Accept Aro;'''
        if len(srcs)==1:
            if tar==srcs[0]:return
        new_list=list()
        for aro in srcs:
            self.MAP_ORDER.remove(aro.AroID)
            new_list.append(aro.AroID)
        tar_index=self.MAP_ORDER.index(tar.AroID)
        for newid in new_list:
            self.MAP_ORDER.insert(tar_index+1,newid)
        self.sortMap()
        return
    def loadAro(self,arovestr):
        ''' Load Aro from an Arove dict string.
            Should contain AroID keyword.'''
        arove:dict=eval(arovestr)
        aro=self.addAro(oncall=False,**arove)
        return aro
    def delAro(self,aro,oncall=True):
        aro=self.getAro(aro)
        del self.MAP_QUEUE[-1][aro.AroID]
        if oncall:aro.onDel()
        return aro

# Acp
    def getAcp(self,acpid,mdl)->Acp:
        ''' Get Acp by AcpID. Return None if not found.'''
        for acp in self.ACP_MODELS[mdl]:
            if acp.acpid.value==acpid:return acp
        return
    def addAcp(self,acpclass,mdl):
        ''' Add an Acp to model. Return added Acp.'''
        import core
        if isinstance(acpclass,str):
            acp:self.Acp=eval(acpclass+'()')
        else:acp:self.Acp=acpclass()

        list_acpid=[acp.acpid.value for acp in self.ACP_MODELS[mdl]]
        acp.acpid.value=max([0]+list_acpid)+1
        self.ACP_MODELS[mdl].append(acp)
        return acp
    def setAcp(self,acp,mdl,**acpo):
        ''' Set Acp with acpo dict.
        * Para acp: Accept AcpID/Acp;
        * Para acpo: keyword/acpo;'''
        if isinstance(acp,int):acp=self.getAcp(acp,mdl)
        if 'acpo' in acpo:acpo.update(acpo['acpo'])
        acp.setAcpo(**acpo)
        return
    def delAcp(self,acp,mdl)->Acp:
        ''' Delete an Acp. Return deleted Acp.
        * Para acp: Accept AcpID/Acp;'''
        if isinstance(acp,int):acp=self.getAcp(acp,mdl)
        for pid,port in acp.port.value.items():
            for lacpid,lpid in port.link:
                lacp=self.getAcp(lacpid,mdl)
                lacp.setPort(lpid,link=(acp.acpid.value,pid))
                # Not recommand: setAcp(lacpid,mdl,port={lpid:{link:(acp.acpid.value,pid)}})
        self.ACP_MODELS[mdl].remove(acp)
        return acp
    def clipAcps(self,acps:list,mdl,rmlink=False):
        if isinstance(acps[0],int):
            acps=[self.getAcp(acp) for acp in acps]
        for acp in acps:
            for pid,port in acp.port.value.items():
                for lacpid,lpid in port.link:
                    lacp=self.getAcp(lacpid,mdl)
                    if lacp not in acps or not rmlink:
                        lacp.setPort(lpid,link=(acp.acpid.value,pid))
            self.ACP_MODELS[mdl].remove(acp)
        return acps
    def loadAcp(self,mdl,**acpo):
        ''' Load an Acp from Acpo. Acpo must contain acpid/AcpClass.'''
        acp=self.addAcp(acpo['AcpClass'],mdl)
        acp.setAcpo(**acpo)
        return acp
    def cntAcp(self,stid,stport,edid,edport,mdl):
        ''' Connect Acp ports.
            Return 1 for connection while 0 for disconnetion.
            Repeat ports to remove this connection.
            Inport only accepts one while outport can accept more;'''
        acp_st=self.getAcp(stid,mdl)
        acp_ed=self.getAcp(edid,mdl)
        tuple_st=(stid,stport)
        tuple_ed=(edid,edport)
        if acp_st.port.value[stport].io==acp_ed.port.value[edport].io:
            self.err('Link illgal.')
        if acp_st.port.value[stport].io=='in':
            tpl_in=tuple_st
            tpl_out=tuple_ed
        else:
            tpl_in=tuple_ed
            tpl_out=tuple_st
        acp_in=self.getAcp(tpl_in[0],mdl)
        forelink=acp_in.port.value[tpl_in[1]].link
        if len(forelink)!=0:
            if forelink[0]!=tpl_out:
                acp_in.setPort(tpl_in[1],link=forelink[0])
        acp_st.setPort(stport,link=tuple_ed)
        acp_ed.setPort(edport,link=tuple_st)
        return

# Map
    def newMapFile(self,mapname):
        if not self.isSimOpened():self.err('Sim not opened.')
        if mapname not in self.MAP_LIST:
            self.saveMapFile()
            self.MAP_LIST.append(mapname)
            self.MAP_QUEUE[0].clear()
            self.MAP_ACTIVE=mapname
            self.saveMapFile(mapname)
        else:
            self.err('Map name already existed.')
        return
    def loadMapFile(self,mapname=''):
        ''' Read existed map file, including map in sim or app;
            * Para mapname: Empty default for reloading current map;'''
        if not self.isSimOpened():self.err('Sim not opened.')
        if mapname=='': mapname=self.MAP_ACTIVE
        else: self.MAP_ACTIVE=mapname
        self.MAP_QUEUE[-1]=dict()
        appmap='app/'+self.ES_APP+'/map/'+mapname+'.py'
        simmap='sim/'+self.SIM_NAME+'/map/'+mapname+'.py'
        try:map_fd=open(simmap,'r')
        except BaseException:map_fd=open(appmap,'r')
        txt=map_fd.read()
        map_fd.close()
        _locals=dict(locals())
        exec(txt,globals(),_locals)
        self.MAP_ORDER=_locals['ARO_INDEX']
        key_dict=_locals['KEY_DICT']
        for aroid in self.MAP_ORDER:
            arove=_locals['Aro_'+str(aroid)]
            for k,v in key_dict.items():
                if k in arove:
                    temp=arove[k]
                    del arove[k]
                    arove[v]=temp
            self.addAro(**arove)
        return
    def saveMapFile(self,mapname=''):
        'Lv1: Update map;'
        if not self.isSimOpened(): return self.err('Sim not opened.')
        if mapname=='': mapname=self.MAP_ACTIVE
        # Build index and key dict;
        key_dict=dict()
        for aro in self.getFullMap():
            for k,v in aro.__dict__.items():
                if k in aro._flag['unsave']:continue
                if k not in key_dict.values():
                    key_dict[len(key_dict)+1]=k
        # Complete building;
        txt='ARO_INDEX='+self.MAP_ORDER.__str__()+'\n'
        txt+='KEY_DICT='+key_dict.__str__()+'\n'
        # Replace key;
        for aro in self.getFullMap():
            temp_dict=dict()
            for k,v in aro.__dict__.items():
                if k[0]!='_':temp_dict[k]=v
            for k,v in key_dict.items():
                if v in temp_dict:
                    temp=temp_dict[v]
                    del temp_dict[v]
                    temp_dict[k]=temp
            txt+='Aro_'+str(aro.AroID)+'='+temp_dict.__str__()+'\n'

        with open('sim/'+self.SIM_NAME+'/map/'+mapname+'.py','w+') as map_fd:
            map_fd.truncate()
            map_fd.write(txt)
        return
    def renameMapFile(self,mapname='',newname='NewMap'):
        'Lv1: Rename map;'
        if not self.isSimOpened(): return self.err('Sim not opened.')
        self.saveSim()
        if mapname=='': mapname=self.MAP_ACTIVE
        self.MAP_ACTIVE=newname
        self.MAP_LIST.remove(mapname)
        self.MAP_LIST.append(newname)
        os.rename('sim/'+self.SIM_NAME+'/map/'+mapname+'.py','sim/'+self.SIM_NAME+'/map/'+newname+'.py')
        self.saveSim()
        return
    def sortMap(self):
        ''' Sort and update MAP_ORDER.'''
        new_order=list()
        for aroid in self.MAP_ORDER:
            tstack=[aroid]
            while len(tstack)!=0:
                node=tstack[-1]
                aro=self.getAro(node)
                allow_popout=True
                if hasattr(aro,'children'):
                    if aro.AroID not in new_order:
                        new_order.append(aro.AroID)
                    for child in aro.children:
                        if child not in new_order:
                            allow_popout=False
                            new_order.append(child)
                            tstack.append(child)
                            break
                        elif new_order.index(child)<new_order.index(aro.AroID):
                            allow_popout=False
                            new_order.remove(child)
                            new_order.append(child)
                            tstack.append(child)
                            break
                if allow_popout:
                    if aro.AroID not in new_order:
                        new_order.append(aro.AroID)
                    tstack.pop()
        self.MAP_ORDER=new_order
        return
    def getMapOrder(self):
        return self.MAP_ORDER

# Model
    def getModelPath(self,mdl):
        ''' Get model path even not existed.
        * Para mdl: model tuple like (sim,model);'''
        if mdl[0]==self.SIM_NAME:
            if mdl[0] in os.listdir('sim/'):
                path='sim/'+mdl[0]+'/mdl/'+mdl[1]+'.py'
            else:
                path='app/'+mdl[0]+'/mdl/'+mdl[1]+'.py'
        else:
            path='mod/'+mdl[0]+'/mdl/'+mdl[1]+'.py'
        return path
    def newModelFile(self,mdlname):
        'Lv2: Create a new model in opened sim.'
        if not self.isSimOpened():self.err('Sim not opened.')
        model_tuple=(self.SIM_NAME,mdlname)
        if model_tuple not in self.ACP_MODELS:
            self.ACP_MODELS[model_tuple]=list()
        else:self.err('Model name already existed.')
        return
    def saveModelFile(self,mdl=None):
        ''' Update model files by self.ACP_MODELS.
        * Para mdl: None defa mdl tuple for all models;'''
        # if not self.isSimOpened():return self.err('Sim not opened.')
        if mdl is None:models=list(self.ACP_MODELS.keys())
        else: models=[mdl]

        for model in models:
            # Build index and key dict;
            acp_index=[acp.acpid.value for acp in self.ACP_MODELS[model]]
            key_dict=dict()
            acp:self.Acp
            txt='ACP_INDEX='+str(acp_index)+'\n'
            for acp in self.ACP_MODELS[model]:
                acpo=acp.getAcpo()
                for k,v in acpo.items():
                    if k not in key_dict:
                        key_dict[k]=len(key_dict)+1
                for attr,num in key_dict.items():
                    if attr in acpo:
                        acpo[num]=acpo[attr]
                        del acpo[attr]
                txt+='Acp_'+str(acp.acpid.value)+'='+str(acpo)+'\n'

            txt+='KEY_DICT='+str(key_dict)+'\n'
            path=self.getModelPath(model)
            with open(path,'w+') as model_fd:
                model_fd.truncate()
                model_fd.write(txt)
        return
    def loadModelFile(self,mdl):
        ''' Load model from file;'''
        if not self.isSimOpened():self.err('Sim not opened.')
        if mdl not in self.ACP_MODELS:self.ACP_MODELS[mdl]=list()
        path=self.getModelPath(mdl)
        with open(path,'r') as model_fd:
            content=model_fd.read()
        _locals=dict(locals())
        exec(content,globals(),_locals)
        ACP_INDEX=_locals['ACP_INDEX']
        KEY_DICT=_locals['KEY_DICT']
        for acpid in ACP_INDEX:
            acpo=_locals['Acp_'+str(acpid)]
            for attr,idx in KEY_DICT.items():
                if idx in acpo:
                    acpo[attr]=acpo[idx]
                    del acpo[idx]
            self.loadAcp(mdl,**acpo)
        return
    def renameModelFile(self,mdlname,newname):
        'Rename model in sim.'
        if not self.isSimOpened(): return self.err('Sim not opened.')
        self.saveSim()
        mdl_tuple=(self.SIM_NAME,mdlname)
        new_tuple=(self.SIM_NAME,newname)
        if mdl_tuple in self.MODEL_ENABLE:
            list_enable=list(self.MODEL_ENABLE)
            list_enable.append(new_tuple)
            list_enable.remove(mdl_tuple)
            self.setSim({'MODEL_ENABLE':list_enable})
        tmp_value=self.ACP_MODELS[mdl_tuple]
        self.ACP_MODELS[new_tuple]=tmp_value
        del self.ACP_MODELS[mdl_tuple]
        os.rename('sim/'+self.SIM_NAME+'/model/'+mdlname+'.py','sim/'+self.SIM_NAME+'/model/'+newname+'.py')
        self.saveSim()
        return

# Sim
    def newSim(self,simname,src='_Template'):
        'Lv1: Create new sim by copying para src dir without opening;'
        file_list=os.listdir('sim/')
        for f in file_list:
            if simname==f: return self.err('Sim existed.')
        tar_path='sim/'+simname+'/'
        src_path='sim/'+src+'/'
        shutil.copytree(src_path,tar_path)
        return
    def delSim(self,simname):
        if self.isSimOpened(): return self.err('Sim opened.')
        if simname in os.listdir('sim/'):
            shutil.rmtree('sim/'+simname)
        else: return self.err('Sim not found.')
        return
    def openSim(self,simname):
        'Lv2: Open sim, and load mod and setting;'
        self.initCore()
        if self.isSimOpened(): return self.err('Sim already opened.')

        self.SIM_NAME=simname
        if simname in os.listdir('sim/'):
            path='sim/'+simname+'/sim.py'
            shutil.copy(path,'sim/'+simname+'/_sim.py')
            SIM_FD=open(path,'r+')
        elif simname in os.listdir('app/'):
            path='app/'+simname+'/sim.py'
            shutil.copy(path,'app/'+simname+'/_sim.py')
            SIM_FD=open(path,'r+')
        else: return self.err('Sim not found.')

        # Read sim index;
        simtxt=SIM_FD.read()
        SIM_FD.close()
        _locals=dict()
        exec(simtxt,globals(),_locals)

        self.SIM_TREE=self.SimTree(_locals['SIM_TREE'])
        self.loadMod(self.SIM_TREE.node_mod.data)
        self.setSim(self.SIM_TREE.node_perf.data)
        self.MAP_LIST=self.SIM_TREE.node_map.data
        if self.MAP_ACTIVE=='':self.MAP_ACTIVE=self.MAP_LIST[0]
        self.loadMapFile(self.MAP_ACTIVE)
        for mdl in self.SIM_TREE.node_model.data:
            self.loadModelFile((self.SIM_NAME,mdl))

        return
    def closeSim(self,save=False):
        'Lv2: Close current sim and load default setting;'
        if not self.isSimOpened(): return self.err('Sim not opened.')

        if save:self.saveSim()

        # os.remove('sim/'+self.SIM_NAME+'/_sim.py')

        self.initCore()
        return
    def setSim(self,setdict,usercall=True):
        ''' Set sim in tree.
            * Para usercall: True default.
            Wouldnt change simtree perf if not usercall;'''
        if not self.isSimOpened():return self.err('Sim not opened.')
        for k,v in setdict.items():
            if k not in self.__dict__:continue
            if k not in self.SIM_TREE.node_perf.data or usercall:
                self.__dict__[k]=v
                if usercall:self.SIM_TREE.node_perf.data[k]=v
        return
    def saveSim(self):
        'Save current sim;'
        if not self.isSimOpened():return self.err('Sim not opened.')
        self.saveModelFile()
        self.saveMapFile()
        treestr='SIM_TREE='+self.SIM_TREE.saveTree(savedata=True)
        try:
            SIM_FD=open('sim/'+self.SIM_NAME+'/sim.py','r+')
        except BaseException:
            SIM_FD=open('app/'+self.SIM_NAME+'/sim.py','r+')
        SIM_FD.seek(0,0)
        SIM_FD.truncate()
        SIM_FD.write(treestr)
        SIM_FD.flush()
        SIM_FD.close()
        return
    def resetSim(self):
        self.ACPS_PREPARED['Providers']=dict()
        self.loadMapFile()
        return

# Run
    def CollectAcps(self):
        for model,acplist in self.ACP_MODELS.items():
            if model not in self.MODEL_ENABLE:continue
            for acp in acplist:
                if isinstance(acp,self.AcpIterator):
                    if acp.item not in self.ACPS_PREPARED['Iterators']:
                        self.ACPS_PREPARED['Iterators'][acp.item]=list()
                    if acp not in self.ACPS_PREPARED['Iterators'][acp.item]:
                        self.ACPS_PREPARED['Iterators'][acp.item].append(acp)
                elif isinstance(acp,self.AcpProvider):
                    if model not in self.ACPS_PREPARED['Providers']:
                        self.ACPS_PREPARED['Providers'][model]=list()
                    self.ACPS_PREPARED['Providers'][model].append(acp)
                elif isinstance(acp,self.AcpExecutor):
                    if model not in self.ACPS_PREPARED['Executors']:
                        self.ACPS_PREPARED['Executors'][model]=list()
                    self.ACPS_PREPARED['Executors'][model].append(acp)
        return
    def reqAcp(self,acp:Acp,mdl):
        ''' Request Acp.'''
        # Needed var;
        datadict=self.DATADICT
        stack=list()
        track=list()
        stack.append(acp)

        # Main travesal;
        while len(stack)!=0:
            # if len(stack)>self.max_acp_depth:self.err('Acp too deep.')
            acp=stack[-1]
            acpid=acp.getAcpo('acpid')
            # Requesting check;
            if hasattr(acp,'preProgress'):acp.preProgress()
            # IOports check;
            out_ready=True
            for port in acp.getPort(io='out'):
                if (acpid,port.pid) not in datadict:
                    out_ready=False
                    break
            in_ready=True
            for port in acp.getPort(io='in'):

                if port.link[0] not in datadict:
                    in_ready=False
                    stack.append(self.getAcp(port.link[0][0],mdl))
                    break
            # Checked;
            if out_ready and in_ready:
                # All ready, post progress;
                try:
                    if hasattr(acp,'postProgress'):
                        acp.postProgress()
                except BaseException as e:
                    self.setCoreStop()
                    self.err('Post progressing in '+acp.getAcpo('acp_name')+' '+str(e))
                stack.pop()
                track.append(acp)
            elif in_ready:
                # Inport all ready, calculate Acp;
                try:
                    if hasattr(acp,'AcpProgress'):
                        acp.AcpProgress()
                except BaseException as e:
                    self.setCoreStop()
                    self.err('Acp progressing in '+acp.getAcpo('acp_name')+' '+str(e))
            continue

        return track
    def runCompiledSim(self):
        # s=time.time()
        if self.COMPILED_MODEL is None:self.compileModel()
        set_dict=dict()
        for ii in self.COMPILED_MODEL['ITOR']:
            ii:self.AcpIterator
            ii.iterate()

        for oi in self.COMPILED_MODEL['OUTPUT']:
            aroid=oi[0]
            self.DATADICT={'REQ':[aroid]}
            arove=self.COMPILED_MODEL['AROVE_INDEX'][oi[1]]
            for acp in self.COMPILED_MODEL['TRACK_INDEX'][oi[2]]:
                if isinstance(acp,self.AcpProvider):
                    out=self.DATADICT[acp.port.value[1].link[0]][aroid]
                    if len(out[0])==1:out=out[0][0]
                    else:out=out[0]
                elif isinstance(acp,self.AcpSelector):
                    reslist=self.COMPILED_MODEL['INPUT'][(id(acp),aroid)]
                    resdata=list()
                    for resid in reslist:
                        data=getattr(self.getAro(resid),acp.getAcpo('item'))
                        if not isinstance(data,list):data=[data]
                        resdata.append(data)
                    if len(resdata)==0:resdata=[acp.getAcpo('default')]
                    self.DATADICT.update({(acp.getAcpo('acpid'),1):{aroid:resdata}})
                else:
                    if hasattr(acp,'AcpProgress'):acp.AcpProgress()
            if aroid not in set_dict:set_dict[aroid]=dict()
            set_dict[aroid].update({arove:out})

        for aroid,arove in set_dict.items():
            self.setAro(aroid,**arove)
        for ei in self.COMPILED_MODEL['EXCR']:
            ei:self.AcpExecutor
            ei.execute()
        if not self.isCoreStop():
            self.setCoreReady()
        # print(time.time()-s)
        return
    def compileModel(self,mdl=None):
        self.CollectAcps()
        pvdrs=self.ACPS_PREPARED['Providers']
        excrs=self.ACPS_PREPARED['Executors']
        itors=self.ACPS_PREPARED['Iterators']

        INPUT=dict()
        OUTPUT=list()
        EXCR=list()
        ITOR=list()
        AROVE_INDEX=list()
        TRACK_INDEX=list()

        for model,pvdrlist in pvdrs.items():
            for pvdr in pvdrlist:
                self.DATADICT=dict()
                track=self.reqAcp(pvdr,model)
                reqlist=self.DATADICT['REQ']
                if pvdr.item.value in AROVE_INDEX:
                    api=AROVE_INDEX.index(pvdr.item.value)
                else:
                    AROVE_INDEX.append(pvdr.item.value)
                    api=len(AROVE_INDEX)-1
                if track in TRACK_INDEX:
                    ati=TRACK_INDEX.index(track)
                else:
                    TRACK_INDEX.append(track)
                    ati=len(TRACK_INDEX)-1
                for aroid in reqlist:
                    OUTPUT.append([aroid,api,ati])
                    for acp in track:
                        if isinstance(acp,self.AcpSelector):
                            resdict=self.DATADICT[(acp.getAcpo('acpid'),'RES')]
                            INPUT.update({(id(acp),aroid):resdict[aroid]})
        for model,excrlist in excrs.items():
            for _excr in excrlist:
                EXCR.append(_excr)
        for model,itorlist in itors.items():
            for _itor in itorlist:
                ITOR.append(_itor)
        self.COMPILED_MODEL={
            'INPUT':INPUT,
            'OUTPUT':OUTPUT,
            'EXCR':EXCR,
            'ITOR':ITOR,
            'AROVE_INDEX':AROVE_INDEX,
            'TRACK_INDEX':TRACK_INDEX}

        self.resetSim()
        return

# Mod
    def setMod(self):
        return
    def loadMod(self,modlist,unload=False):
        ''' Load Mod from para modlist. Include models and setting.
            * Para unload: unload mod form ESC which not in para modlist;'''
        for modname in modlist:
            if modname not in self.SIM_TREE.node_mod.data:
                self.SIM_TREE.node_mod.data.append(modname)
            if modname not in self.MOD_TREE_DICT:
                exec('import mod.'+modname)
                self.MOD_TREE_DICT[modname]=self.ModTree(modname)

                mod_setting=eval('mod.'+modname+'.MOD_PERF')
                self.setSim(mod_setting,usercall=False)

                model_index=eval('mod.'+modname+'.MODEL_INDEX')
                for model in model_index:
                    self.loadModelFile((modname,model))
        if unload:
            for modname in self.MOD_TREE_DICT:
                'todo: unload mods'
        return
    def getModAttr(self,modname,attrname=None):
        ''' Return attribute in mod or mod self.
            * Para attrname: default for mod self.'''
        if attrname is None:
            try:ret=eval('mod.'+modname)
            except BaseException as e:self.err(e)
        else:
            try:ret=eval('mod.'+modname+'.'+attrname)
            except BaseException as e:self.err(e)
        return ret

    pass
esc=EvrSimCore()
