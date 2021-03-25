import wx
from core import ESC,esui
class EsWindow(wx.Frame):
    def __init__(self,p=None,s=None,title='EsWindow'):
        cx,cy,cw,ch=wx.ClientDisplayRect()
        if p is None:p=(cx,cy)
        if s is None:s=(cw,ch)
        super().__init__(None,pos=p,size=s,title=title,style=wx.NO_BORDER | wx.ICON_HAND)
        self.list_evtool=list()
        self.dialog=None
        self.icon = wx.Icon('res/img/evrsim.ico', wx.BITMAP_TYPE_ICO)
        self.gl_timer=wx.Timer(self)
        self.SetIcon(self.icon)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        # self.Bind(esui.EBIND_RUN_SIM, self.onRunSim)
        self.Bind(wx.EVT_CHAR_HOOK,self.onKeyDown)
        self.Bind(wx.EVT_TIMER,self.onRunSimTimer,self.gl_timer)
        return

    def onComEvt(self,e:wx.Event):
        e.Skip()
        etype=e.getEventArgs()
        if etype==esui.ETYPE_RUN_SIM:
            # self.onOpenSim(e)
            self.runSim()
            pass
        for tool in self.list_evtool:
            esui.sendEvent(etype,target=tool)
        return

    def runSim(self):
        if self.gl_timer.IsRunning():
            self.gl_timer.Stop()
        else:
            if ESC.isCoreStop():ESC.setCoreReady()
            self.gl_timer.Start(1000//ESC.fps)
        return

    def onRunSimTimer(self,e):
        if ESC.isCoreBusy():return
        elif ESC.isCoreStop():
            self.gl_timer.Stop()
            esui.UMR.MAP_DIV.readMap()
        elif ESC.isCoreReady():
            esui.UMR.MAP_DIV.readMap()
            ESC.runCompiledSim()
            esui.sendComEvt(esui.ETYPE_STEP_SIM)
        return

    def onKeyDown(self,e):
        e.Skip()
        if not isinstance(e.EventObject,wx.TextCtrl):
            esui.sendComEvt(esui.ETYPE_KEY_DOWN,None,eobj=e)
        return

    def regToolEvent(self,tool:wx.Window):
        if tool not in self.list_evtool:
            self.list_evtool.append(tool)
            tool.SetExtraStyle(wx.WS_EX_BLOCK_EVENTS)
        else:
            self.list_evtool.remove(tool)
        return

    def lauchApp(self):

        return
    pass
