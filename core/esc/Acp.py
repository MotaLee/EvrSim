import numpy as np
import mod
from core import esc as ESC
class AcpAttr(object):
    def __init__(self,name,value=0,**argkw):
        ''' Acp attribute.
        * Para name: attribute name;
        * Para value: 0 default;
        * Para argkw:
            * type: attr type, auto default;
            * fixed: if attr can be modified, False default;
            * long: if attr is long data, False default;
            * save: if attr can save to file, True default;
            * visible: if attr can display in editor, True default;'''
        self.name=name
        self.value=value
        self.enum_type=argkw.get('type','auto')
        self.flag_visible=argkw.get('visible',True)
        self.flag_fixed=argkw.get('fixed',False)
        self.flag_long=argkw.get('long',False)
        self.flag_save=argkw.get('save',True)
        return
    pass
class AcpPort(object):
    def __init__(self,**argkw):
        ''' Acp port.
        * Para argkw:
            * Para pid: ID for port;
            * Para name: Port name;
            * Para io: Enum for 'in' or 'out';'''
        self.io:str=argkw.get('io')  # 'in' or 'out';
        self.pid:int=argkw.get('pid')
        self.name:str=argkw.get('name')
        self.link=argkw.get('link',list())    # [(AcpID,portid),...];
        return
    pass
class Acp(object):
    def __init__(self):
        self.acpid   =AcpAttr('acpid',-1,visible=False)
        self.acp_name=AcpAttr('Acp Name','NewAcp')
        self.position=AcpAttr('Position',[0,0],visible=False)
        self.desc    =AcpAttr('Desc','',long=True)
        self.fix_in  =AcpAttr('Fix Input',True,visible=False,save=False)
        self.fix_out =AcpAttr('Fix Output',True,visible=False,save=False)
        self.port    =AcpAttr('Port',dict(),visible=False)
        self.AcpClass=AcpAttr('AcpClass',
            self.__module__+'.'+type(self).__name__,
            visible=False)
        return

    def addPort(self,**argkw):
        ''' Para arkw: port/pid/io/name'''
        if 'port' in argkw:port=argkw.get('port')
        else:port=AcpPort(**argkw)
        self.port.value[port.pid]=port
        return

    def setPort(self,pid,**argkw):
        ''' Set Acp port by pid. attr io cannot be set.
            * Para pid: Needed;
            * Para argkw:
                * name: To set name;
                * link: port link;'''
        if 'name' in argkw:
            self.port.value[pid].name=argkw.get('name')
        if 'link' in argkw:
            link=argkw.get('link')
            if isinstance(link,tuple):link=[link]
            for tpl in link:
                if tpl in self.port.value[pid].link:
                    # Repeat tuple to del;
                    self.port.value[pid].link.remove(tpl)
                elif self.port.value[pid].io=='out':
                    # Append for output port;
                    self.port.value[pid].link.append(tpl)
                else:
                    # Replace for input port;
                    self.port.value[pid].link=[tpl]
        return

    def delPort(self,pid):
        del self.port.value[pid]
        return

    def setAcpo(self,**acpo):
        if 'port' in acpo:
            for pdict in acpo['port']:
                pid=pdict['pid']
                del pdict['pid']
                if  pid in self.port.value:
                    # Empty pdict to del port, non-empty to set;
                    if len(pdict)==0:self.delPort(pid)
                    else:self.setPort(pid,**pdict)
                else:
                    self.addPort(pid=pid,**pdict)
            del acpo['port']
        for k,v in acpo.items():
            if hasattr(self,k):getattr(self,k).value=v
        return

    def getAcpo(self,key=''):
        ''' Get Acpo.
            * Para key: Empty default for all Acpo in a dict;'''
        if key=='':
            acpo=dict(vars(self))
            ports=[vars(port) for port in acpo['port'].value.values()]
            del acpo['port']
            for k,v in vars(self).items():
                if isinstance(v,AcpAttr):acpo[k]=v.value
            acpo['port']=ports
        else:
            acpo=getattr(self,key).value
        return acpo

    def getPort(self,**argkw):
        ''' Get ports. No para for all.
            * Para pid: In argkw. By pid;
            * Para name: In argkw. By name;
            * Para io: In argkw. Enum for in/out;
            '''
        if 'pid' in argkw:
            return list(self.port.value[argkw['pid']])
        if 'name' in argkw:
            for port in self.port.value.values():
                if port.name==argkw['name']:return list(port)
        if 'io' in argkw:
            ports=list()
            for port in self.port.value.values():
                if port.io==argkw['io']:ports.append(port)
            return ports
        return list(self.port.value.values())

    def getAcpAttr(self,key='',port=False):
        ''' Get AcpAttr.
            * Para key: Empty default for all AcpAttr in a dict;
            * Para port: False default;'''
        if key=='':
            acpattr:dict=dict(vars(self))
            if not port:del acpattr['port']
            return acpattr
        else:
            acpattr={key:getattr(self,key)}
        return acpattr
    pass

class AcpSetter(Acp):
    def __init__(self):
        super().__init__()
        ''' Input Port name correspond to Arove display name.'''
        self.expression=AcpAttr('Aro Expression','')
        self.fix_out.value=False
        return
    pass

class AcpGetter(Acp):
    def __init__(self):
        super().__init__()
        ''' Output Port name correspond to Arove display name.'''
        self.expression=AcpAttr('Aro Expression','')
        self.fix_in.value=False
        return

    pass

class AcpIterator(Acp):
    def __init__(self):
        ''' Generate iteration.
        * Attr item: Iterator name;
        * Attr current: ;
        * Attr start: ;
        * Attr end: ;
        * Attr step: ;
        * Out 1: Step out;
        * Out 2: Current out;
        * Method iterate: ;'''
        super().__init__()
        self.item=AcpAttr('Item','time')
        self.current=AcpAttr('Current',0)
        self.start=AcpAttr('start',.0)
        self.step=AcpAttr('Step',.1)
        self.end=AcpAttr('End',.0)
        self.addPort(pid=1,name='Step out',io='out')
        self.addPort(pid=2,name='Current out',io='out')
        return

    def iterate(self):
        '''Return 0 when iterator stoped.'''
        if self.current.value>self.end.value and not ESC.flag_realtime:
            return 0
        if self.item.value=='time':
            self.current.value+=ESC.TIME_RATE*ESC.len_timestep
        else:self.current.value+=self.step.value
        return 1

    def AcpProgress(self):
        reqlist=ESC.DATADICT['REQ']
        stepdict=dict()
        curdict=dict()
        for aroid in reqlist:
            stepdict[aroid]=[[self.step.value]]
            curdict[aroid]=[[self.current.value]]
        ESC.DATADICT.update({(self.acpid.value,1):stepdict,(self.acpid.value,2):curdict})
        return
    pass

class AcpExecutor(Acp):
    def __init__(self):
        super().__init__()
        ''' Input Port name correspond to Arove display name.'''
        self.script=AcpAttr('Script','',long=True)
        self.fixIO='Neither'
        self.fix_out.value=False
        self.fix_in.value=False
        return

    def execute(self):
        return
    pass

# Methods;
def getAcp(acpid,mdl)->Acp:
    ''' Get Acp by AcpID. Return None if not found.'''
    for acp in ESC.ACP_MODELS[mdl]:
        if acp.acpid.value==acpid:return acp
    return

def addAcp(acpclass,mdl)->Acp:
    ''' Add an Acp to model. Return added Acp.'''
    mod
    if isinstance(acpclass,str):
        acp:Acp=eval(acpclass+'()')
    else:acp:Acp=acpclass()

    list_acpid=[acp.acpid.value for acp in ESC.ACP_MODELS[mdl]]
    acp.acpid.value=max([0]+list_acpid)+1
    ESC.ACP_MODELS[mdl].append(acp)
    return acp

def setAcp(acp,mdl,**acpo):
    ''' Set Acp with acpo dict.
    * Para acp: Accept AcpID/Acp;
    * Para acpo: keyword/acpo;'''
    if isinstance(acp,int):acp=getAcp(acp,mdl)
    if 'acpo' in acpo:acpo.update(acpo['acpo'])
    acp.setAcpo(**acpo)
    return

def delAcp(acp,mdl)->Acp:
    ''' Delete an Acp. Return deleted Acp.
    * Para acp: Accept AcpID/Acp;'''
    if isinstance(acp,int):acp=getAcp(acp,mdl)
    for pid,port in acp.port.value.items():
        for lacpid,lpid in port.link:
            lacp=getAcp(lacpid,mdl)
            lacp.setPort(lpid,link=(acp.acpid.value,pid))
            # Not recommand: setAcp(lacpid,mdl,port={lpid:{link:(acp.acpid.value,pid)}})
    ESC.ACP_MODELS[mdl].remove(acp)
    return acp

def clipAcps(acps:list,mdl,rmlink=False):
    if isinstance(acps[0],int):
        acps=[getAcp(acp) for acp in acps]
    for acp in acps:
        for pid,port in acp.port.value.items():
            for lacpid,lpid in port.link:
                lacp=getAcp(lacpid,mdl)
                if lacp not in acps or not rmlink:
                    lacp.setPort(lpid,link=(acp.acpid.value,pid))
        ESC.ACP_MODELS[mdl].remove(acp)
    return acps

def loadAcp(mdl,**acpo):
    ''' Load an Acp from Acpo. Acpo must contain acpid/AcpClass.'''
    acp=addAcp(acpo['AcpClass'],mdl)
    acp.setAcpo(**acpo)
    return acp

def cntAcp(stid,stport,edid,edport,mdl):
    ''' Connect Acp ports.

        Return 1 for connection while 0 for disconnetion.

        Repeat ports to remove this connection.

        Inport only accepts one while outport can accept more;'''
    acp_st=getAcp(stid,mdl)
    acp_ed=getAcp(edid,mdl)
    tuple_st=(stid,stport)
    tuple_ed=(edid,edport)
    if acp_st.port.value[stport].io==acp_ed.port.value[edport].io:
        ESC.err('Link illgal.')
    if acp_st.port.value[stport].io=='in':
        tpl_in=tuple_st
        tpl_out=tuple_ed
    else:
        tpl_in=tuple_ed
        tpl_out=tuple_st
    acp_in=getAcp(tpl_in[0],mdl)
    forelink=acp_in.port.value[tpl_in[1]].link
    if len(forelink)!=0:
        if forelink[0]!=tpl_out:
            acp_in.setPort(tpl_in[1],link=forelink[0])
    acp_st.setPort(stport,link=tuple_ed)
    acp_ed.setPort(edport,link=tuple_st)

    return

class AcpSelector(Acp):
    def __init__(self):
        ''' Select Arove in last map snapshot.
        * Attr expression: Expression to select Aroes;
        * Attr item: Arove to select;
        * Attr default: Default output when no Aro matches;
        * Out 1: Item out;'''
        super().__init__()
        self.expression=AcpAttr('Aro Expression','',long=True)
        self.default=AcpAttr('defalut',0)
        self.item=AcpAttr('Item','')
        self.addPort(pid=1,name='Item out',io='out')
        return

    def AcpProgress(self):
        'ESC.ARO_QUEUE[-1] needed.'
        reqlist=ESC.DATADICT['REQ']
        slctdict=dict()
        resdict=dict()
        for SELF_AROID in reqlist:
            SELF_ARO=ESC.getAro(SELF_AROID,queue=0)
            slctdict[SELF_AROID]=list()
            resdict[SELF_AROID]=list()
            for ARO in ESC.MAP_QUEUE[0].values():
                AROVE=ARO.__dict__
                ABBRCLASS=ARO.AroClass[ARO.AroClass.rfind('.')+1:]
                try:ev=eval(self.expression.value)
                except BaseException:ev=False
                if ev:
                    if not isinstance(AROVE[self.item.value],list):
                        # Convert single int to vec1;
                        data=[AROVE[self.item.value]]
                    else:
                        data=AROVE[self.item.value]
                    resdict[SELF_AROID].append(ARO.AroID)
                    slctdict[SELF_AROID].append(data)
            if len(slctdict[SELF_AROID])==0:
                slctdict[SELF_AROID]=[self.default.value]
        if len(list(slctdict.values())[0])==0:
            ESC.warn('Selector '+self.acp_name.value+' matched nothing.')
        ESC.DATADICT.update({
            (self.acpid.value,1):slctdict,
            (self.acpid.value,'RES'):resdict})
        return
    pass

class AcpProvider(Acp):
    def __init__(self):
        ''' Provide Arove to Aro map.
        * Attr expression: Expression to select Aroes;
        * Attr item: Arove to select;
        * Attr default: Default output when no Aro matches;
        * Out 1: Item out;'''
        super().__init__()
        self.expression=AcpAttr('Aro Expression','',long=True)
        self.item=AcpAttr('Item','')
        self.addPort(pid=1,name='Item in',io='in')
        return

    def preProgress(self):
        arolist=list()
        for ARO in ESC.getFullMap():
            ABBRCLASS=ARO.AroClass[ARO.AroClass.rfind('.')+1:]
            AROVE=ARO.__dict__
            target=eval(self.expression.value)
            if target: arolist.append(ARO.AroID)
        ESC.DATADICT.update({'REQ':arolist})
        return

    def postProgress(self):
        indict=ESC.DATADICT[self.port.value[1].link[0]]
        reqlist=ESC.DATADICT['REQ']
        for aroid,itemvalue in indict.items():
            if aroid in reqlist:
                if len(itemvalue)!=1:ESC.err('Provide too more')
                if len(itemvalue[0])==1:
                    data=itemvalue[0][0]
                else:
                    data=itemvalue[0]
                ESC.setAro(aroid,{self.item.value:data})
        return
    pass

class AcpLimitor(Acp):
    def __init__(self):
        ''' Limit output.
        * Attr expression: Expression to select Aroes;
        * Attr item: Arove to select;
        * Attr default: Default output when no Aro matches;
        * Out 1: Item out;'''
        super().__init__()
        self.up=AcpAttr('Up','Inf')
        self.low=AcpAttr('Low','Inf')
        self.up_trigger=AcpAttr('Up Trigger',None)
        self.low_trigger=AcpAttr('Low Trigger',None)
        self.addPort(pid=1,name='In',io='in')
        self.addPort(pid=2,name='Out',io='out')
        return

    def AcpProgress(self):
        indata=ESC.DATADICT[self.port.value[1].link[0]]
        for inkey,invalue in indata.items():
            for i in range(0,len(invalue)):
                for j in range(0,len(invalue[i])):
                    if self.low.value!='Inf' and invalue[i][j]<=self.low.value:
                        if self.low_trigger.value is None:
                            invalue[i][j]=self.low.value
                        else:invalue[i][j]=self.low_trigger.value
                        break
                    if self.up.value!='Inf' and invalue[i][j]>=self.up.value:
                        if self.up_trigger.value is None:
                            invalue[i][j]=self.up.value
                        else:invalue[i][j]=self.up_trigger.value
            indata[inkey]=invalue
        ESC.DATADICT.update({(self.acpid.value,2):indata})
        return
    pass

class AcpPMTD(Acp):
    def __init__(self):
        ''' PMTD Function. Accept single value list input.
        * Attr expression: Expression to calculate;
        * In 1: symbol a;
        * In 2: symbol b, up to 5 input;
        * Out 0: Value out;'''
        super().__init__()
        self.fix_out.value=True
        self.expression=AcpAttr('Expression','',long=True)  # Use symbol a and b to do PMTD;
        self.addPort(pid=0,name='Out',io='out')
        self.addPort(pid=1,name='In a',io='in')
        self.addPort(pid=2,name='In b',io='in')
        return

    def AcpProgress(self):
        max_dict=dict()
        sym_dict=dict()
        symindex='abcde'
        for pid,port in self.port.value.items():
            if pid==0:continue
            d=ESC.DATADICT[port.link[0]]
            if len(d)>len(max_dict) and type(list(d.keys())[0])==int:max_dict=d
            sym=symindex[pid-1]
            sym_dict[sym]=np.array(list(d.values()))
        res=eval(self.expression.value,globals(),sym_dict)

        output_dict=dict()
        i=0
        for k in max_dict:
            output_dict[k]=res[i].tolist()
            i+=1
        # opid=list(self.outport.keys())[0]
        ESC.DATADICT.update({(self.acpid.value,0):output_dict})
        return
    pass

class AcpVector3(Acp):
    def __init__(self):
        super().__init__()
        ''' vectpr3.
        * In 1,2,3: x,y,z in;
        * Out 0: Value out;'''
        self.addPort(pid=0,name='Our',io='out')
        self.addPort(pid=1,name='In x',io='in')
        self.addPort(pid=2,name='In y',io='in')
        self.addPort(pid=3,name='In z',io='in')
        return

    def AcpProgress(self):
        xdict=ESC.DATADICT[self.port.value[1].link[0]]
        ydict=ESC.DATADICT[self.port.value[2].link[0]]
        zdict=ESC.DATADICT[self.port.value[3].link[0]]

        vec3_dict=dict()
        for aroid,xlist in xdict.items():
            for i in range(0,len(xlist)):
                if aroid not in vec3_dict:
                    vec3_dict[aroid]=list()
                vec3=[xlist[i][0],ydict[aroid][i][0],zdict[aroid][i][0]]
                vec3_dict[aroid]=[vec3]
        ESC.DATADICT.update({(self.acpid.value,4):vec3_dict})
        return

    pass

class AcpDepartor3(Acp):
    def __init__(self):
        ''' departot3.
        * In 1,2,3: x,y,z in;
        * Out 0: Value out;'''
        super().__init__()
        self.addPort(pid=0,name='In vec3',io='in')
        self.addPort(pid=1,name='x',io='out')
        self.addPort(pid=2,name='y',io='out')
        self.addPort(pid=3,name='z',io='out')
        return

    def AcpProgress(self):
        vec3_dict=ESC.DATADICT[self.port.value[1].link[0]]
        xdict=dict()
        ydict=dict()
        zdict=dict()
        for aroid,vec3list in vec3_dict.items():
            for vec3 in vec3list:
                if aroid not in xdict:
                    xdict[aroid]=list()
                    ydict[aroid]=list()
                    zdict[aroid]=list()
                xdict[aroid].append([vec3[0]])
                ydict[aroid].append([vec3[1]])
                zdict[aroid].append([vec3[2]])
        ESC.DATADICT.update({
            (self.acpid.value,1):xdict,
            (self.acpid.value,2):ydict,
            (self.acpid.value,3):zdict})
        return
    pass

class AcpConst(Acp):
    def __init__(self):
        super().__init__()
        self.item=AcpAttr('Item','')
        self.value=AcpAttr('Value',0)
        self.addPort(pid=1,name='Out',io='out')
        return

    def AcpProgress(self):
        if type(self.value.value)!=list:out=[self.value.value]
        else:out=self.value.value
        reqlist=ESC.DATADICT['REQ']
        outdict=dict()
        for aroid in reqlist:
            outdict[aroid]=[out]
        ESC.DATADICT.update({(self.acpid.value,1):outdict})
        return
    pass

class AcpNorm(Acp):
    def __init__(self):
        super().__init__()
        self.addPort(pid=1,name='in vec',io='in')
        self.addPort(pid=2,name='out norm',io='out')
        return

    def AcpProgress(self):
        vec_dict=ESC.DATADICT[self.port.value[1].link[0]]
        out_dict=dict()
        for aroid,vec_list in vec_dict.items():
            out_dict[aroid]=list()
            for vec in vec_list:
                vec=np.array(vec)
                out_dict[aroid].append([np.linalg.norm(vec)])
        ESC.DATADICT.update({(self.acpid.value,2):out_dict})
        return
    pass

class AcpSum(Acp):
    def __init__(self):
        super().__init__()
        self.addPort(pid=1,name='in',io='in')
        self.addPort(pid=2,name='out sum',io='out')
        return

    def AcpProgress(self):
        in_dict=ESC.DATADICT[self.port.value[1].link[0]]
        out_dict=dict()
        for aroid,dlist in in_dict.items():
            # darr=np.array(dlist)
            nparr=np.sum(dlist,axis=0)
            out_dict[aroid]=[nparr.tolist()]
        ESC.DATADICT.update({(self.acpid.value,2):out_dict})
        return
    pass

class AcpCross(Acp):
    def __init__(self):
        super().__init__()
        self.addPort(pid=0,name='out',io='out')
        self.addPort(pid=1,name='in a',io='in')
        self.addPort(pid=2,name='in b',io='in')
        return

    def AcpProgress(self):
        v1dict=ESC.DATADICT[self.port.value[1].link[0]]
        v2dict=ESC.DATADICT[self.port.value[2].link[0]]
        output_dict=dict()
        if type(list(v1dict.keys())[0])==int:
            tardict=v1dict
        else:
            tardict=v2dict
        i=0
        for k in tardict:
            v1_value=list(v1dict.values())[i]
            v2_value=list(v2dict.values())[i]
            output_dict[k]=np.cross(v1_value,v2_value).tolist()
            i+=1
        ESC.DATADICT.update({(self.acpid.value,0):output_dict})
        return
    pass
