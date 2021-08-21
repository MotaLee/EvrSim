# import _glm as glm
import numpy as np
from core import esgl
class TdpXyzAxis(esgl.ToolDrawPart):
    def __init__(self,tool):
        super().__init__(tool)
        VA=np.array([
            [0,0,0,     1,0,0,1],
            [.5,0,0,    1,0,0,1],
            [0,0,0,     0,1,0,1],
            [0,.5,0,    0,1,0,1],
            [0,0,0,     0,0,1,1],
            [0,0,.5,    0,0,1,1]],
            dtype=np.float32)
        EA=np.array([[0,1],[2,3],[4,5]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        return
    pass

class TdpGrid(esgl.ToolDrawPart):
    # gap=0.5;
    def __init__(self,tool):
        super().__init__(tool)
        EA=np.array([],dtype=np.uint32)
        VA=np.zeros([44,7],dtype=np.float32)
        for i in range(0,21,2):
            VA[i]=[-5/2,0,i/4-2.5,.5,.5,.5,1]
            VA[i+1]=[5/2,0,i/4-2.5,.5,.5,.5,1]
            VA[i+22]=[i/4-2.5,0,-5/2,.5,.5,.5,1]
            VA[i+23]=[i/4-2.5,0,5/2,.5,.5,.5,1]
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        return
    pass

class TdpViewBall(esgl.ToolDrawPart):
    def __init__(self,tool):
        super().__init__(tool)
        self.dict_fix['fix']=True
        from core import esui
        self.dict_fix['pos']=[0,65*esui.YU,10*esui.XU,10*esui.YU]
        VA=np.array([
            [0,0,0,     1,0,0,1],
            [.3,0,0,    1,0,0,1],
            [0,0,0,     0,1,0,1],
            [0,.3,0,    0,1,0,1],
            [0,0,0,     0,0,1,1],
            [0,0,.3,    0,0,1,1]],
            dtype=np.float32)
        EA=np.array([[0,1],[2,3],[4,5],[1,3],[1,5],[3,5]],dtype=np.uint32)
        self.addMesh(
            draw_type=esgl.DT_LINE,
            layout=[esgl.VtxLayout('color')],
            vertices=VA,faces=EA)
        return

    pass

class DpRatioRuler(esgl.ToolDrawPart):
    pass

class TdpTrack(esgl.ToolDrawPart):
    def __init__(self,tool):
        super().__init__(tool)
        self.draw_type=esgl.DT_LINE
        # self.dict_layout['color']=4
        self.aroid=-1
        self.flag_alive=True
        self.col=[1,1,1,1]
        return
    pass
