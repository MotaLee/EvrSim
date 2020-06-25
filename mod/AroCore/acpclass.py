import numpy as np
from core import ESC
# Acp class defination;
class Acp(object):
    'Arove calculation part;'
    def __init__(self):
        self.AcpID=0
        cn=str(type(self))
        self.AcpClass=cn[8:cn.find('>')-1]
        self.position=[0,0]
        self.fixIO=True
        self.inport=dict()   # {portid:(childAcpID,portid),...};
        self.outport=dict()  # {portid:[(ParentAcpID,portid),...],...};

        self.AcpName=''
        self.desc=''
        self.port=dict()   # {portid:'name',...};
        return

    def preProgress(self,datadict):
        ''' Generate requesting dict.

            Be called before ports checking;'''
        return {}

    def AcpProgress(self,datadict):
        ''' Calculate Acp.

            Be called after inports ready;'''
        return {}

    def postProgress(self,datadict):
        ''' Fill the requesting dict

            Be called after ports checking.

            Should be overrided by sub class;'''
        return {}
    pass

class AcpSelector(Acp):
    ''' Select Arove in last map snapshot.

        Addition: expression, item.

        Outport: output.

        Inport: None;'''
    def __init__(self):
        super().__init__()
        self.expression=''   # Selecting expression;
        self.item=''    # Arove item to select, empty for Aro;
        self.outport={1:list()}
        self.port={1:'out'}
        return

    def AcpProgress(self,datadict):
        'ESC.ARO_QUEUE[-1] needed.'
        for kt in datadict.keys():
            if 'REQ' in kt:
                reqlist=datadict[kt]
        arvdict=dict()
        for SELF_AROID in reqlist:
            selfdict={SELF_AROID:list()}
            for ARO in ESC.ARO_QUEUE[-1]:
                condi=eval(self.expression)
                if condi:
                    selfdict[SELF_AROID].append(ARO.__dict__[self.item])
            arvdict.update(selfdict)
        return {(self.AcpID,1):arvdict}
    pass

class AcpProvider(Acp):
    ''' Addition: expression, item.

        Outport: None.

        Inport: input;'''
    def __init__(self):
        super().__init__()
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
        for Aro in ESC.ARO_MAP:
            target=eval(self.expression.__str__()) and 'position' in Aro.__dict__
            if target: arolist.append(Aro.AroID)
        reqdict[datakey]=arolist
        return reqdict

    def postProgress(self,datadict):
        indict=datadict[self.inport[1]]
        reqlist=datadict[(self.AcpID,'REQ')]
        for aroid,itemvalue in indict.items():
            if aroid in reqlist:
                ESC.setArove(aroid,{self.item:itemvalue})
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
        out1=(self.AcpID,1)
        out2=(self.AcpID,2)
        ret={out1:{self.item:[self.step]},
            out2:{self.item:[self.current]}}
        return ret

    def iterate(self):
        self.current+=self.step
        return

    pass

class AcpPMTD(Acp):
    ''' PMTD Function. Accept single value list input.

        Addition: expression.

        Inport: a, b.

        Outport: output;'''
    def __init__(self):
        super().__init__()
        self.expression=''  # Use symbol a and b to do PMTD;
        self.inport={1:None,2:None}
        self.outport={3:[]}
        self.port={1:'in a',2:'in b',3:'out r'}
        return

    def AcpProgress(self,datadict):
        adict=datadict[self.inport[1]]
        bdict=datadict[self.inport[2]]
        out_dict=dict()
        a=np.array(list(adict.values()))
        b=np.array(list(bdict.values()))
        res=eval(self.expression,globals(),{'a':a,'b':b})
        if len(adict)>=len(bdict):tdict=adict
        else:tdict=bdict
        i=0
        for k in tdict:
            out_dict[k]=[res[i][0]]
            i+=1
        return {(self.AcpID,3):out_dict}
    pass

class AcpGroup(Acp):
    pass

class AcpBuffer(Acp):
    ''' Addition: NONE.

        Outport: output.

        Inport: input;'''
    def __init__(self):
        super().__init__()
        self.inport={1:None}
        self.outport={2:list()}
        self.port={1:'in',2:'out'}
        return
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
                vec3_dict[aroid]=[xlist[i],ydict[aroid][i],zdict[aroid][i]]

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
                xdict[aroid].append(vec3[0])
                ydict[aroid].append(vec3[1])
                zdict[aroid].append(vec3[2])
        return {(self.AcpID,2):xdict,(self.AcpID,3):ydict,(self.AcpID,4):zdict}
    pass
