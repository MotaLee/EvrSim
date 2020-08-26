from mod.AroCore import Aro,AroPoint,AroGroup,AroTargets
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
        self.MCP=[0,0,0]    # Mass center point;
        self.mass=0
        self.position=[0,0,0]
        self.velocity=[0,0,0]
        self.agl_v=[0,0,0]
        self.force=[0,0,0]
        self.moment=[0,0,0]
        return

    pass

class PointForce(AroTargets):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpArrow'
        self.position=[0,0,0]
        self.value=[0,0,0]
        self.color=[1,0,0,1]
        self.tag='force'
        return
    pass

class Moment(AroTargets):
    def __init__(self):
        super().__init__()
        self.adp='DpMoment'
        self.position=[0,0,0]
        self.value=[0,0,0]
        self.tag='moment'
        return
    pass

class AxisConstraint(AroTargets):
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
