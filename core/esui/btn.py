import wx
from core import esui

# Btn wx sub class;
class Btn(wx.Button):
    def __init__(self,parent,p=wx.DefaultPosition,s=wx.DefaultSize,txt='',able=True,tip='',cn=''):
        wx.Button.__init__(self,parent,
            pos=p,
            size=s,
            label=txt,
            name=cn,
            style=wx.NO_BORDER)
        self.on_ctrl=False
        self.btn_able=able
        self.SetToolTip(tip)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.on_ctrl: dc.SetBrush(wx.Brush(esui.COLOR_SECOND))
        else: dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        if self.btn_able: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_SECOND)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        if not self.btn_able:return
        self.on_ctrl=True
        return

    def onLeave(self,e):
        if not self.btn_able:return
        self.on_ctrl=False
        return
    pass

class BorderlessBtn(Btn):
    def __init__(self,parent,p,s,blbtnlabel,able=True,tip='',cn=''):
        Btn.__init__(self,parent,
            (int(p[0]+1),int(p[1]+1)),
            (int(s[0]-2),int(s[1]-2)),
            blbtnlabel,able,tip,cn)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        clr=self.Parent.BackgroundColour
        if self.on_ctrl: dc.SetBrush(wx.Brush(esui.COLOR_SECOND))
        else: dc.SetBrush(wx.Brush(clr))
        dc.SetPen(wx.Pen(clr))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1],self.Size[0],self.Size[1])
        if self.btn_able: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_SECOND)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return
    pass

# Select button wx sub class;
class SelectBtn(wx.ToggleButton):
    on_ctrl=False
    enable_ctrl=True
    def __init__(self,parent,p,s,txt,tip='',select=False,enable=True,tsize=10,cn=''):
        wx.ToggleButton.__init__(self,parent,
            name=cn,
            pos=p,
            size=s,
            label=txt,
            style=wx.NO_BORDER)
        self.enable_ctrl=enable

        self.SetToolTip(tip)
        self.txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,'Microsoft YaHei')
        self.SetFont(self.txtfont)
        self.SetValue(select)

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
        elif self.on_ctrl:dc.SetBrush(wx.Brush(esui.COLOR_SECOND))
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
        return

    def onLeave(self,e):
        if not self.enable_ctrl: return
        self.on_ctrl=False
        return
    pass

class BlSelectBtn(SelectBtn):
    ''' Borderless Select Button.'''
    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.GetValue():
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self.on_ctrl:
            dc.SetBrush(wx.Brush(esui.COLOR_SECOND))
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
        self.SetBackgroundColour(esui.COLOR_SECOND)
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        return
    pass
