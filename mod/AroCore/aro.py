from core import ESC

class AroTree(ESC.Aro):
    ''' Aro with tree structure.

        Addition Arove: parent, children;'''
    def __init__(self):
        super().__init__()
        self._Arove_flag['invisible']+=['parent','children']
        self.parent=None    # AroID;
        self.children=list()    # AroID list;
        return
    pass

class AroTargets(ESC.Aro):
    ''' Aro with targets.

        Addition Arove: targets;'''
    def __init__(self):
        super().__init__()
        self._Arove_flag['target'].append('targets')
        self.targets=list()     # AroID list;
        return
    pass

class AroPoint(ESC.Aro):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpPoint'
        self.position=[0,0,0]
        return
    pass

class AroImage(ESC.Aro):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpImage'
        self.position=[0,0,0]
        self.size=[0,0]
        self.image=''
        return
    pass

class AroSpace(AroTree):
    '''Addition Arove: space_set;'''
    def __init__(self):
        super().__init__()
        self._Arove_flag['invisible'].append('space_list')
        self.space_list=list()
        return
    pass

class AroGroup(AroTree):
    '''Addition Arove: link_dict;'''
    def __init__(self):
        super().__init__()
        self._Arove_flag['invisible'].append('group_dict')
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

class AroField(AroPoint):
    def __init__(self):
        super().__init__()
        self.shape=None     # None for all space;
        self.CST='XYZ'  # Emum for XYZ, Rtp, Rtz;
        self.function=[0,0,0]
        return
    pass

class AroLight(AroPoint):
    def __init__(self):
        super().__init__()
        self.type=1     # 1 for 'point';
        self.strength=.5
        self.color=[1,1,1]
        return

    def getLightPara(self):
        out={
            'pos':self.position,
            'type':self.type,
            'strength':self.strength,
            'color':self.color}
        return out
    pass
