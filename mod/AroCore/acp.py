import sys
import numpy as np
import interval as itv
from core import ESC
# Acp class defination;
class Acp(object):
    'Arove calculation part;'
    def __init__(self):
        self._acpo_flag={
            'invisible':[
                '_acpo_flag','AcpID','AcpClass','position',
                'fixIO','port','inport','outport'],
            'longdata':['desc'],
            'uneditable':[]
        }
        self.AcpID=0
        self.AcpClass=self.__module__+'.'+type(self).__name__
        self.position=[0,0]
        self.fixIO='Both'   # Both/In/Out/Neither
        self.port=dict()   # {portid:'name',...};
        self.inport=dict()   # {portid:(childAcpID,portid),...};
        self.outport=dict()  # {portid:[(ParentAcpID,portid),...],...};

        self.AcpName=''
        self.desc=''
        self.static=False
        return

    def preProgress(self,datadict):
        ''' Generate requesting dict.

            Be called before ports checking;'''
        return {}

    def AcpProgress(self,datadict):
        ''' Calculate Acp.

            Be called after inports ready.

            Returning datadict forms like:

            `{(AcpID,portID):{items:[data...]}}`;'''
        return {}

    def postProgress(self,datadict):
        ''' Fill the requesting dict

            Be called after ports checking.

            Should be overrided by sub class;'''
        return {}

    def presetVar(self):
        '''ARO, SELF_ARO, SELF_AROID, AROVE, etc.'''
        return
    pass

# Base Acp;
class AcpSelector(Acp):
    ''' Select Aro/Arove in last map snapshot.

        Addition: expression, item.

        Outport: output.

        Inport: None.

        Para item: Empty for Aro, else Arove;'''
    def __init__(self):
        super().__init__()
        self._acpo_flag['longdata'].append('expression')
        self.expression=''   # Selecting expression;
        self.item=''    # Arove item to select;
        self.default=0
        self.outport={1:list()}
        self.port={1:'out'}
        return

    def AcpProgress(self,datadict):
        'ESC.ARO_QUEUE[-1] needed.'
        for kturple in datadict.keys():
            if 'REQ' in kturple:
                reqlist=datadict[kturple]
        slctdict=dict()
        for SELF_AROID in reqlist:
            SELF_ARO=ESC.getAro(SELF_AROID,queue=-1)
            selfdict={SELF_AROID:list()}
            for ARO in ESC.MAP_QUEUE[-1]:
                # Keyword defination;
                AROVE=ARO.__dict__
                AROCLASS_ABBR=AROVE['AroClass'][AROVE['AroClass'].rfind('.')+1:]
                try:ev=eval(self.expression)
                except BaseException:ev=False
                if ev:
                    if self.item=='':
                        data=[SELF_ARO]
                    elif type(AROVE[self.item])!=list:
                        # Convert single int to vec1;
                        data=[AROVE[self.item]]
                    else:
                        data=AROVE[self.item]
                    selfdict[SELF_AROID].append(data)
            for aroid,vlist in selfdict.items():
                if len(vlist)==0:selfdict[aroid].append(self.default)
            slctdict.update(selfdict)
            if len(list(slctdict.values())[0])==0:ESC.bug('W: Selector '+self.AcpName+' matched nothing.')
        return {(self.AcpID,1):slctdict}
    pass

class AcpProvider(Acp):
    ''' Addition: expression, item.

        Outport: None.

        Inport: input;'''
    def __init__(self):
        super().__init__()
        self._acpo_flag['longdata'].append('expression')
        self.expression=''   # Aro target expression to provide;
        self.item=''    # Arove item to provide, empty for Aro;
        self.inport={1:None}
        self.port={1:'in'}
        return

    def preProgress(self,datadict):
        datakey=(self.AcpID,'REQ')
        if datakey in datadict: return {}
        reqdict={datakey:list()}
        arolist=list()
        for ARO in ESC.ARO_MAP:
            # Keyword defination;
            AROVE=ARO.__dict__
            AROCLASS_ABBR=AROVE['AroClass'][AROVE['AroClass'].rfind('.')+1:]
            target=eval(self.expression.__str__())
            if target: arolist.append(ARO.AroID)
        reqdict[datakey]=arolist
        return reqdict

    def postProgress(self,datadict):
        indict=datadict[self.inport[1]]
        reqlist=datadict[(self.AcpID,'REQ')]
        for aroid,itemvalue in indict.items():
            if aroid in reqlist:
                if len(itemvalue)!=1:return ESC.bug('E: Provide too more')
                if len(itemvalue[0])==1:
                    data=itemvalue[0][0]
                else:
                    data=itemvalue[0]
                ESC.setAro(aroid,{self.item:data})
        return {}
    pass

class AcpIterator(Acp):
    ''' Addition: item, current, step, start, end.

        Outport: output.

        Inport: None;'''
    def __init__(self):
        super().__init__()
        self.item=''    # Special for 'time', 'x' in ESWx;
        self.current=0
        self.start=0
        self.step=0.1
        self.end=1
        self.outport={1:[],2:[]}
        self.port={1:'step out',2:'current out'}
        return

    def AcpProgress(self,datadict):
        op1=(self.AcpID,1)
        op2=(self.AcpID,2)
        if self.item=='time':out1=ESC.TIME_RATE*ESC.TIME_STEP
        else:out1=self.step
        ret={op1:{self.item:[out1]},
            op2:{self.item:[self.current]}}
        return ret

    def iterate(self):
        'Return 0 when iterator stoped;'
        if self.current>self.end and not ESC.SIM_REALTIME:
            return 0
        if self.item=='time':self.current+=ESC.TIME_RATE*ESC.TIME_STEP
        else:self.current+=self.step
        return 1

    pass

class AcpGroup(Acp):
    pass

class AcpMCU(Acp):
    ''' Process IO like a MCU.

        Addition: script.

        Outport: adjustable.

        Inport: adjustable.'''
    def __init__(self):
        super().__init__()
        self._acpo_flag['long'].append('script')
        self.fixIO='Neither'
        self.script=''
        self.script_path=''
        return

    def AcpProgress(self,data):
        for inkey,invalue in self.inport.items():
            locals[self.port[inkey]]=data[invalue]

        return
    pass

class AcpExecutor(Acp):
    def __init__(self):
        super().__init__()
        self._acpo_flag['longdata'].append('script')
        self.script=''
        self.fixIO='Neither'
        return
    pass

# Operator;
class AcpLimitor(Acp):
    ''' Addition: up/low/up_trigger/low_trigger.

        Outport: output.

        Inport: input;'''
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={2:list()}
        self.port={1:'in',2:'out'}
        self.up='Inf'
        self.low='Inf'
        self.up_trigger=None
        self.low_trigger=None
        return

    def AcpProgress(self,data):
        indata=data[self.inport[1]]
        for inkey,invalue in indata.items():
            for i in range(0,len(invalue)):
                for j in range(0,len(invalue[i])):
                    if self.low!='Inf' and invalue[i][j]<=self.low:
                        if self.low_trigger is None:invalue[i][j]=self.low
                        else:invalue[i][j]=self.low_trigger
                        break
                    if self.up!='Inf' and invalue[i][j]>=self.up:
                        if self.up_trigger is None:invalue[i][j]=self.up
                        else:invalue[i][j]=self.up_trigger
            indata[inkey]=invalue
        return {(self.AcpID,2):indata}
    pass

class AcpPMTD(Acp):
    ''' PMTD Function. Accept single value list input.

        Addition: expression.

        Inport: adjustable.

        Outport: output;'''
    def __init__(self):
        super().__init__()
        self.fixIO='Out'
        self.expression=''  # Use symbol a and b to do PMTD;
        self.inport={1:None,2:None}
        self.outport={0:[]}
        self.port={0:'out R',1:'in a',2:'in b'}
        return

    def AcpProgress(self,datadict):
        max_dict=dict()
        sym_dict=dict()
        symindex='abcdefghijklmnopqrstuvwxyz'
        for inkey,invalue in self.inport.items():
            d=datadict[invalue]
            if len(d)>len(max_dict) and type(list(d.keys())[0])==int:max_dict=d
            sym=symindex[inkey-1]
            sym_dict[sym]=np.array(list(d.values()))
        res=eval(self.expression,globals(),sym_dict)

        output_dict=dict()
        i=0
        for k in max_dict:
            output_dict[k]=res[i].tolist()
            i+=1
        opid=list(self.outport.keys())[0]
        return {(self.AcpID,opid):output_dict}
    pass

class AcpVector3(Acp):
    ''' Addition: None.

        Inport: x, y, z;

        Outport: vec3.'''
    def __init__(self):
        super().__init__()
        self.inport={1:None,2:None,3:None}
        self.outport={4:[]}
        self.port={1:'in x',2:'in y',3:'in z',4:'out vec3'}
        return

    def AcpProgress(self,datadict):
        xdict=datadict[self.inport[1]]
        ydict=datadict[self.inport[2]]
        zdict=datadict[self.inport[3]]

        vec3_dict=dict()
        for aroid,xlist in xdict.items():
            for i in range(0,len(xlist)):
                if aroid not in vec3_dict:
                    vec3_dict[aroid]=list()
                vec3=[xlist[i][0],ydict[aroid][i][0],zdict[aroid][i][0]]
                vec3_dict[aroid]=[vec3]

        return {(self.AcpID,4):vec3_dict}

    pass

class AcpDepartor3(Acp):
    ''' Addition: None.

        Inport: vec3.

        Outport: x, y, z.;'''
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={2:[],3:[],4:[]}
        self.port={1:'in vec3',2:'out x',3:'out y',4:'out z'}
        return

    def AcpProgress(self,datadict):
        vec3_dict=datadict[self.inport[1]]
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
        return {(self.AcpID,2):xdict,(self.AcpID,3):ydict,(self.AcpID,4):zdict}
    pass

class AcpConst(Acp):
    def __init__(self):
        super().__init__()
        self.item=''
        self.value=0
        self.outport={1:list()}
        self.port={1:'out'}
        return

    def AcpProgress(self,datadict):
        if type(self.value)!=list:out=[self.value]
        else:out=self.value
        for kturple in datadict.keys():
            if 'REQ' in kturple:
                reqlist=datadict[kturple]
        outdict=dict()
        for aroid in reqlist:
            outdict[aroid]=[out]
        return {(self.AcpID,1):outdict}
    pass

class AcpNorm(Acp):
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={2:[]}
        self.port={1:'in vec',2:'out norm'}
        return

    def AcpProgress(self,datadict):
        vec_dict=datadict[self.inport[1]]
        out_dict=dict()
        for aroid,vec_list in vec_dict.items():
            out_dict[aroid]=list()
            for vec in vec_list:
                vec=np.array(vec)
                out_dict[aroid].append([np.linalg.norm(vec)])
        return {(self.AcpID,2):out_dict}
    pass

class AcpSum(Acp):
    ''' Addition: NONE.

            Inport: 1.in.

            Outport: 2.out;'''
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={2:list()}
        self.port={1:'in',2:'out'}
        return

    def AcpProgress(self,datadict):
        in_dict=datadict[self.inport[1]]
        out_dict=dict()
        for aroid,dlist in in_dict.items():
            # darr=np.array(dlist)
            out_dict[aroid]=[np.sum(dlist,axis=0).tolist()]
        return {(self.AcpID,2):out_dict}
    pass

class AcpCross(Acp):
    def __init__(self):
        super().__init__()
        self.inport={1:None,2:None}
        self.outport={0:[]}
        self.port={0:'out r',1:'in a',2:'in b'}
        return

    def AcpProgress(self,datadict):
        v1dict=datadict[self.inport[1]]
        v2dict=datadict[self.inport[2]]
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
        return {(self.AcpID,0):output_dict}
    pass
