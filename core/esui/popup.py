# Parent lib;
import wx
from core import esui
yu=esui.YU

class PopupList(wx.ComboPopup):
    def __init__(self,items):
        super().__init__()
        self.ipos=0
        self.items=items
        return

    def Create(self,parent):
        # Overrided;
        self.lctrl=wx.ListCtrl(parent,
            style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.NO_BORDER)
        self.lctrl.SetBackgroundColour(esui.COLOR_BACK)
        self.lctrl.Bind(wx.EVT_MOTION, self.onMove)
        self.lctrl.Bind(wx.EVT_LEFT_DOWN, self.onClk)
        self.lctrl.Bind(wx.EVT_PAINT,self.onPaint)
        self.pw=self.GetComboCtrl().Size[0]
        self.ph=self.GetComboCtrl().Size[1]
        return True

    def GetControl(self):
        # Overrided;
        return self.lctrl

    def GetStringValue(self):
        # Overrided;
        return str(self.ipos)

    def OnDismiss(self):
        # Overrided;
        self.GetComboCtrl()._flag_active=False
        wx.ComboPopup.OnDismiss(self)
        return

    def onPaint(self,e):
        dc=wx.BufferedPaintDC(self.lctrl)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.lctrl.Size[0],self.lctrl.Size[1])
        dc.DrawLine(5,self.ph*(self.ipos+1),self.lctrl.Size[0]-5,self.ph*(self.ipos+1))

        dc.SetTextForeground(esui.COLOR_TEXT)
        pts=dc.GetTextExtent(self.GetComboCtrl().label)
        for i in range(len(self.items)):
            # if type(self.items[i])==tuple:
                # txt=self.items[i][0]+'.'+self.items[i][1]
            # else:
            txt=self.items[i]
            dc.DrawText(txt,(self.pw-pts[0])/2,i*self.ph+pts[1]/2)
        return

    def onClk(self,e):
        self.Dismiss()
        e.Skip()
        return

    def onMove(self,e):
        cpos=e.GetPosition()
        self.ipos=cpos[1]//self.ph
        self.lctrl.Refresh(eraseBackground=False)
        e.Skip()
        return
    pass

# Menu Btn wx sub class;
class MenuBtn(wx.ComboCtrl):
    def __init__(self,parent,p,s,label,items):
        super().__init__(parent,
            pos=p,size=s,value=label,style=wx.CB_READONLY)
        self.label=label
        self._flag_active=False
        self._flag_hover=False
        self.setItems(items)
        self.popup=self.PopupControl
        self.pop_ctrl=self.PopupControl.lctrl

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def setItems(self,items):
        try:
            popup=self.GetPopupControl()
            popup.items=items
            popup.ipos=0
        except BaseException:
            popup=PopupList(items)
            self.SetPopupControl(popup)
        self.SetPopupMaxHeight(len(items)*self.Size[1]+yu)
        self.SetPopupMinWidth(2*self.Size[0]+yu)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self._flag_active:
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self._flag_hover:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else:
            dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        dc.DrawPolygon([
            (self.Size[0]-1,self.Size[1]-1),
            (self.Size[0]-7,self.Size[1]-1),
            (self.Size[0]-1,self.Size[1]-7)])

        if self._flag_active:
            dc.SetTextForeground(esui.COLOR_BACK)
        else:
            dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.label)
        dc.DrawText(self.label,(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        self._flag_hover=True
        self.Refresh(eraseBackground=False)
        return

    def onLeave(self,e):
        self._flag_hover=False
        self.Refresh(eraseBackground=False)
        return

    def onClk(self,e):
        self._flag_active=True
        self.ShowPopup()
        self.GetPopupControl().lctrl.Refresh(eraseBackground=False)
        return

    def getCurrent(self)->str:
        return self.popup.items[self.popup.ipos]
    pass

class BorderlessMenuBtn(MenuBtn):
    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self._flag_active:
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self._flag_hover:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else:
            dc.SetBrush(wx.Brush(esui.COLOR_LBACK))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self._flag_active:
            dc.SetTextForeground(esui.COLOR_BACK)
        else:
            dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.label)
        dc.DrawText(self.label,(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)

        # dc.SetBrush(wx.Brush(esui.COLOR_TEXT))
        # dc.DrawPolygon([
        #     (self.Size[0]-1,self.Size[1]-1),
        #     (self.Size[0]-7,self.Size[1]-1),
        #     (self.Size[0]-1,self.Size[1]-7)])
        return

    pass

class SelectMenuBtn(MenuBtn):
    def setItems(self,items):
        try:
            popup=self.GetPopupControl()
            popup.items=items
            popup.ipos=0
        except BaseException:
            popup=PopupList(items)
            self.SetPopupControl(popup)
        self.SetPopupMaxHeight(len(items)*self.Size[1]+yu)
        self.SetPopupMinWidth(self.Size[0])
        self.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        popup=self.PopupControl
        self.label=popup.items[popup.ipos]
        self.SetValue(popup.items[popup.ipos])
        e.Skip()
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self._flag_active:
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self._flag_hover:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else:
            dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        dc.DrawPolygon([
            (self.Size[0]-1,self.Size[1]-1),
            (self.Size[0]-7,self.Size[1]-1),
            (self.Size[0]-1,self.Size[1]-7)])

        if self._flag_active:
            dc.SetTextForeground(esui.COLOR_BACK)
        else:
            dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.label)
        dc.DrawText(self.label,(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        # dc.DrawText(self.label,(yu,(self.Size[1]-tsize[1])/2))
        return
    pass
