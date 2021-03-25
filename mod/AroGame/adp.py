import numpy as np
import OpenGL.GL as gl
from core import ESC,esgl
class MeshObj(esgl.AroDrawPart):
    def __init__(self, aroid):
        super().__init__(aroid)
        # self.list_mesh=esgl.import3DFile('mod/Dynamics/res/moment.obj')
        # self.list_mesh=esgl.import3DFile('1.fbx')
        self.list_mesh=esgl.import3DFile('mod/Game/res/zhong.fbx')
        super().updateAdp()
        return
    pass
