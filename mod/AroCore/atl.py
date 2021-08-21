import time
import wx
from core import ESC,esc,esui,estl
yu=esui.YU
# Tool class defination;
class AroMenu(estl.ToolBase,esui.MenuBtnDiv):
    ''' Menu to create Aro.
        * Argkw items: List of Aroes;'''
    def __init__(self,parent,name,mod,**argkw):
        esui.MenuBtnDiv.__init__(self,parent,**argkw)
        estl.ToolBase.__init__(self,name,mod)
        self.bindPopup(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        e.Skip()
        abbrclass=e.EventObject.label
        if hasattr(ESC,abbrclass):
            aroclass=getattr(ESC,abbrclass)
        else:
            aroclass='mod.'+self.mod+'.'+abbrclass
        ESC.addAro(AroClass=aroclass,AroName='New Aro')
        esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        return
    pass

class AcpMenu(estl.ToolBase,esui.MenuBtnDiv):
    ''' Menu to create Acp.
        * Argkw items: List of Aroes;'''
    def __init__(self,parent,name,mod,**argkw):
        esui.MenuBtnDiv.__init__(self,parent,**argkw)
        estl.ToolBase.__init__(self,name,mod)
        self.bindPopup(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        e.Skip()
        abbrclass=e.EventObject.label
        if hasattr(esc,abbrclass):
            acpclass=getattr(esc,abbrclass)
        else:
            acpclass='mod.'+self.mod+'.'+abbrclass
        esui.UMR.MDL_DIV.addAcpNode(acpclass)
        return
    pass

class RunSimBtn(esui.TglBtn):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        e.Skip()
        if ESC.isCoreReady():
            esui.sendComEvt(esui.ETYPE_RUN_SIM,target=esui.UMR.ESMW)
            try:
                from . import txt_real,txt_time
                if txt_time.timer.IsRunning():
                    txt_time.timer.Stop()
                else:
                    txt_time.timer.Start(1000//ESC.fps)
                if txt_real.timer.IsRunning():
                    txt_real.timer.Stop()
                else:
                    txt_real.start=time.time()
                    txt_real.timer.Start(1000//ESC.fps)
            except BaseException:pass
        return
    pass

class ResetMapBtn(estl.Button):
    def __init__(self,parent,name,mod,**argkw):
        super().__init__(parent,name,mod,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        try:
            from . import txt_real,txt_time
            if txt_time is not None:txt_time.clearTimer()
            if txt_real is not None:txt_real.clearTimer()
        except BaseException:pass
        esui.sendComEvt(esui.ETYPE_RESET_SIM)
        return
    pass

class SimTimeText(esui.DivText):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.timestamp=0.0
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        return

    def onTimer(self,e):
        if ESC.isCoreStop():
            self.timer.Stop()
            from . import btn_run
            btn_run.SetValue(False)
            return
        if self.timer.IsRunning():
            self.timestamp+=ESC.TIME_RATE/ESC.fps
            m=int(self.timestamp/60)
            s=int(self.timestamp) % 60
            ms=int((self.timestamp-int(self.timestamp))*60)
            if m<10:m='0'+str(m)
            else: m=str(m)
            if s<10:s='0'+str(s)
            else: s=str(s)
            if ms<10:ms='0'+str(ms)
            else: ms=str(ms)
            self.setLabel(m+':'+s+':'+ms)
        return

    def clearTimer(self):
        self.timestamp=0
        self.setLabel('00:00:00')
        return
    pass

class RealTimeText(esui.DivText):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.start=0
        self.timestamp=0.0
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        return

    def onTimer(self,e):
        if ESC.isCoreStop():
            self.timer.Stop()
            return
        if self.timer.IsRunning():
            self.timestamp=time.time()-self.start
            m=int(self.timestamp/60)
            s=int(self.timestamp) % 60
            ms=int((self.timestamp-int(self.timestamp))*60)
            if m<10:m='0'+str(m)
            else: m=str(m)
            if s<10:s='0'+str(s)
            else: s=str(s)
            if ms<10:ms='0'+str(ms)
            else: ms=str(ms)
            self.setLabel(m+':'+s+':'+ms)
        return

    def clearTimer(self):
        self.timestamp=0
        self.start=0
        self.setLabel('00:00:00')
        return
    pass

class ALibsBtn(estl.Button):
    'todo'
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.show_lib=False
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if self.show_lib:return
        else:self.show_lib=True
        self.tab=esui.UMR.SIDE_DIV.getTab('ALibs')
        # self.tab.SetBackgroundColour(esui.COLOR_LBACK)
        tx=self.tab.Size.x
        ty=self.tab.Size.y
        self.tab.txt_alibs=esui.StaticText(self.tab,(yu,yu),(8*yu,4*yu),'ALibs:',align='left')
        self.tab.btn_add=esui.Btn(self.tab,(tx-5*yu,yu),(4*yu,4*yu),'+')
        self.tab.input_search=esui.InputText(self.tab,style={'p':(yu,6*yu),'s':(tx-11*yu,4*yu)})
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
            ESC.setAro(aro.AroID,AroName='New Aro')
            esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        else:esui.UMR.MDL_DIV.addAcpNode(classname)
        return
    pass

class WrkSpcBtn(estl.Button):
    def __init__(self,parent,name,mod,**argkw):
        super().__init__(parent,name,mod,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        esui.toggleWorkspace()
        return
    pass

class EnablePresetBtn(esui.TglBtn):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        e.Skip()
        ESC.setSim({'flag_preset':self.getStatus()})
        if ESC.isCoreReady():
            esui.sendComEvt(esui.ETYPE_RUN_PRESET,target=esui.UMR.ESMW)
        return
    pass
