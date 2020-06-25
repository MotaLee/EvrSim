import wx
from core import ESC
from core import esui
from core import esevt
# Tool class defination;
# Lv.1;
class BaseTool(object):
    'Lv:1: Base tool class. Only build base var;'
    def __init__(self,name,label,p,s):
        self.name=name
        self.label=label
        self.p=p
        self.s=s
        self.ctrl=None
        return

    def getToolByName(self,toolname):
        if self.ctrl is None: return ESC.bug('E: Control not built.')
        for ctrl in self.ctrl.Parent.Children:
            if ctrl.name==toolname:
                return ctrl
        return ESC.bug('Control not found.')
    pass

# Lv.2;
class CreateTool(BaseTool):
    'Lv:2: Second tool class. Build MenuBtn ctrl;'
    def __init__(self,name,label,p,s,indexlist):
        super().__init__(name,label,p,s)
        self.index=indexlist
        return

    def build(self,parent):
        self.ctrl=esui.MenuBtn(parent,
            self.p,self.s,
            self.label,self.index)
        self.ctrl.name=self.name
        return
    pass

class ToggleTool(BaseTool):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,label,p,s,state=False,tip=''):
        super().__init__(name,label,p,s)
        self.state=state
        self.tip=tip
        return

    def build(self,parent):
        self.ctrl=esui.SelectBtn(parent,
            self.p,self.s,
            self.label,
            select=self.state,
            tip=self.tip,tsize=self.s[1]/2)
        self.ctrl.name=self.name
        return
    pass

class TextTool(BaseTool):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        self.ctrl=esui.Stc(parent,self.p,self.s,
            self.label,
            tsize=self.s[1]/2)
        self.ctrl.name=self.name
        return
    pass

class ButtonTool(BaseTool):
    'Lv:2: Second tool class. Build Btn ctrl;'
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        self.ctrl=esui.btn(parent,self.p,self.s,
            self.label)
        self.ctrl.name=self.name
        return
    pass

# Lv.3;
class CreateAroTool(CreateTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,label,p,s,indexlist):
        super().__init__(name,label,p,s,indexlist)
        return
    def build(self,parent):
        super().build(parent)
        self.popup=self.ctrl.GetPopupControl()
        self.popup.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return
    def onClkPopup(self,e):
        self.ctrl.HidePopup()
        print(self.popup.ipos)
        return
    pass

class CreateAcpTool(CreateTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,label,p,s,indexlist):
        super().__init__(name,label,p,s,indexlist)
        return
    def build(self,parent):
        super().build(parent)
        self.mod_name=self.ctrl.Parent.Label
        self.popup=self.ctrl.GetPopupControl()
        self.popup.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return
    def onClkPopup(self,e):
        self.ctrl.HidePopup()
        wxmw=self.ctrl.Parent.Parent.Parent  # wxmw.modpl.modtab.self;
        acppl=wxmw.FindWindowByName('acppl')
        acpclass='mod.'+self.mod_name+'.'+self.index[self.popup.ipos-1]
        acp=ESC.addAcp(acpclass,acppl.acpmodel)
        ESC.setAcp(acp.AcpID,{'AcpName':'New Acp'},acppl.acpmodel)
        acppl.drawAcp()
        return
    pass

class RunSimTool(ToggleTool):
    def __init__(self,name,label,p,s,state=False,tip=''):
        super().__init__(name,label,p,s,state,tip)
        return

    def build(self,parent):
        super().build(parent)
        self.wxmw=parent.Parent.Parent     # wxmw.modpl.modtab.self;
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        self.wxmw.sendEvent(esevt.esEVT_RUN_SIM)
        time_txt=self.getToolByName('time_txt')
        if time_txt.timer.IsRunning():
            time_txt.timer.Stop()
        else:
            time_txt.timer.Start(int(1000*ESC.TIME_STEP))
        e.Skip()
        return
    pass

class ResetMapTool(ButtonTool):
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return
    def onClk(self,e):
        ESC.loadMapFile()
        wxmw=self.ctrl.Parent.Parent.Parent
        aropl=wxmw.FindWindowByName('aropl')
        aropl.readMap()
        return
    pass

class TimeTextTool(TextTool):
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        self.timestamp=0.0
        return

    def build(self,parent):
        super().build(parent)
        self.ctrl.timer=wx.Timer(self.ctrl)
        self.ctrl.Bind(wx.EVT_TIMER,self.onTimer,self.ctrl.timer)
        return

    def onTimer(self,e):
        if self.ctrl.timer.IsRunning():
            self.timestamp+=ESC.TIME_STEP
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
    pass
