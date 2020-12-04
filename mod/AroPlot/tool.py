import wx,glm
import numpy as np
from core import ESC,esui,esevt,esgl,estool
from .tdp import TdpXyzAxis,TdpGrid,TdpViewBall,TdpTrack
class XyzAxisTool(estool.GLTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpXyzAxis(self)
        self.addToGL()
        return
    pass

class GridTool(estool.GLTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpGrid(self,'xz')
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

class ViewBallTool(estool.GLTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpViewBall(self)
        self.addToGL()
        return
    pass

class AuxDisTool(estool.UIGLTool):
    def __init__(self,name):
        super().__init__(name)
        self.enable=False    # Testing,false default;
        self.aux_list=list()    # aux is a tdp instance with dynamic attrs;
        self.col_dict={
            0:[1,0,0,1],
            1:[0,1,0,1],
            2:[0,0,1,1]}

        self.Bind(esevt.EVT_RESET_SIM,self.onResetSim)
        self.Bind(esevt.EVT_SIM_CIRCLED,self.onSimCircled)
        esui.ARO_PLC.regToolEvent(self)
        self.Hide()
        return

    def updateTDPLIST(self):
        new_list=list()
        for tdp in esgl.TDP_LIST:
            if tdp.tool!=self:
                new_list.append(tdp)
        esgl.TDP_LIST=new_list+self.aux_list
        return

    def onResetSim(self,e):
        if not self.enable:return
        for aux in self.aux_list:
            if type(aux)==TdpTrack:
                aux.__init__(self)
        self.updateTDPLIST()
        esgl.drawGL()
        return

    def onSimCircled(self,e):
        if not self.enable:return
        p_aro_list=list()
        for aro in ESC.ARO_MAP.values():
            if hasattr(aro,'position'):
                p_aro_list.append(aro)

        for aro in p_aro_list:
            hasaux=False
            for aux in self.aux_list:
                if aux.aroid==aro.AroID:
                    if len(aux.VA)==0:continue
                    hasaux=True
                    aux.alive=True
                    vtx=np.array([aro.position+self.col_dict[aux.col]],dtype=np.float32)

                    if (vtx==aux.VA[-1]).all():continue
                    aux.VA=np.append(aux.VA,vtx,axis=0)
                    if len(aux.VA)<50:
                        if len(aux.EA)==0:
                            if len(aux.VA)>=2:
                                aux.EA=np.append(aux.EA,np.array([0,1],dtype=np.uint32))
                        else:
                            aux.EA=np.append(aux.EA,np.array([aux.EA[-1],aux.EA[-1]+1],dtype=np.uint32))
                    else:
                        aux.VA=np.delete(aux.VA,0,axis=0)
                    break
            if not hasaux:
                aux=TdpTrack(self)
                aux.aroid=aro.AroID
                aux.alive=True
                aux.col=aux.aroid % len(self.col_dict)
                aux.VA=np.array([aro.position+self.col_dict[aux.col]],dtype=np.float32)

                self.aux_list.append(aux)

        alive_list=list()
        for aux in self.aux_list:
            if aux.alive:
                aux.update_data=True
                alive_list.append(aux)
        self.aux_list=alive_list
        self.updateTDPLIST()
        return

    def toggleDis(self,enable=True):
        self.enable=enable
        for aux in self.aux_list:
            aux.visible=self.enable
        return

    pass

class MainSwitch(estool.ToggleTool):
    def __init__(self,name,parent,p,s):
        super().__init__(name,parent,p,s,'√',select=True)
        self.xyz_axis=None
        self.view_ball=None
        self.grid=None
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if self.xyz_axis is None:
            self.xyz_axis=estool.getToolByName('xyz_axis','AroPlot')
            self.view_ball=estool.getToolByName('view_ball','AroPlot')
            self.grid=estool.getToolByName('grid','AroPlot')

        self.xyz_axis.tdp.visible=not self.xyz_axis.tdp.visible
        self.grid.tdp.visible=not self.grid.tdp.visible
        self.view_ball.tdp.visible=not self.view_ball.tdp.visible
        e.Skip()
        esgl.drawGL()
        return
    pass
