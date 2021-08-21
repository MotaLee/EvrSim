import numpy
inf=numpy.inf
from core import esc
from mod.AroCore import AroField

# Aro class defination;
class MassPoint(esc.Aro):
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

class RigidBody(esc.Aro):
    def __init__(self):
        super().__init__()
        self.mass=0
        self.position=[0,0,0]
        self.center=[0,0,0]
        self.velocity=[0,0,0]
        self.agl_v=[0,0,0]
        self.force=[0,0,0]
        self.moment=[0,0,0]
        self.LCS=[[1,0,0],[0,1,0],[0,0,1]]
        self.inertia=[0,0,0]
        self.size=[1,1,1]
        return
    pass

class PointForce(esc.Aro):
    def __init__(self):
        super().__init__()
        self.adp='mod.AroCore.AdpArrow'
        self.position=[0,0,0]
        self.value=[0,0,0]
        self.color=[1,0,0,1]
        self.tag='force'
        return
    pass

class Moment(esc.Aro):
    def __init__(self):
        super().__init__()
        self.adp='DpMoment'
        self.position=[0,0,0]
        self.value=[0,0,0]
        self.tag='moment'
        return
    pass

class Constraint(esc.Aro):
    def __init__(self):
        super().__init__()
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
        self.addFlag(enum='style')
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
        self.refs=-1
        self.connections=-1
        self.addFlag(link=['refs','connections'],hide=['refs','connections'])
        return

    def onAdd(self):
        from core import ESC
        r=ESC.addAro(AroClass=ComboNode,AroName='Refs',parent=self.AroID)
        c=ESC.addAro(AroClass=ComboNode,AroName='Connections',parent=self.AroID)
        self.children=[r.AroID,c.AroID]
        self.refs=r.AroID
        self.connections=c.AroID
        ESC.updateLink(self)
        return
    pass
class ComboNode(esc.Aro):
    def __init__(self):
        super().__init__()
        self.icon={
            'normal':'res\img\Icon_model.png',
            'unfold':'res\img\Icon_model.png'}
        self.addFlag(lock='AroName',hide='icon')
        return
    pass

class Beam2D(RigidBody):
    def __init__(self):
        super().__init__()
        self.adp='AdpBeam2D'
        self.radius=.2
        self.length=2
        self.color=[1,0,0]
        self.ptf=[1,0,0]
        self.pts=[-1,0,0]
        return
    pass

class RefPoint(esc.Aro):
    def __init__(self):
        super().__init__()
        self.adp='AdpRefPoint'
        self.position=[0,0,0]
        self.color=[1,0,0]
        self.ref=-1
        self.refattr=''
        self.addFlag(link='ref')
        return
    pass
