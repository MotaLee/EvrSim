import wx
from core import esui

# Btn wx sub class;
class Btn(wx.Button):
    ''' Basic button.

        Para argkw: label/enable/cn/tip.'''
    def __init__(self,parent,p=wx.DefaultPosition,s=wx.DefaultSize,label='',**argkw):
        super().__init__(parent,pos=p,size=s,label=label,style=wx.NO_BORDER)
        enable=argkw.get('enable',True)
        cn=argkw.get('cn','')
        tip=argkw.get('tip','')
        self.on_ctrl=False
        self.enable=enable
        self.SetToolTip(tip)
        self.SetName(cn)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.on_ctrl: dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else: dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        if self.enable: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_ACTIVE)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        if not self.enable:return
        self.on_ctrl=True
        return

    def onLeave(self,e):
        if not self.enable:return
        self.on_ctrl=False
        return
    pass

class BorderlessBtn(Btn):
    def __init__(self,parent,p,s,label,**argkw):
        super().__init__(parent,(p[0]+1,p[1]+1),(s[0]-2,s[1]-2),label,**argkw)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        clr=self.Parent.BackgroundColour
        if self.on_ctrl: dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else: dc.SetBrush(wx.Brush(clr))
        dc.SetPen(wx.Pen(clr))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1],self.Size[0],self.Size[1])
        if self.enable: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_ACTIVE)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return
    pass

# Select button wx sub class;
class SelectBtn(wx.ToggleButton):
    ''' Para argkw: tip/enable/select/cn/tsize'''
    def __init__(self,parent,p,s,txt,**argkw):
        super().__init__(parent,pos=p,size=s,style=wx.NO_BORDER)
        enable=argkw.get('enable',True)
        select=argkw.get('select',False)
        cn=argkw.get('cn','')
        tip=argkw.get('tip','')
        tsize=argkw.get('tsize',10)

        self.on_ctrl=False
        self.enable_ctrl=enable
        self.SetToolTip(tip)
        self.txtfont=esui.ESFont(size=tsize)
        self.SetFont(self.txtfont)
        self.SetValue(select)
        self.SetLabel(txt)
        self.SetName(cn)

        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_DCLICK,lambda e: None)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onClk(self,e):
        if not self.enable_ctrl: return
        self.SetValue(not self.GetValue())
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.GetValue(): dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self.on_ctrl:dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else:dc.SetBrush(wx.Brush(esui.COLOR_BACK))

        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self.GetValue():dc.SetTextForeground(esui.COLOR_BACK)
        else: dc.SetTextForeground(esui.COLOR_TEXT)
        dc.SetFont(self.txtfont)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        if not self.enable_ctrl: return
        self.on_ctrl=True
        e.Skip()
        return

    def onLeave(self,e):
        if not self.enable_ctrl: return
        self.on_ctrl=False
        e.Skip()
        return
    pass

class BlSelectBtn(SelectBtn):
    ''' Borderless Select Button.'''
    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.GetValue():
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self.on_ctrl:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        else:
            bg=self.Parent.GetBackgroundColour()
            dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self.GetValue():dc.SetTextForeground(esui.COLOR_BACK)
        else: dc.SetTextForeground(esui.COLOR_TEXT)
        dc.SetFont(self.txtfont)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2,)
        return
    pass

# Tab Btn wx sub class;
class TabBtn(wx.ToggleButton):
    ''' Label of Btn and its tab must be the same.'''
    def __init__(self,parent,p,s,tablabel,cn=''):
        wx.ToggleButton.__init__(self,parent,
            pos=p,
            size=s,
            label=tablabel,
            name=cn,
            style=wx.NO_BORDER)
        self.on_ctrl=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        # if ESC.SIM_FD is None:return
        self.SetValue(True)
        for ctrl in self.Parent.Children:
            if type(ctrl)==TabBtn and ctrl!=self:
                ctrl.SetValue(False)
            if isinstance(ctrl,(wx.Panel,wx.ScrolledWindow)):
                if ctrl.GetLabel()==self.GetLabel():
                    ctrl.Show()
                else: ctrl.Hide()
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.GetValue(): pw=8
        else:pw=1
        dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=pw))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        self.on_ctrl=True
        self.SetBackgroundColour(esui.COLOR_ACTIVE)
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        return
    pass
