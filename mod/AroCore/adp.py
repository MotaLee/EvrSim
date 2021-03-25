import _glm as glm
import numpy as np
import OpenGL.GL as gl
from core import ESC,esgl
class AdpPoint(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.dict_fix['orient']=True
        ps=0.1
        VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        VA=np.tile(VA,(4,1))
        VA[0][0]+=ps
        VA[1][0]-=ps
        VA[2][1]+=ps
        VA[3][1]-=ps
        EA=np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return
    pass

class AdpPlane(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        ps=1
        VA=np.array([[0,0,0,.5,.5,.5,1]],dtype=np.float32)
        VA=np.tile(VA,(4,1))
        VA[0][0]+=ps
        VA[0][2]+=ps
        VA[1][0]-=ps
        VA[1][2]+=ps
        VA[2][0]-=ps
        VA[2][2]-=ps
        VA[3][0]+=ps
        VA[3][2]-=ps
        EA=np.array([[0,1,2,3]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_QUAD,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return

    def updateAdp(self):
        super().updateAdp()
        dcs=[[1,0,0],[0,1,0],[0,0,1]]
        lcs=getattr(self.Aro,'LCS',dcs)
        self.trans=esgl.rotateToCS(self.trans,dcs,lcs)
        size=getattr(self.Aro,'size',[1,1])
        self.trans=glm.scale(self.trans,[size[0],1,size[1]])
        return
    pass

class AdpArrow(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.value=getattr(self.Aro,'value',[0,1,0])
        self.color=getattr(self.Aro,'color',[1,1,1,1])
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        ps=0.05
        length=np.linalg.norm(self.value)
        ca=np.array([self.color],dtype=np.float32)
        ca=np.tile(ca,(5,1))
        VA=np.array([
            [0,length,0],
            [0,length-2*ps,ps],
            [ps,length-2*ps,-1*ps],
            [-1*ps,length-2*ps,-1*ps],
            [0,0,0]],dtype=np.float32)
        VA=np.hstack((VA,ca))
        EA=np.array([[0,4],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return

    def updateAdp(self):
        super().updateAdp()
        self.trans=self.trans*esgl.rotateToVec(
            glm.vec3([0,1,0]),glm.vec3(self.value))
        return
    pass

class AdpImage(esgl.AroDrawPart):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.texture=self.Aro.image
        w=self.Aro.size[0]/100
        h=self.Aro.size[1]/-100
        VA=np.array([
            [0,0,0,0,0],
            [w,0,0,1,0],
            [w,h,0,1,1],
            [0,h,0,0,1]
            ],dtype=np.float32)
        EA=np.array([[0,1,2,3]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_QUAD,
            layout=[esgl.VtxLayout('tex')],
            vertices=VA,faces=EA,
            texture=self.Aro.image)
        self.updateAdp()
        return
    pass

class AdpBody(esgl.AroDrawPart):
    def updateAdp(self):
        self.Aro=ESC.getAro(self.name)
        v_p=list(self.Aro.position)
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        dcs=[[1,0,0],[0,1,0],[0,0,1]]
        lcs=getattr(self.Aro,'LCS',dcs)
        self.trans=esgl.rotateToCS(self.trans,dcs,lcs)
        v_s=getattr(self.Aro,'size',[1,1,1])
        self.trans=glm.scale(self.trans,v_s)
        return
    pass

class AdpCube(AdpBody):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        VA=np.array([
            [-.5,.5,-.5,.5,.5,.5,1],
            [.5,.5,-.5,.5,.5,.5,1],
            [.5,.5,.5,.5,.5,.5,1],
            [-.5,.5,.5,.5,.5,.5,1],
            [-.5,-.5,-.5,.5,.5,.5,1],
            [.5,-.5,-.5,.5,.5,.5,1],
            [.5,-.5,.5,.5,.5,.5,1],
            [-.5,-.5,.5,.5,.5,.5,1]],dtype=np.float32)
        EA=np.array([
            [0,1,2,3],[1,5,6,2],[3,2,6,7],
            [0,3,7,4],[1,0,4,5],[7,6,5,4]],dtype=np.uint32)
        norm_mat=esgl.getPtNormal(VA,EA)
        VA=np.hstack((VA,norm_mat))
        self.addMesh(
            draw_type=esgl.DT_QUAD,
            layout=[esgl.VtxLayout('color'),esgl.VtxLayout('normal')],
            vertices=VA,faces=EA)
        self.updateAdp()
        return
    pass

class AdpCS(AdpBody):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        VA=np.array([
            [0,0,0,1,1,1,1],
            [1,0,0,1,0,0,1],
            [0,1,0,0,1,0,1],
            [0,0,1,0,0,1,1]],dtype=np.float32)
        EA=np.array([
            [0,1],[0,2],[0,3]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        self.updateAdp()
    pass
