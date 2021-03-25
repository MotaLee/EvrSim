import numpy
inf=numpy.inf
from core import EvrSimCore
from mod.AroCore import AroTargets,AroField

# Aro class defination;
class MassPoint(EvrSimCore.Aro):
    ''' Addition Arove: velocity, force, mass;'''
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpPoint'
        self.position=[0,0,0]
        self.velocity=[0,0,0]
        self.force=[0,0,0]
        self.mass=0
        return
    pass

class RigidBody(EvrSimCore.AroNode):
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

class Constraint(EvrSimCore.Aro):
    def __init__(self):
        super().__init__()
        self._flag['target']+=['master','servant','m_target','s_target']
        self.adp='AdpConstraint'
        self.position=[0,0,0]
        self.UXYZ=[0,0,0]
        self.RXYZ=[0,0,1]
        self.master=0
        self.servant=0
        self.m_target=0
        self.s_target=0
        return
    pass

class Ground(RigidBody):
    def __init__(self):
        super().__init__()
        self.addAroveFlag(enum='style')
        self.adp='AdpGnd'
        self.mass=inf
        self.inertia=[inf,inf,inf]
        self.style='point' # Enum for point/plane;
        return

    def onSet(self):
        if self.style=='point':
            self.adp='AdpGnd'
        elif self.style=='plane':
            self.adp='mod.AroCore.AdpPlane'
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
        return
    pass

class BodyCombo(RigidBody):
    def __init__(self):
        RigidBody.__init__(self)
        self.adp='AdpBC'
        return

    def onAdd(self):
        from core import ESC
        r=ESC.addAro(AroClass=ComboNode,AroName='Refs',parent=self.AroID)
        c=ESC.addAro(AroClass=ComboNode,AroName='Connections',parent=self.AroID)
        self.children=[r.AroID,c.AroID]
        return
    pass
class ComboNode(EvrSimCore.AroNode):
    def __init__(self):
        super().__init__()
        self.icon={
            'normal':'res\img\Icon_model.png',
            'unfold':'res\img\Icon_model.png'}
        self.addAroveFlag(uneditable='AroName',invisible='icon')
        return
    pass
