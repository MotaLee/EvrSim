import _pybullet as pb
import numpy as np
from core import ESC,esgl
from .aro import RigidBody,ForceField
class BulletEngine(ESC.AcpExecutor):
    def __init__(self):
        super().__init__()
        # self.Client = pb.connect(pb.GUI)    # or p.DIRECT for non-graphical version
        self.Client = pb.connect(pb.DIRECT)    # or p.DIRECT for non-graphical version
        self.arobodys=dict()
        self.fields=dict()
        pb.setRealTimeSimulation(0)
        pb.setTimeStep(1/esgl.FPS)
        return

    def execute(self):
        force_allfield=np.array([0,0,0])
        for aro in ESC.getFullMap():
            if isinstance(aro,RigidBody):
                if aro.AroID not in self.arobodys:self.createBody(aro)
            elif isinstance(aro,ForceField):
                if aro.AroID not in self.fields:
                    if aro.shape is None:
                        force_allfield+=np.array(aro.function)
        for aroid,bodyid in self.arobodys.items():
            pb.applyExternalForce(objectUniqueId=bodyid,
                linkIndex=-1,
                forceObj=force_allfield.tolist(),
                posObj=ESC.getAro(aroid).position,
                flags=pb.WORLD_FRAME)
        pb.stepSimulation()
        for aroid,bodyid in self.arobodys.items():
            pos,orn=pb.getBasePositionAndOrientation(bodyid)
            lcs=pb.getMatrixFromQuaternion(orn)
            lcs=[[lcs[0],lcs[3],lcs[6]],
                [lcs[1],lcs[4],lcs[7]],
                [lcs[2],lcs[5],lcs[8]]]
            lv,av=pb.getBaseVelocity(bodyid)
            ESC.setAro(ESC.getAro(aroid),{
                'position':list(pos),
                'LCS':lcs,
                'velocity':list(lv),
                'agl_v':list(av)})
            pass
        return

    def resetSimulation(self):
        self.arobodys=dict()
        self.fields=dict()
        pb.resetSimulation()
        return

    def createBody(self,aro,cubic=True):
        shift=[0,0,0]
        adplist=esgl.DICT_ADP[aro.AroID]
        if len(adplist)==1:
            size=esgl.getAABB(adplist[0],False)
            scale=getattr(aro,'size',[1,1,1])
            if len(scale)==2:scale+=[scale[0]]
            pc=np.array([(size[0]+size[1])/2,
                (size[2]+size[3])/2,
                (size[4]+size[5])/2])
            p=np.array(aro.position)
            absize=[abs(t) for t in size]
            halfsize=[
                scale[0]*(absize[0]+absize[1])/2,
                scale[1]*(absize[2]+absize[3])/2,
                scale[2]*(absize[4]+absize[5])/2]
            qua=esgl.getQuaternionFormCS(aro.LCS)
            qua=qua[1:]+[qua[0]]
            if cubic:
                # vid=pb.createVisualShape(shapeType=pb.GEOM_BOX,
                #     visualFramePosition=shift,
                #     halfExtents=halfsize)
                cid=pb.createCollisionShape(shapeType=pb.GEOM_BOX,
                    collisionFramePosition=shift,
                    halfExtents=halfsize)
                if aro.mass==np.inf:mass=0
                else:mass=aro.mass
                bodyid=pb.createMultiBody(baseMass=mass,
                    baseInertialFramePosition=shift,
                    baseOrientation=qua,
                    baseCollisionShapeIndex=cid,
                    # baseVisualShapeIndex=vid,
                    basePosition=p+pc)
                pb.resetBaseVelocity(objectUniqueId=bodyid,
                    linearVelocity=aro.velocity,
                    angularVelocity=aro.agl_v)
                self.arobodys[aro.AroID]=bodyid
        else:
            for adp in adplist:pass
        return bodyid
    pass
