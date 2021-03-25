import _glm as glm
import numpy as np
from core import ESC,esui,esgl,estl
GLC=esgl.glc
from .tdp import TdpXyzAxis,TdpGrid,TdpViewBall,TdpTrack
class XyzAxisTool(estl.GLTool):
    def __init__(self):
        super().__init__()
        self.tdp=TdpXyzAxis(self)
        self.addToGL()
        return
    pass

class GridTool(estl.GLTool):
    def __init__(self):
        super().__init__()
        self.tdp=TdpGrid(self)
        self.transGrid('xz')
        self.addToGL()
        return

    def transGrid(self,panel):
        if panel=='xz':
            self.tdp.trans=glm.mat4(1.0)
        elif panel=='yz':
            self.tdp.trans=glm.rotate(glm.mat4(1),glm.radians(90),glm.vec3(0,0,1))
        elif panel=='xy':
            self.tdp.trans=glm.rotate(glm.mat4(1),glm.radians(90),glm.vec3(1,0,0))
        return
    pass

class ViewBallTool(estl.GLTool):
    def __init__(self):
        super().__init__()
        self.tdp=TdpViewBall(self)
        self.addToGL()
        return
    pass

# class AuxTool(estl.UIGLTool):
#     def __init__(self,name,mod):
#         super().__init__(name,mod)
#         self.enable=True
#         self.aux_list=list()    # aux is a tdp instance with dynamic attrs;
#         self.col_dict={
#             0:[1,0,0,1],
#             1:[0,1,0,1],
#             2:[0,0,1,1]}

#         self.Bind(esui.EBIND_RESET_SIM,self.onResetSim)
#         self.Bind(esui.EBIND_STEP_SIM,self.onSimCircled)
#         esui.UMR.MAP_DIV.regToolEvent(self)
#         self.Hide()
#         return

#     def onResetSim(self,e):
#         if not self.enable:return
#         for aux in self.aux_list:
#             if type(aux)==TdpTrack:
#                 aux.__init__(self)
#         GLC.addTdp(self.fullname,self.aux_list)
#         GLC.drawGL()
#         return

#     def onSimCircled(self,e):
#         if not self.enable:return
#         p_aro_list=list()
#         for aro in ESC.getFullMap():
#             if hasattr(aro,'position'):
#                 p_aro_list.append(aro)

#         for aro in p_aro_list:
#             aro:ESC.Aro
#             hasaux=False
#             for aux in self.aux_list:
#                 if isinstance(aux,TdpTrack) and aux.aroid==aro.AroID:
#                     if len(aux.VA)==0:continue
#                     hasaux=True
#                     aux.flag_alive=True
#                     vtx=np.array([aro.position+self.col_dict[aux.col]],dtype=np.float32)

#                     if (vtx==aux.VA[-1]).all():continue
#                     aux.VA=np.append(aux.VA,vtx,axis=0)
#                     if len(aux.VA)<50:
#                         if len(aux.EA)==0:
#                             if len(aux.VA)>=2:
#                                 aux.EA=np.append(aux.EA,np.array([0,1],dtype=np.uint32))
#                         else:
#                             aux.EA=np.append(aux.EA,np.array([aux.EA[-1],aux.EA[-1]+1],dtype=np.uint32))
#                     else:aux.VA=np.delete(aux.VA,0,axis=0)
#                     break
#             if not hasaux:
#                 aux=TdpTrack(self)
#                 aux.aroid=aro.AroID
#                 aux.col=aux.aroid % len(self.col_dict)
#                 aux.VA=np.array([aro.position+self.col_dict[aux.col]],dtype=np.float32)
#                 self.aux_list.append(aux)

#         alive_list=list()
#         for aux in self.aux_list:
#             if aux.flag_alive:
#                 aux.flag_update=True
#                 alive_list.append(aux)
#         self.aux_list=alive_list
#         GLC.addTdp(self.fullname,self.aux_list)
#         return

#     pass

class DisplaySwitch(estl.ToggleButton):
    def __init__(self,parent,name,mod,**argkw):
        super().__init__(parent,name,mod,**argkw)
        self.Bind(esui.EBIND_LEFT_CLK,self.onClk)
        return

    def onClk(self,e):
        e.Skip()
        from . import xyz_axis,grid,view_ball
        if self.label=='All':
            xyz_axis.tdp.visible=not xyz_axis.tdp.visible
            grid.tdp.visible=not grid.tdp.visible
            view_ball.tdp.visible=not view_ball.tdp.visible
        if self.label=='Trc':
            pass
        GLC.drawGL()
        return
    pass
