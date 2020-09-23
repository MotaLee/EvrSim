import wx
from core import esui

class AcpToolPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        yu=esui.YU
        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Acp')
        self.move_btn=esui.BlSelectBtn(self,(0,2*yu),(4*yu,4*yu),'Mv')
        self.remove_btn=esui.BorderlessBtn(self,(0,6*yu),(4*yu,4*yu),'Rm')
        self.attach_btn=esui.BlSelectBtn(self,(0,self.Size[1]-4*yu),(4*yu,4*yu),'Att')

        self.move_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMove)
        self.remove_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkRemove)
        self.attach_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAttach)
        return

    def onClkRemove(self,e):
        self.Parent.canvaspl.rmAcpNodes()
        return

    def onClkMove(self,e):
        if self.Parent.canvaspl.acp_moving:
            self.Parent.canvaspl.acp_moving=False
        else:
            self.Parent.canvaspl.acp_moving=True
        e.Skip()
        return

    def onClkAttach(self,e):
        if self.Parent.canvaspl.attaching:
            self.Parent.canvaspl.attaching=False
        else:
            self.Parent.canvaspl.attaching=True
        e.Skip()
        return
    pass
