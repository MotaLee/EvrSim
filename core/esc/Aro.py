import numpy
import mod,app
inf=numpy.inf
class Aro(object):
    ''' Core Aro class.
        '''
    def __init__(self):
        self._flag={
            'unsave':['_flag','_ptr'],
            'hide':['_flag','_ptr','_input','_output'],
            'lock':['adp','AroClass','AroID','AbbrClass'],
            'long':['desc'],
            'link':['parent','children'],
            'enum':[]}
        self._ptr=dict()
        self._input=[]
        self._output=[]
        # Preset Arove;
        self.AroID=0
        self.AbbrClass=type(self).__name__
        self.AroClass=self.__module__+'.'+self.AbbrClass
        self.adp=''
        self.parent=-1    # AroID;
        self.children=list()    # AroID list;
        self.AroName=''
        self.desc=''
        self.enable=True
        self.visible=True
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

    def addFlag(self,**argkw):
        ''' Add flag of Arove using argkw=Arove | [Arove..].
            Call after Arove defination.
            * Argkw unsave: Not save to map;
            * Argkw hide: Not display in editor;
            * Argkw uneditble: Uneditable in editor;
            * Argkw long: Dislay as long in editor;
            * Argkw enum: As enum;
            * Argkw auto: As auto;
            '''
        for k,vl in argkw.items():
            if not isinstance(vl,list):vl=[vl]
            vchk=[v for v in vl
                if hasattr(self,v) and v not in self._flag[k]]
            self._flag[k]+=vchk

        return
    pass

class AroSpace(Aro):
    '''Addition Arove: space_set;'''
    def __init__(self):
        super().__init__()
        self.space_list=list()
        return
    pass

class AroGroup(Aro):
    '''Addition Arove: link_dict;'''
    def __init__(self):
        super().__init__()
        self.group_dict=dict()  # {AroID:AroID list}
        return
    pass
