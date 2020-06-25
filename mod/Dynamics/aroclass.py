import mod.AroCore
# Aro class defination;
class MassPoint(mod.AroCore.Aro):
    '''
    Addition Arove:
        *position, velocity, force, mass;
    '''
    def __init__(self):
        super().__init__()
        self.position=[0,0,0]
        self.velocity=[0,0,0]
        self.force=[0,0,0]
        self.mass=0
        return
    pass
