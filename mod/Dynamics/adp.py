import numpy as np
# import _glm as glm
from core import esgl
from mod.AroCore import AdpBody
class AdpBC(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid)
        # self.addMesh(
        #     draw_type=esgl.DT_LINE,
        #     layout=[esgl.VtxLayout('color')])
        self.updateAdp()
        return

    def updateAdp(self):
        # self.Aro=ESC.getAro(self.name)
        # elm_dict=dict()
        # VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        # EA=np.array([0,0],dtype=np.uint32)
        # for srcid in self.Aro.group_dict.keys():
        #     srcaro=ESC.getAro(srcid)
        #     vtx=np.array([srcaro.position+[1,1,1,1]],dtype=np.float32)
        #     self.VA=np.vstack((self.VA,vtx))
        #     elm_dict[srcid]=len(self.VA)-1
        # for srcid,tar_list in self.Aro.group_dict.items():
        #     for tarid in tar_list:
        #         tea=np.array([elm_dict[srcid],elm_dict[tarid]],dtype=np.uint32)
        #         self.EA=np.hstack((self.EA,tea))
        # self.flag_update=True
        return
    pass

class AdpMoment(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.list_mesh=esgl.import3DFile('mod/Dynamics/res/moment.obj')
        self.updateAdp()
        return

    def updateAdp(self):
        super().updateAdp()
        r=esgl.rotateToVec((0,1,0),self.Aro.value)
        self.trans=r*self.trans
        return
    pass

class AdpConstraint(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        VA=np.array([
            [.1,.1,.1,1,1,1,1],
            [.1,-0.1,.1,1,1,1,1],
            [-0.1,.1,.1,1,1,1,1],
            [-0.1,-0.1,.1,1,1,1,1],
            [.1,.1,-0.1,1,1,1,1],
            [.1,-0.1,-0.1,1,1,1,1],
            [-0.1,.1,-0.1,1,1,1,1],
            [-0.1,-0.1,-0.1,1,1,1,1]],dtype=np.float32)
        EA=np.array([
            [0,1],[1,3],[3,2],[2,0],
            [4,5],[5,7],[7,6],[6,4]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return
    pass

class AdpGnd(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid)
        ps=0.2
        VA=np.array([
            [0,0,0,   0.5,0.5,0.5,1],
            [0,-1*ps,ps,     0.5,0.5,0.5,1],
            [ps,-1*ps,ps/-1,     0.5,0.5,0.5,1],
            [ps/-1,-1*ps,ps/-1,     0.5,0.5,0.5,1]],dtype=np.float32)
        EA=np.array([[0,1],[0,2],[0,3],[1,3],[2,3],[1,2]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return
    pass

class AdpRefPoint(esgl.AroDrawPart):
    def __init__(self, aroid):
        super().__init__(aroid)
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.dict_fix['orient']=True
        s=0.1
        n=0.01
        VA=np.array([
            [s-n,s-n,0],[s-n,n,0],[n,s-n,0],
            [-s+n,s-n,0],[-s+n,n,0],[-n,s-n,0],
            [-s+n,-s+n,0],[-s+n,-n,0],[-n,-s+n,0],
            [s-n,-s+n,0],[s-n,-n,0],[n,-s+n,0],
            ],dtype=np.float32)
        CA=np.array([self.Aro.color],dtype=np.float32)
        CA=np.tile(CA,(12,1))
        alpha=np.ones(12).astype(np.float32)
        VA=np.column_stack((VA,CA,alpha))
        EA=np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_TRI,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return
    pass

class AdpBeam2D(AdpBody):
    def __init__(self, aroid):
        super().__init__(aroid)
        aro=self.Aro
        vai,eai,f=esgl.genCircleArr(aro.radius)
        vao,eao,f=esgl.genCircleArr(aro.radius*2)
        VA=np.vstack((vai,vao))
        EA=np.vstack([eai,eao+len(vai)])
        CA=np.array([aro.color],dtype=np.float32)
        CA=np.tile(CA,(VA.shape[0],1))
        alpha=np.ones((VA.shape[0],1)).astype(np.float32)
        VA=np.hstack((VA,CA,alpha))

        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,edges=EA,
            trans=esgl.transMat(vec=aro.ptf))
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,edges=EA,
            trans=esgl.transMat(vec=aro.pts))

        var,e,f=esgl.genRectArr()

        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=esgl.stackColorArr(var,aro.color),
            edges=np.array([0,1,2,3],dtype=np.uint32),
            trans=esgl.transMat(option='scale',vec=[aro.length,aro.radius*4,1]))
        self.updateAdp()
        return

    def updateAdp(self):
        super().updateAdp()

        self.flag_update=True
        return
    pass
