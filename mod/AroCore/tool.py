import wx
import glm
from core import ESC
from core import esui
from core import esgl
from core import esevt
from core import estool
from .tdp import TdpXyzAxis,TdpGrid,TdpViewBall
# Tool class defination;
class CreateAroTool(estool.CreateTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,label,p,s,items):
        super().__init__(name,label,p,s,items)
        return

    def build(self,parent):
        super().build(parent)
        self.mod_name=self.ctrl.Parent.Label
        self.popup=self.ctrl.GetPopupControl()
        self.popup.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.ctrl.HidePopup()
        aroclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        aro=ESC.addAro(aroclass)
        ESC.setAro(aro.AroID,{'AroName':'New Aro'})
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_UPDATE_MAP)
        return
    pass

class CreateAcpTool(estool.CreateTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,label,p,s,items):
        super().__init__(name,label,p,s,items)
        return

    def build(self,parent):
        super().build(parent)
        self.mod_name=self.ctrl.Parent.Label
        self.popup=self.ctrl.GetPopupControl()
        self.popup.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.ctrl.HidePopup()
        acpclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        acp=ESC.addAcp(acpclass,esui.ACP_PLC.acpmodel)
        ESC.setAcp(acp.AcpID,{'AcpName':'New Acp'},esui.ACP_PLC.acpmodel)
        esui.ACP_PLC.drawAcp()
        return
    pass

class RunSimTool(estool.ToggleTool):
    def __init__(self,name,label,p,s,state=False,tip=''):
        super().__init__(name,label,p,s,state,tip)
        return

    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        esevt.sendEvent(esevt.esEVT_RUN_SIM,target=esui.WXMW)
        time_txt=estool.getToolByName('time_txt','AroCore').ctrl
        if time_txt.timer.IsRunning():
            time_txt.timer.Stop()
        else:
            time_txt.timer.Start(int(1000*ESC.TIME_STEP))
        e.Skip()
        return
    pass

class ResetMapTool(estool.ButtonTool):
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        time_txt_shell=estool.getToolByName('time_txt','AroCore')
        time_txt_shell.clearTimer()
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_RESET_SIM)
        return
    pass

class SimTimeText(estool.TextTool):
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        self.timestamp=0.0
        self.run_btn=None
        return

    def build(self,parent):
        super().build(parent)
        self.ctrl.timer=wx.Timer(self.ctrl)
        self.ctrl.Bind(wx.EVT_TIMER,self.onTimer,self.ctrl.timer)
        self.run_btn=estool.getToolByName('run_btn','AroCore').ctrl
        return

    def onTimer(self,e):
        if ESC.CORE_STAUS=='STOP':
            self.ctrl.timer.Stop()
            self.run_btn.SetValue(False)
            return
        if self.ctrl.timer.IsRunning():
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
            self.ctrl.SetLabel(m+':'+s+':'+ms)
            self.ctrl.Refresh()
        return

    def clearTimer(self):
        self.timestamp=0
        self.ctrl.SetLabel('00:00:00')
        self.ctrl.Refresh()
        return
    pass

# Lv.3, Aro panel Tool with tdp;
class XyzAxisTool(estool.StaticDPTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpXyzAxis(self)
        return
    pass

class GridTool(estool.StaticDPTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpGrid(self,'xz')
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

class ViewBallTool(estool.StaticDPTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=TdpViewBall(self)
        return
    pass
