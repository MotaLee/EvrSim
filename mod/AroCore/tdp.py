import glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esui
from core import esgl
TDP=esgl.ToolDrawPart
class TdpXyzAxis(TDP):
    def __init__(self,tool):
        super().__init__(tool)
        self.gl_type=gl.GL_LINES
        self.VA=np.array([
            [0,0,0,     1,0,0,1],
            [.5,0,0,    1,0,0,1],
            [0,0,0,     0,1,0,1],
            [0,.5,0,    0,1,0,1],
            [0,0,0,     0,0,1,1],
            [0,0,.5,    0,0,1,1]],
            dtype=np.float32)
        self.EA=np.array([0,1,2,3,4,5],dtype=np.uint32)
        return
    pass

class TdpGrid(TDP):
    # gap=0.5;
    def __init__(self,tool,panel):
        super().__init__(tool)
        self.gl_type=gl.GL_LINES
        self.EA=np.array([],dtype=np.uint32)
        self.VA=np.zeros([44,7],dtype=np.float32)
        for i in range(0,21,2):
            self.VA[i]=[-5/2,0,i/4-2.5,.5,.5,.5,1]
            self.VA[i+1]=[5/2,0,i/4-2.5,.5,.5,.5,1]
            self.VA[i+22]=[i/4-2.5,0,-5/2,.5,.5,.5,1]
            self.VA[i+23]=[i/4-2.5,0,5/2,.5,.5,.5,1]
        if panel=='xz':
            self.trans=glm.mat4(1.0)
        elif panel=='yz':
            self.trans=glm.rotate(glm.mat4(1),glm.radians(90),glm.vec3(0,0,1))
        elif panel=='xy':
            self.trans=glm.rotate(glm.mat4(1),glm.radians(90),glm.vec3(1,0,0))
        return
    pass

class TdpViewBall(TDP):
    def __init__(self,tool):
        super().__init__(tool)
        self.gl_type=gl.GL_LINES
        self.VA=np.array([
            [0,0,0,     1,0,0,1],
            [.5,0,0,    1,0,0,1],
            [0,0,0,     0,1,0,1],
            [0,.5,0,    0,1,0,1],
            [0,0,0,     0,0,1,1],
            [0,0,.5,    0,0,1,1]],
            dtype=np.float32)
        self.EA=np.array([[0,1],[2,3],[4,5],[1,3],[1,5],[3,5]],dtype=np.uint32)
        self.fix_position=[0,65*esui.YU,10*esui.XU,10*esui.YU]
        return

    pass

class DpRatioRuler(TDP):
    pass

class TdpTrack(TDP):
    def __init__(self,tool):
        super().__init__(tool)
        self.gl_type=gl.GL_LINES
        self.VA=np.array([],dtype=np.float32)
        self.EA=np.array([],dtype=np.uint32)
        return
    pass
