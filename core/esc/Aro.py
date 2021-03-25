import numpy as np
import mod,app
inf=np.inf
class Aro(object):
    ''' Core Aro class.
        '''
    def __init__(self):
        self._flag={
            'unsave':['_flag'],
            'invisible':['_flag','AroID'],
            'uneditable':['adp','AroClass'],
            'longdata':['desc'],
            'target':[],
            'enum':[]}
        # Preset Arove;
        self.AroID=0
        self.AroClass=self.__module__+'.'+type(self).__name__
        self.adp=''
        # User changeable Arove;
        self.AroName=''
        self.desc=''
        self.enable=True
        self.visable=True
        return

    def onAdd(self):
        ''' This method will be called in ESC.addAro'''
        return
    def onSet(self):
        ''' This method will be called in ESC.setAro'''
        return
    def onDel(self):
        ''' This method will be called in ESC.delAro'''
        return

    def addAroveFlag(self,**argkw):
        ''' Add flag of Arove using argkw=Arove | [Arove..].
            * Argkw unsave: Not save to map;
            * Argkw invisible: Not display in editor;
            * Argkw uneditble: Uneditable in editor;
            * Argkw longdata: Dislay as longdata in editor;
            * Argkw enum: As enum;
            '''
        for k,vl in argkw.items():
            if not isinstance(vl,list):vl=[vl]
            vchk=[v for v in vl
                if hasattr(self,v) and v not in self._flag[k]]
            self._flag[k]+=vchk

        return
    pass

class AroNode(Aro):
    ''' Aro node with tree structure.
        * Addition Arove: parent, children;'''
    def __init__(self):
        super().__init__()
        self.parent=-1    # AroID;
        self.children=list()    # AroID list;
        self.addAroveFlag(invisible=['parent','children'])
        return
    pass

class AroSpace(AroNode):
    '''Addition Arove: space_set;'''
    def __init__(self):
        super().__init__()
        self._flag['invisible'].append('space_list')
        self.space_list=list()
        return
    pass

class AroGroup(AroNode):
    '''Addition Arove: link_dict;'''
    def __init__(self):
        super().__init__()
        self._flag['invisible'].append('group_dict')
        self.group_dict=dict()  # {AroID:AroID list}
        return
    pass
