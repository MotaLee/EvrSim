# Parent lib;
import core.esui as esui
wx=esui.wx
gmv=esui.gmv

# Btn wx sub class;
class btn(wx.Button):
    def __init__(self,parent,p=wx.DefaultPosition,s=wx.DefaultSize,txt='',able=True,tip='',cn=''):
        wx.Button.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
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
        if self.on_ctrl: dc.SetBrush(wx.Brush('#555555'))
        else: dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        if self.btn_able: dc.SetTextForeground(gmv.COLOR_Text)
        else: dc.SetTextForeground('#555555')
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

class BorderlessBtn(btn):
    def __init__(self,parent,p,s,blbtnlabel,able=True,tip='',cn=''):
        btn.__init__(self,parent,
            (int(p[0]+1),int(p[1]+1)),
            (int(s[0]-2),int(s[1]-2)),
            blbtnlabel,able,tip,cn)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        clr=self.Parent.BackgroundColour
        if self.on_ctrl: dc.SetBrush(wx.Brush('#555555'))
        else: dc.SetBrush(wx.Brush(clr))
        dc.SetPen(wx.Pen(clr))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,self.Size[1],self.Size[0],self.Size[1])
        if self.btn_able: dc.SetTextForeground(gmv.COLOR_Text)
        else: dc.SetTextForeground('#555555')
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return
    pass

# Select button wx sub class;
class SelectBtn(wx.ToggleButton):
    on_ctrl=False
    enable_ctrl=True
    def __init__(self,parent,p,s,txt,tip='',select=False,enable=True,tsize=12):
        wx.ToggleButton.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            label=txt,
            style=wx.NO_BORDER)
        self.enable_ctrl=enable
        self.SetToolTip(tip)
        self.txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,'微软雅黑')
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
        # dc.Clear()
        if self.GetValue(): dc.SetBrush(wx.Brush(gmv.COLOR_Front))
        elif self.on_ctrl:dc.SetBrush(wx.Brush(gmv.COLOR_Second))
        else:dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        if self.GetValue():dc.SetTextForeground(gmv.COLOR_Back)
        else: dc.SetTextForeground(gmv.COLOR_Text)
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
