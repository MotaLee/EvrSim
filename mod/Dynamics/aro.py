from mod.AroCore import Aro,AroPoint,AroGroup,AroTargets,AroField
from mod.Dynamics import DpRigidGroup
# Aro class defination;
class MassPoint(AroPoint):
    ''' Addition Arove:

        velocity, force, mass;'''
    def __init__(self):
        super().__init__()
        self.velocity=[0,0,0]
        self.force=[0,0,0]
        self.mass=0
        return
    pass

class RigidBody(Aro):
    def __init__(self):
        super().__init__()
        self.mass=0
        self.position=[0,0,0]   # Also Mass center;
        self.velocity=[0,0,0]
        self.agl_v=[0,0,0]
        self.force=[0,0,0]
        self.moment=[0,0,0]
        self.LCS=[[1,0,0],[0,1,0],[0,0,1]]
        self.inertia=[0,0,0]
        self.size=[1,1,1]
        return
    pass

class RigidGroup(AroGroup,RigidBody):
    def __init__(self):
        AroGroup.__init__(self)
        RigidBody.__init__(self)
        self.adp='DpRigidGroup'

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

class Constraint(Aro):
    def __init__(self):
        super().__init__()
        self._Arove_flag['target']+=['master','servant','m_target','s_target']
        self.adp='DpConstraint'
        self.position=[0,0,0]
        self.UXYZ=[0,0,0]
        self.RXYZ=[0,0,1]
        self.master=0
        self.servant=0
        self.m_target=0
        self.s_target=0
        return
    pass

class Ground(Aro):
    def __init__(self):
        super().__init__()
        self.adp='DpGround'
        self.position=[0,0,0]
        self.mass='inf'
        self.inertia=['inf','inf','inf']
        self.velocity=[0,0,0]
        self.agl_v=[0,0,0]
        return
    pass

class PlaneGnd(Ground,RigidBody):
    def __init__(self):
        # super().__init__()
        RigidBody.__init__(self)
        Ground.__init__(self)
        self.adp='mod.AroCore.AdpPlane'
        self.size=[5,5]
        return
    pass

class ForceField(AroField):
    def __init__(self):
        super().__init__()
        # self.value=[0,0,1]
        return
    pass

class MassCube(RigidBody):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpCube'
        # self.adp=['mod.AroCore.AdpCube','mod.AroCore.AdpCS']
        return
    pass
