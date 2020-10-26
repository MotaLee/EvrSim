import glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esgl
ADP=esgl.AroDrawPart
class DpRigidGroup(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        self.updateDP(self.Aro)
        return

    def updateDP(self,aro):
        self.Aro=aro
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
        self.update_data=True
        # print(self.Aro.AroName,self.VA)
        return
    pass

class DpMoment(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_TRIANGLES
        self.fix_size=True
        self.VA,self.EA=esgl.importDPM('mod/Dynamics/res/moment.obj')
        self.updateDP(self.Aro)
        return

    def updateDP(self,aro):
        self.Aro=aro
        v=list(self.Aro.position)
        r1=glm.translate(glm.mat4(1.0),v)
        r2=esgl.rotateToVec((0,1,0),self.Aro.value)
        self.trans=r2*r1
        return
    pass

class DpConstraint(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        self.fix_size=True
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
        self.updateDP(self.Aro)
        return

    def updateDP(self,aro):
        self.Aro=aro
        v_p=list(self.Aro.position)
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        return
    pass

class DpGround(ADP):
    def __init__(self,aroid):
        super().__init__(aroid)
        self.gl_type=gl.GL_LINES
        ps=0.2

        VA=np.array([
            [0,0,0,   0.5,0.5,0.5,1],
            [0,-1*ps,ps,     0.5,0.5,0.5,1],
            [ps,-1*ps,ps/-1,     0.5,0.5,0.5,1],
            [ps/-1,-1*ps,ps/-1,     0.5,0.5,0.5,1]],dtype=np.float32)
        self.VA=VA
        self.EA=np.array([[0,1],[0,2],[0,3],[1,3],[2,3],[1,2]],dtype=np.uint32)
        self.updateDP(self.Aro)
        return

    def updateDP(self,aro):
        self.Aro=aro
        v_p=list(self.Aro.position)
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        return
    pass
