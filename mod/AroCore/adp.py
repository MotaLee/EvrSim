import glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esui
from core import esgl
ADP=esgl.AroDrawPart
class AdpPoint(ADP):
    def __init__(self,aro):
        super().__init__(aro=aro)
        self.gl_type=gl.GL_LINES
        self.fix_size=True
        self.fix_orientation=True
        ps=0.1

        VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        VA=np.tile(VA,(4,1))
        VA[0][0]+=ps
        VA[1][0]-=ps
        VA[2][1]+=ps
        VA[3][1]-=ps
        self.VA=VA
        self.EA=np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],dtype=np.uint32)
        v_p=list(self.Aro.position)
        # v_p=glm.vec3()
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        return
    pass
