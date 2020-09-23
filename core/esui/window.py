import threading
import wx
from core import ESC
from core import esui
from core import esevt
class EsWindow(wx.Frame):
    def __init__(self,p=None,s=None,title='EsWindow'):
        cx,cy,cw,ch=wx.ClientDisplayRect()
        if p is None:p=(cx,cy)
        if s is None:s=(cw,ch)
        super().__init__(None,pos=p,size=s,title=title,style=wx.NO_BORDER | wx.ICON_HAND)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.icon = wx.Icon('res/img/evrsim.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.dialog=None
        self.gl_timer=wx.Timer(self)
        self.esc_thread=ESCThread()
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(esevt.EVT_RUN_SIM, self.onRunSim)
        self.Bind(wx.EVT_CHAR_HOOK,self.onKeyDown)
        self.Bind(wx.EVT_TIMER,self.onRunSimTimer,self.gl_timer)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_OPEN_SIM:
            self.onOpenSim(e)
        e.Skip()
        return

    def onRunSim(self,e):
        if self.gl_timer.IsRunning():
            self.gl_timer.Stop()
        else:
            if ESC.CORE_STAUS=='STOP':ESC.CORE_STAUS='READY'
            from core import esgl
            self.gl_timer.Start(int(1000/esgl.FPS))
        return

    def onRunSimTimer(self,e):
        if ESC.CORE_STAUS=='STOP':
            self.gl_timer.Stop()
            esui.ARO_PLC.readMap()
        elif ESC.CORE_STAUS=='BUSY':
            return
        elif ESC.CORE_STAUS=='READY':
            esui.ARO_PLC.readMap()
            if not self.esc_thread.is_alive():
                self.esc_thread=ESCThread()
                self.esc_thread.start()
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_SIM_CIRCLED)
        return

    def onOpenSim(self,e):
        if ESC.SIM_NAME!='':
            'todo: open sim after already opened another sim;'
            return
        sim_name=e.GetEventArgs(1)
        ESC.openSim(sim_name)
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_LOAD_MOD)
        return

    def onKeyDown(self,e):
        if not isinstance(e.EventObject,wx.TextCtrl):
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,[esevt.ETYPE_KEY_DOWN,e])
        e.Skip()
        return
    pass

class ESCThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        return

    def run(self):
        ESC.runSim()
        return
    pass
