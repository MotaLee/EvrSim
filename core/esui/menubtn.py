# Parent lib;
import wx
from core import esui
gmv=esui.gmv

# Menu btn wx sub class;
class MenuBtn(wx.ComboCtrl):
    click_ctrl=False
    on_ctrl=False

    def __init__(self,parent,p,s,menulabel,items):
        wx.ComboCtrl.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            value=menulabel,
            style=wx.CB_READONLY)
        self.Label=menulabel
        self.setItems(items)

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def setItems(self,items):
        popup=ppc(items)
        self.SetPopupControl(popup)
        self.SetPopupMaxHeight(len(items)*self.Size[1]+gmv.YU)
        self.SetPopupMinWidth(2*self.Size[0]+gmv.YU)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.click_ctrl:
            dc.SetBrush(wx.Brush(gmv.COLOR_Front))
        elif self.on_ctrl:
            dc.SetBrush(wx.Brush('#555555'))
        else:
            dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        dc.SetBrush(wx.Brush(gmv.COLOR_Front))
        dc.DrawPolygon([
            (self.Size[0]-1,self.Size[1]-1),
            (self.Size[0]-7,self.Size[1]-1),
            (self.Size[0]-1,self.Size[1]-7)])

        if self.click_ctrl:
            dc.SetTextForeground(gmv.COLOR_Back)
        else:
            dc.SetTextForeground(gmv.COLOR_Text)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        self.on_ctrl=True
        self.Refresh(eraseBackground=False)
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.Refresh(eraseBackground=False)
        return

    def onClk(self,e):
        self.click_ctrl=True
        self.ShowPopup()
        self.GetPopupControl().lctrl.Refresh(eraseBackground=False)
        return
    pass

class ppc(wx.ComboPopup):
    def __init__(self,items):
        wx.ComboPopup.__init__(self)
        self.ipos=1
        self.item=items
        return
    # Overrided;
    def Create(self,parent):
        self.lctrl=wx.ListCtrl(parent,
            style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.NO_BORDER)
        self.lctrl.SetBackgroundColour(gmv.COLOR_Back)
        self.lctrl.Bind(wx.EVT_MOTION, self.onMoveMouse)
        self.lctrl.Bind(wx.EVT_LEFT_DOWN, self.onClk)
        self.lctrl.Bind(wx.EVT_PAINT,self.onPaint)
        self.pw=self.GetComboCtrl().Size[0]
        self.ph=self.GetComboCtrl().Size[1]
        return True
    # Overrided;
    def GetControl(self):
        return self.lctrl
    # Overrided;
    def GetStringValue(self):
        return str(self.ipos)
    # Overrided;
    def OnDismiss(self):
        self.GetComboCtrl().click_ctrl=False
        wx.ComboPopup.OnDismiss(self)
        return

    def onPaint(self,e):
        dc=wx.BufferedPaintDC(self.lctrl)
        dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawRectangle(0,0,self.lctrl.Size[0],self.lctrl.Size[1])
        dc.DrawLine(5,self.ph*self.ipos,self.pw*2-5,self.ph*self.ipos)
        dc.SetTextForeground(gmv.COLOR_Text)
        pts=dc.GetTextExtent(self.GetComboCtrl().GetLabel())
        for i in range(0,len(self.item)):
            dc.DrawText(self.item[i],(self.pw-pts[0])//2,int(i*self.ph+pts[1]/2))
        return

    def onClk(self,e):
        self.Dismiss()
        return

    def onMoveMouse(self,e):
        cpos=e.GetPosition()
        self.ipos=cpos[1]//self.ph+1
        self.lctrl.Refresh(eraseBackground=False)
        e.Skip()
        return
    pass

class BorderlessMenuBtn(MenuBtn):
    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.click_ctrl:
            dc.SetBrush(wx.Brush(gmv.COLOR_Front))
        elif self.on_ctrl:
            dc.SetBrush(wx.Brush('#555555'))
        else:
            dc.SetBrush(wx.Brush('#333333'))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self.click_ctrl:
            dc.SetTextForeground(gmv.COLOR_Back)
        else:
            dc.SetTextForeground(gmv.COLOR_Text)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return
    pass
