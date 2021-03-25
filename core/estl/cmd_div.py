import wx
from core import ESC,esui
xu=esui.XU
yu=esui.YU
class CmdDiv(esui.Div):
    def __init__(self,parent,**argkw):
        argkw['style']['border']=esui.COLOR_FRONT
        super().__init__(parent,**argkw)
        self.histxt=esui.MultilineText(self,readonly=True,
            style={'p':(0,0),'s':(75*xu,17*yu)})
        self.comhead=esui.StaticText(self,(yu,17*yu),(8*xu,4*yu),'EvrSim>>',align='left')
        self.comtxt=esui.InputText(self,style={'p':(9*yu,17*yu),'s':(75*xu-10*yu,4*yu)})
        self.comtxt.SetExtraStyle(wx.TE_PROCESS_ENTER)
        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.comtxt.Bind(wx.EVT_TEXT_ENTER,self.onCmd)
        # self._err=ESC.err
        ESC.err=self.err

        self.Hide()
        return

    def err(self,bugstr,report=False):
        esui.sendComEvt(esui.ETYPE_OPEN_CMD)
        self.histxt.appendText(bugstr+'\n')
        return

    def onComEvt(self,e):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_OPEN_CMD:
            self.Show()
        elif etype==esui.ETYPE_CLOSE_CMD:
            self.Hide()
        elif etype==esui.ETYPE_KEY_DOWN:
            self.onKeyDown(e.getEventArgs('eobj'))
        return

    def onCmd(self,e):
        self.histxt.appendText('EvrSim>>'+e.String+'\n')
        self.histxt.Refresh()
        return

    def onKeyDown(self,e):
        if e.GetKeyCode()==wx.WXK_ESCAPE:
            esui.sendComEvt(esui.ETYPE_CLOSE_CMD)
        e.Skip()
        return
    pass
