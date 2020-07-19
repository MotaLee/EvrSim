
import wx
from core import esui
wxapp = wx.App()
cx,cy,cw,ch=wx.ClientDisplayRect()
xu=cw/100
yu=ch/100
esui.XU=xu
esui.YU=yu
class ESW(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,pos=(cx,cy+50),size=(cw,ch-50),name='wxmw',
            style=wx.SYSTEM_MENU)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        return
    pass

def onClk(e):
    print(1)
    return
wxmw=ESW()
testui=esui.ScrolledPlc(wxmw,(100,100),(200,300))
test_txt1=esui.btn(testui,(0,0),(100,50),'text')
test_txt=esui.Stc(testui,(0,290),(100,50),'text')
testui.updateVirtualSize()

test_txt.Bind(wx.EVT_LEFT_DOWN,onClk)
wxmw.Show()
wxapp.MainLoop()
