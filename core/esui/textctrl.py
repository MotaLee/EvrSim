# Parent lib;
import wx
from core import esui
gmv=esui

# Static text ctrl;
class Stc(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=(int(p[0]+1),int(p[1]+1)),
            size=(int(s[0]-2),int(s[1]-2)),
            label=txt,
            style=wx.NO_BORDER)
        self.align_type=align
        self.txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,esui.TEXT_FONT)
        self.SetFont(self.txtfont)
        # self.SetForegroundColour(esui.COLOR_Text)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        bg=self.Parent.GetBackgroundColour()
        dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.Pen(bg))
        dc.DrawRectangle(1,1,self.Size[0]-2,self.Size[1]-2)

        dc.SetFont(self.GetFont())
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.SetTextBackground(bg)
        tsize=dc.GetTextExtent(self.GetLabel())
        if self.align_type=='left':tx=0
        elif self.align_type=='right':tx=self.Size[0]-tsize[0]
        else:tx=(self.Size[0]-tsize[0])//2
        dc.DrawText(self.GetLabel(),tx,(self.Size[1]-tsize[1])//2)
        return
    def onClk(self,e):
        if hasattr(self.Parent,'onClk'):
            self.Parent.onClk(e)
        e.Skip()
        return
    def onDClk(self,e):
        if hasattr(self.Parent,'onDClk'):
            self.Parent.onDClk(e)
        e.Skip()
        return
    pass

# Transparent StaticText wx sub class;
class Ttc(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,exstl=0,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=p,
            size=s,
            label=txt,
            style=wx.NO_BORDER | wx.TRANSPARENT_WINDOW | exstl)
        self.align_type=align
        txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,esui.TEXT_FONT)
        self.SetFont(txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.GetLabel())
        if self.align_type=='left':
            tx=0
        elif self.align_type=='right':
            tx=self.Size[0]-tsize[0]
        else:
            tx=(self.Size[0]-tsize[0])//2
        dc.DrawText(self.GetLabel(),tx,(self.Size[1]-tsize[1])//2)
        return
    pass

# TextCtrl wx sub class;
class Tcc(wx.TextCtrl):
    def __init__(self,parent,p,s,hint='',tsize=12,cn='',tip='',exstl=0):
        super().__init__(parent,
            value=hint,
            name=cn,
            style=wx.NO_BORDER | exstl)
        self.SetToolTip(tip)
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.SetForegroundColour(esui.COLOR_TEXT)
        txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,esui.TEXT_FONT)
        self.SetFont(txtfont)
        # self.SetLabel(label)

        cdc=wx.ClientDC(self)
        ts=cdc.GetTextExtent('hint')
        margin=(s[1]-ts[1])/2
        self.on_etr=False
        self.SetPosition((int(p[0]),int(p[1]+margin)))
        self.SetSize((int(s[0]),int(s[1]-margin)))

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        # dc.Clear()
        dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=1))
        dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.DrawText(self.GetValue(),1,0)
        return

    def onEnter(self,e):
        self.on_etr=True
        self.SetBackgroundColour(esui.COLOR_SECOND)
        e.Skip()
        return

    def onLeave(self,e):
        self.on_etr=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        e.Skip()
        return
    pass

# Multiline text ctrl;
class Mtc(wx.TextCtrl):
    def __init__(self,parent,p,s,hint='',tsize=12,cn='',exstl=0):
        wx.TextCtrl.__init__(self,parent,
            pos=p,
            size=s,
            value=hint,
            name=cn,
            style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_NO_VSCROLL| exstl)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.SetForegroundColour(esui.COLOR_TEXT)
        txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,esui.TEXT_FONT)
        self.SetFont(txtfont)

        cdc=wx.ClientDC(self)
        ts=cdc.GetTextExtent('hint')
        margin=(s[1]-ts[1])/2
        self.on_etr=False
        # self.SetPosition((int(p[0]),int(p[1]+margin)))
        # self.SetSize((int(s[0]),int(s[1]-margin)))

        self.Bind(wx.EVT_PAINT,self.onPaint)
        # self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        # self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_LBACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size.x,self.Size.y)
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.DrawText(self.GetValue(),3,0)
        return

    def onEnter(self,e):
        self.on_etr=True
        self.SetBackgroundColour(esui.COLOR_SECOND)
        e.Skip()
        return

    def onLeave(self,e):
        self.on_etr=False
        self.SetBackgroundColour(esui.COLOR_BACK)
        e.Skip()
        return
    pass
