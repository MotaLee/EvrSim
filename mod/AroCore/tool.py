import wx
import glm
import numpy as np
from core import ESC
from core import esui
from core import esgl
from core import esevt
from core import estool
from .tdp import TdpXyzAxis,TdpGrid,TdpViewBall,TdpTrack
import mod
yu=esui.YU

# Other reliabilities;
class ALibsTreePlc(esui.TreePlc):
    def buildTree(self):
        self.item_list=list()
        for modname in ESC.MOD_LIST:
            aroci=eval('mod.'+modname+'.ARO_INDEX')
            acpci=eval('mod.'+modname+'.ACP_INDEX')
            ti=self.tree_item(modname,children=aroci+acpci)
            self.item_list.append(ti)
            for aitem in aroci+acpci:
                ti=self.tree_item(aitem,depth=1,parent=modname)
                self.item_list.append(ti)
        self.drawTree()
        return
    pass
# Tool class defination;
class AroMenu(estool.CreateMenuTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,parent,p,s,label,items):
        super().__init__(name,parent,p,s,label,items)
        self.mod_name=self.Parent.Label
        self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.HidePopup()
        aroclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        aro=ESC.addAro(aroclass)
        ESC.setAro(aro.AroID,{'AroName':'New Aro'})
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class AcpMenu(estool.CreateMenuTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,parent,p,s,label,items):
        super().__init__(name,parent,p,s,label,items)
        self.mod_name=self.Parent.Label
        self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.HidePopup()
        acpclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        esui.ACP_PLC.addAcpNode(acpclass)
        return
    pass

class RunSimBtn(estool.ToggleTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        esevt.sendEvent(esevt.ETYPE_RUN_SIM,target=esui.WXMW)
        time_txt=estool.getToolByName('time_txt','AroCore')
        if time_txt is None:return
        if time_txt.timer.IsRunning():
            time_txt.timer.Stop()
        else:
            time_txt.timer.Start(int(1000*ESC.TIME_STEP))
        # e.Skip()
        return
    pass

class ResetMapBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        time_txt_shell=estool.getToolByName('time_txt','AroCore')
        if time_txt_shell is not None:
            time_txt_shell.clearTimer()
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_RESET_SIM)
        return
    pass

class SimTimeText(estool.TextTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.timestamp=0.0
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        return

    def onTimer(self,e):
        if ESC.CORE_STAUS=='STOP':
            self.timer.Stop()
            estool.getToolByName('run_btn','AroCore').SetValue(False)
            return
        if self.timer.IsRunning():
            self.timestamp+=ESC.TIME_STEP*ESC.TIME_RATE
            m=int(self.timestamp/60)
            s=int(self.timestamp) % 60
            ms=int((self.timestamp-int(self.timestamp))*60)
            if m<10:m='0'+str(m)
            else: m=str(m)
            if s<10:s='0'+str(s)
            else: s=str(s)
            if ms<10:ms='0'+str(ms)
            else: ms=str(ms)
            self.SetLabel(m+':'+s+':'+ms)
            self.Refresh()
        return

    def clearTimer(self):
        self.timestamp=0
        self.SetLabel('00:00:00')
        self.Refresh()
        return
    pass

class ALibsBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.show_lib=False
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if self.show_lib:return
        else:self.show_lib=True
        self.tab=esui.SIDE_PLC.getTab('ALibs')
        # self.tab.SetBackgroundColour(esui.COLOR_LBACK)
        tx=self.tab.Size.x
        ty=self.tab.Size.y
        self.tab.txt_alibs=esui.StaticText(self.tab,(yu,yu),(8*yu,4*yu),'ALibs:',align='left')
        self.tab.btn_add=esui.Btn(self.tab,(tx-5*yu,yu),(4*yu,4*yu),'+')
        self.tab.input_search=esui.InputText(self.tab,(yu,6*yu),(tx-11*yu,4*yu))
        self.tab.btn_search=esui.Btn(self.tab,(tx-9*yu,6*yu),(8*yu,4*yu),'Search')
        self.tab.tree=ALibsTreePlc(self.tab,(yu,11*yu),(tx-2*yu,50*yu))
        self.tab.tree.buildTree()
        self.tab.Show()
        self.tab.btn_add.Bind(wx.EVT_LEFT_DOWN,self.onClkAdd)
        return

    def onClkAdd(self,e):
        ti_list=self.tab.tree.getSelection()
        if len(ti_list)==0:return
        ti=ti_list[0]
        classname=ti.parent+'.'+ti.label
        try:aroci=eval('mod.'+ti.parent+'.ARO_INDEX')
        except BaseException:return
        if ti.Label in aroci:
            aro=ESC.addAro(classname)
            ESC.setAro(aro.AroID,{'AroName':'New Aro'})
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        else:esui.ACP_PLC.addAcpNode(classname)
        return
    pass
# Lv.3, Aro panel Tool with tdp;
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
        esui.ARO_PLC.drawGL()
        return

    def onSimCircled(self,e):
        if not self.enable:return
        p_aro_list=list()
        for aro in ESC.ARO_MAP:
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
