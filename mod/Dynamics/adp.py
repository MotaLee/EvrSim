import glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esgl
ADP=esgl.AroDrawPart
class DpRigidGroup(ADP):
    def __init__(self,aro):
        super().__init__(aro)
        self.gl_type=gl.GL_LINES
        VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        EA=np.array([0,0],dtype=np.uint32)

        elm_dict=dict()
        for srcid in self.Aro.group_dict.keys():
            srcaro=ESC.getAro(srcid)
            vtx=np.array([srcaro.position+[1,1,1,1]],dtype=np.float32)
            VA=np.vstack((VA,vtx))
            elm_dict[srcid]=len(VA)-1
        for srcid,tar_list in self.Aro.group_dict.items():
            for tarid in tar_list:
                tea=np.array([elm_dict[srcid],elm_dict[tarid]],dtype=np.uint32)
                EA=np.hstack((EA,tea))

        self.VA=VA
        self.EA=EA
        return
    pass

class DpMoment(ADP):
    def __init__(self,aro):
        super().__init__(aro)
        self.gl_type=gl.GL_TRIANGLES
        self.fix_size=True
        self.VA,self.EA=esgl.importDPM('mod/Dynamics/DPM/moment.obj')
        v=list(self.Aro.position)
        r1=glm.translate(glm.mat4(1.0),v)
        r2=esgl.rotateToVec((0,1,0),self.Aro.value)
        self.trans=r2*r1
        return
    pass

class DpAxisConstraint(ADP):
    pass

class DpGround(ADP):
    def __init__(self,aro):
        super().__init__(aro)
        self.gl_type=gl.GL_TRIANGLES
        ps=0.2

        VA=np.array([
            [0,0,0,   0.5,0.5,0.5,1],
            [0,-1*ps,ps,     0.5,0.5,0.5,1],
            [ps,-1*ps,ps/-1,     0.5,0.5,0.5,1],
            [ps/-1,-1*ps,ps/-1,     0.5,0.5,0.5,1]],dtype=np.float32)
        self.VA=VA
        self.EA=np.array([[0,1,2],[0,2,3],[0,1,3],[1,2,3]],dtype=np.uint32)
        v_p=list(self.Aro.position)
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        return
    pass
