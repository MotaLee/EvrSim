from core import ESC

class AroTargets(ESC.Aro):
    ''' Aro with targets.

        Addition Arove: targets;'''
    def __init__(self):
        super().__init__()
        self._flag['target'].append('targets')
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
