import wx
from core import esui

# Btn wx sub class;
class Btn(wx.Button):
    def __init__(self,parent,p=(0,0),s=(0,0),txt='',**argkw):
        ''' Basic button.
            * Para argkw: enable/cn/tip/option.
            * Dict option: border/ext'''
        super().__init__(parent,pos=p,size=s,label=txt,style=wx.NO_BORDER)
        self._flag_hover=False
        self.option={'border':True,'ext':False}
        self.option.update(argkw.get('option',{}))
        if not self.option['border']:
            self.Move(p[0]+1,p[1]+1)
            self.SetSize(s[0]-2,s[1]-2)
        self.flag_enable=argkw.get('enable',True)
        self.SetToolTip(argkw.get('tip',''))
        self.SetName(argkw.get('cn',''))

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DCLICK,lambda e: None)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self._flag_hover:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        elif self.option['border']:
            dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        else:
            dc.SetBrush(wx.Brush(self.Parent.BackgroundColour))

        if self.option['border']:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        else:
            dc.SetPen(wx.Pen(self.Parent.BackgroundColour))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self.option['ext']:
            dc.SetBrush(wx.Brush(esui.COLOR_TEXT))
            dc.SetPen(wx.Pen(esui.COLOR_TEXT))
            dc.DrawRectangle(self.Size[0]-11,self.Size[1]-6,4,4)
            dc.DrawRectangle(self.Size[0]-5,self.Size[1]-6,4,4)

        if self.flag_enable: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_ACTIVE)
        tsize=dc.GetTextExtent(self.Label)
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        if not self.flag_enable:return
        self._flag_hover=True
        return

    def onLeave(self,e):
        if not self.flag_enable:return
        self._flag_hover=False
        return
    pass

# Select button wx sub class;
class SltBtn(wx.ToggleButton):
    ''' Para argkw: tip/enable/exclusive/select/cn/tsize'''
    def __init__(self,parent,p,s,label,**argkw):
        super().__init__(parent,pos=p,size=s,style=wx.NO_BORDER)
        self.option={'border':True,'ext':False}
        self.option.update(argkw.get('option',{}))
        if not self.option['border']:
            self.Move(p[0]+1,p[1]+1)
            self.SetSize(s[0]-2,s[1]-2)
        self._flag_hover=False
        self.flag_enable=argkw.get('enable',True)
        self.flag_exclusive=argkw.get('exclusive',False)
        self.SetToolTip(argkw.get('tip',''))
        self.txtfont=esui.ESFont(size=argkw.get('tsize',10))
        self.SetFont(self.txtfont)
        self.SetValue(argkw.get('select',False))
        self.SetLabel(label)
        self.SetName(argkw.get('cn',''))

        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DCLICK,lambda e: None)
        return

    def onClk(self,e):
        if not self.flag_enable: return
        if self.flag_exclusive:
            for ctrl in self.Parent.Children:
                if isinstance(ctrl,SltBtn):
                    ctrl.Value=False
                    ctrl.Refresh()
        self.SetValue(not self.Value)
        self.Refresh()
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.Value:
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        elif self._flag_hover:
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
        elif self.option['border']:
            dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        else:
            dc.SetBrush(wx.Brush(self.Parent.BackgroundColour))

        if self.option['border']:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        else:
            dc.SetPen(wx.Pen(self.Parent.BackgroundColour))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        if self.option['ext']:
            dc.SetBrush(wx.Brush(esui.COLOR_TEXT))
            dc.SetPen(wx.Pen(esui.COLOR_TEXT))
            dc.DrawRectangle(self.Size[0]-11,self.Size[1]-6,4,4)
            dc.DrawRectangle(self.Size[0]-5,self.Size[1]-6,4,4)

        if self.Value:dc.SetTextForeground(esui.COLOR_BACK)
        elif self.flag_enable: dc.SetTextForeground(esui.COLOR_TEXT)
        else: dc.SetTextForeground(esui.COLOR_ACTIVE)
        tsize=dc.GetTextExtent(self.Label)
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        if not self.flag_enable: return
        self._flag_hover=True
        e.Skip()
        return

    def onLeave(self,e):
        if not self.flag_enable: return
        self._flag_hover=False
        e.Skip()
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
        self._flag_hover=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        # if not ESC.isSimOpened():return
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
        self._flag_hover=True
        self.SetBackgroundColour(esui.COLOR_ACTIVE)
        return

    def onLeave(self,e):
        self._flag_hover=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        return
    pass
