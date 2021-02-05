import _glm as glm
import numpy as np
import OpenGL.GL as gl
from core import ESC,esgl
ADP=esgl.AroDrawPart
class DpRigidGroup(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        self.updateADP()
        self.dict_layout['color']=4
        return

    def updateADP(self):
        self.Aro=ESC.getAro(self.name)
        elm_dict=dict()
        self.VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        self.EA=np.array([0,0],dtype=np.uint32)
        for srcid in self.Aro.group_dict.keys():
            srcaro=ESC.getAro(srcid)
            vtx=np.array([srcaro.position+[1,1,1,1]],dtype=np.float32)
            self.VA=np.vstack((self.VA,vtx))
            elm_dict[srcid]=len(self.VA)-1
        for srcid,tar_list in self.Aro.group_dict.items():
            for tarid in tar_list:
                tea=np.array([elm_dict[srcid],elm_dict[tarid]],dtype=np.uint32)
                self.EA=np.hstack((self.EA,tea))
        self._is_modified=True
        # print(self.Aro.AroName,self.VA)
        return
    pass

class DpMoment(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_TRIANGLES
        self.dict_layout.update({'color':4,'normal':3})
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.VA,self.EA=esgl.importDPM('mod/Dynamics/res/moment.obj')
        norm_mat=esgl.getPtNormal(self.VA,self.EA)
        self.VA=np.hstack((self.VA,norm_mat))
        self.updateADP()
        return

    def updateADP(self):
        super().updateADP()
        r=esgl.rotateToVec((0,1,0),self.Aro.value)
        self.trans=r*self.trans
        return
    pass

class DpConstraint(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        self.dict_layout['color']=4
        self.dict_fix['fix']=True
        self.dict_fix['size']=True
        self.VA=np.array([
            [.1,.1,.1,1,1,1,1],
            [.1,-0.1,.1,1,1,1,1],
            [-0.1,.1,.1,1,1,1,1],
            [-0.1,-0.1,.1,1,1,1,1],
            [.1,.1,-0.1,1,1,1,1],
            [.1,-0.1,-0.1,1,1,1,1],
            [-0.1,.1,-0.1,1,1,1,1],
            [-0.1,-0.1,-0.1,1,1,1,1]],dtype=np.float32)
        self.EA=np.array([
            [0,1],[1,3],[3,2],[2,0],
            [4,5],[5,7],[7,6],[6,4]],dtype=np.uint32)
        self.updateADP()
        return
    pass

class DpGround(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        self.dict_layout['color']=4
        ps=0.2

        VA=np.array([
            [0,0,0,   0.5,0.5,0.5,1],
            [0,-1*ps,ps,     0.5,0.5,0.5,1],
            [ps,-1*ps,ps/-1,     0.5,0.5,0.5,1],
            [ps/-1,-1*ps,ps/-1,     0.5,0.5,0.5,1]],dtype=np.float32)
        self.VA=VA
        self.EA=np.array([[0,1],[0,2],[0,3],[1,3],[2,3],[1,2]],dtype=np.uint32)
        self.updateADP()
        return
    pass
