import glm
import numpy as np
import OpenGL.GL as gl
from core import ESC
from core import esui
from core import esgl

# OpenGL drawing part class;
class DrawPart(object):
    ''' Attr: dp_name, gl_type, VA, EA, trans, Aro, dim.

        Para Aro: accept Aro or its AroID.;'''
    def __init__(self):
        self.dp_name=''

        self.gl_type=gl.GL_POINTS

        self.fix_position=False
        self.fix_size=False
        self.fix_orientation=False
        self.highlight=False

        self.VA=np.array([],dtype=np.float32)
        self.EA=np.array([],dtype=np.uint32)
        self.trans=glm.mat4(1.0)
        self.ftrans=glm.mat4(1.0)

        return

    def transADP(self):
        ftrans=self.trans
        if self.fix_position:
            dpp=self.fix_position
            gl.glViewport(int(dpp[0]+4*esui.YU),int(esgl.PLC_H-dpp[1]-dpp[3]),int(dpp[2]),int(dpp[3]))
            ftrans=glm.translate(ftrans,glm.vec3(esgl.AP.tolist()))
            ftrans=glm.scale(ftrans,glm.vec3(esgl.PLC_H/dpp[3]))
        else:
            gl.glViewport(0,0,esgl.PLC_W,esgl.PLC_H)
            if self.fix_size:
                v_AE=(esgl.EP-esgl.AP).tolist()
                v_OE=(esgl.EP-self.Aro.position).tolist()
                agl_AEO=esgl.getAngleFrom2Vec3(v_AE,v_OE)
                l_ArE=glm.length(v_OE)*glm.cos(agl_AEO)
                l_AE=glm.length(v_AE)
                ftrans=glm.scale(ftrans,glm.vec3(l_ArE/l_AE))
        if self.fix_orientation:
            ftrans=esgl.getFixOriMat(ftrans)
        self.ftrans=ftrans
        return
    pass

class AroDrawPart(DrawPart):
    ''' Para Aro: accept Aro or its AroID.;'''
    def __init__(self,aro=None):
        super().__init__()
        if type(aro)==int:aro=ESC.getAro(aro)
        self.Aro=aro
        if hasattr(aro,'position'):
            self.ep_dis=np.linalg.norm(esgl.EP-aro.position)
        self.dp_name=aro.AroID
        return
    pass

class ToolDrawPart(DrawPart):
    ''' Para Aro: accept Aro or its AroID.;'''
    def __init__(self,tool):
        super().__init__()
        self.tool=tool
        return
    pass
