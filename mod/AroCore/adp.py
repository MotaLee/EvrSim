import _glm as glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esui
from core import esgl
ADP=esgl.AroDrawPart
class AdpPoint(ADP):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.gl_type=gl.GL_LINES
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.dict_fix['orient']=True
        self.dict_layout['color']=4
        ps=0.1

        VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        VA=np.tile(VA,(4,1))
        VA[0][0]+=ps
        VA[1][0]-=ps
        VA[2][1]+=ps
        VA[3][1]-=ps
        self.VA=VA
        self.EA=np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],dtype=np.uint32)
        self.updateADP()
        return
    pass

class AdpPlane(ADP):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.gl_type=gl.GL_QUADS
        self.dict_layout['color']=4
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
        self.VA=VA
        self.EA=np.array([[0,1,2,3]],dtype=np.uint32)
        self.updateADP()
        return

    def updateADP(self):
        super().updateADP()
        size=getattr(self.Aro,'size',[1,1])
        self.trans=glm.scale(self.trans,[size[0],1,size[1]])
        'todo: rotate'
        return
    pass

class AdpArrow(ADP):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.gl_type=gl.GL_LINES
        self.value=getattr(self.Aro,'value',[0,1,0])
        self.color=getattr(self.Aro,'color',[1,1,1,1])
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.dict_layout['color']=4
        length=np.linalg.norm(self.value)
        ps=0.05

        ca=np.array([self.color],dtype=np.float32)
        ca=np.tile(ca,(5,1))
        VA=np.array([
            [0,length,0],
            [0,length-2*ps,ps],
            [ps,length-2*ps,-1*ps],
            [-1*ps,length-2*ps,-1*ps],
            [0,0,0]],dtype=np.float32)
        self.VA=np.hstack((VA,ca))
        self.EA=np.array([[0,4],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],dtype=np.uint32)
        self.updateADP()
        return

    def updateADP(self):
        super().updateADP()
        self.trans=self.trans*esgl.rotateToVec(glm.vec3([0,1,0]),glm.vec3(self.value))
        return
    pass

class AdpImage(ADP):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.gl_type=gl.GL_TRIANGLES
        self.texture=self.Aro.image
        w=self.Aro.size[0]/100
        h=self.Aro.size[1]/-100
        self.dict_layout['tex']=2
        self.VA=np.array([
            [0,0,0,0,0],
            [w,0,0,1,0],
            [0,h,0,0,1],
            [w,h,0,1,1]],dtype=np.float32)
        self.EA=np.array([[0,1,2],[1,2,3]],dtype=np.uint32)
        self.updateADP()
        return
    pass

class AdpBody(ADP):
    def updateADP(self):
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
        self.gl_type=gl.GL_QUADS
        self.dict_layout.update({'color':4,'normal':3})
        self.VA=np.array([
            [-.5,.5,-.5,.5,.5,.5,1],
            [.5,.5,-.5,.5,.5,.5,1],
            [.5,.5,.5,.5,.5,.5,1],
            [-.5,.5,.5,.5,.5,.5,1],
            [-.5,-.5,-.5,.5,.5,.5,1],
            [.5,-.5,-.5,.5,.5,.5,1],
            [.5,-.5,.5,.5,.5,.5,1],
            [-.5,-.5,.5,.5,.5,.5,1]],dtype=np.float32)
        self.EA=np.array([
            [0,1,2,3],[1,5,6,2],[3,2,6,7],
            [0,3,7,4],[1,0,4,5],[7,6,5,4]],dtype=np.uint32)
        norm_mat=esgl.getPtNormal(self.VA,self.EA)
        self.VA=np.hstack((self.VA,norm_mat))
        self.updateADP()
        return
    pass

class AdpCS(AdpBody):
    def __init__(self,aroid):
        super().__init__(aroid=aroid)
        self.gl_type=gl.GL_LINES
        self.dict_layout['color']=4
        self.VA=np.array([
            [0,0,0,1,1,1,1],
            [1,0,0,1,0,0,1],
            [0,1,0,0,1,0,1],
            [0,0,1,0,0,1,1]],dtype=np.float32)
        self.EA=np.array([
            [0,1],[0,2],[0,3]],dtype=np.uint32)
        self.updateADP()
    pass
