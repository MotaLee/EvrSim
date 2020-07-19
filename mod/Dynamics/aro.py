from mod.AroCore import Aro,AroPoint,AroGroup,AroTarget
from mod.Dynamics import DpRigidGroup
# Aro class defination;
class MassPoint(AroPoint):
    ''' Addition Arove:
        position, velocity, force, mass;'''
    def __init__(self):
        super().__init__()
        self.velocity=[0,0,0]
        self.force=[0,0,0]
        self.mass=0
        return
    pass

class RigidGroup(AroGroup):
    def __init__(self):
        super().__init__()
        self.adp='DpRigidGroup'
        self.RP=None     # Reference point, target to AroID;
        self.force=[0,0,0]
        self.moment=[0,0,0]
        return

    pass

class PointForce(AroTarget):

    pass

class Moment(AroTarget):
    def __init__(self):
        super().__init__()
        self.adp='DpMoment'
        self.position=[0,0,0]
        self.value=[0,0,0]
        return
    pass

class AxisConstraint(AroTarget):
    def __init__(self):
        super().__init__()
        self.adp='DpAxisConstraint'
        self.axis=[1,0,0]

        return
    pass

class Ground(Aro):
    def __init__(self):
        super().__init__()
        self.adp='DpGround'
        self.position=[0,0,0]

        return
    pass
