from core import ESC
# Aro class defination;
class Aro(object):
    ''' Core Aro class;'''
    def __init__(self):
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

    def onSet(self,arove={}):
        ''' This method will be called in ESC.setAro'''
        new_arove=dict(arove)
        for k,v in arove.items():
            if k not in self.__dict__:
                del new_arove[k]
        self.__dict__.update(new_arove)
        return

    def onDel(self):
        ''' This method will be called in ESC.delAro'''
        return
    pass

class AroTree(Aro):
    ''' Aro with tree structure.

        Addition Arove: parent, children;'''
    def __init__(self):
        super().__init__()
        self.parent=None    # AroID;
        self.children=list()    # AroID list;
        return
    pass

class AroTarget(Aro):
    ''' Aro with targets.

        Addition Arove: targets;'''
    def __init__(self):
        super().__init__()
        self.targets=list()     # AroID list;
        return
    pass

class AroPoint(Aro):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpPoint'
        self.position=[0,0,0]
        return
    pass

class AroSpace(AroTree):
    '''Addition Arove: space_set;'''
    def __init__(self):
        super().__init__()
        self.data_type.update({'space_list':'AroID list'})
        self.space_list=list()
        return
    pass

class AroGroup(AroTree):
    '''Addition Arove: link_dict;'''
    def __init__(self):
        super().__init__()
        self.group_dict=dict()  # {AroID:AroID list}
        return

    def onSet(self,arove={}):
        super().onSet(arove)
        new_dict=dict()
        existed_list=list()
        for k,v_list in self.group_dict.items():
            if k in existed_list: k_aro=True
            else:k_aro=ESC.getAro(k)
            if k_aro is not None:
                existed_list.append(k)
                new_dict[k]=list()
                for v in v_list:
                    if v in existed_list: v_aro=True
                    else:v_aro=ESC.getAro(v)
                    if v_aro is not None:
                        new_dict[k].append(v)
        self.group_dict=new_dict
        self.children=list(self.group_dict.keys())
        return
    pass
