# Parent lib;
import wx
from core import esui
gmv=esui.gmv

# Static text ctrl;
class Stc(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=(int(p[0]+1),int(p[1]+1)),
            size=(int(s[0]-2),int(s[1]-2)),
            label=txt,
            style=wx.NO_BORDER)
        self.align_type=align
        self.txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,'微软雅黑')
        self.SetFont(self.txtfont)
        # self.SetForegroundColour(gmv.COLOR_Text)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        bg=self.Parent.GetBackgroundColour()
        dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.Pen(bg))
        dc.DrawRectangle(1,1,self.Size[0]-2,self.Size[1]-2)

        dc.SetFont(self.GetFont())
        dc.SetTextForeground(gmv.COLOR_Text)
        dc.SetTextBackground(bg)
        tsize=dc.GetTextExtent(self.GetLabel())
        if self.align_type=='left':tx=0
        elif self.align_type=='right':tx=self.Size[0]-tsize[0]
        else:tx=(self.Size[0]-tsize[0])//2
        dc.DrawText(self.GetLabel(),tx,(self.Size[1]-tsize[1])//2)
        return
    def onClk(self,e):
        self.Parent.onClk(e)
        e.Skip()
        return
    pass

# Transparent StaticText wx sub class;
class Ttc(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,exstl=0,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            label=txt,
            style=wx.NO_BORDER | wx.TRANSPARENT_WINDOW | exstl)
        self.align_type=align
        txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,'微软雅黑')
        self.SetFont(txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(gmv.COLOR_Text)
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
    def __init__(self,parent,p,s,hint='',tsize=12,cn=''):
        wx.TextCtrl.__init__(self,parent,
            value=hint,
            name=cn,
            style=wx.NO_BORDER)
        self.SetBackgroundColour(gmv.COLOR_Back)
        self.SetForegroundColour(gmv.COLOR_Text)
        txtfont=wx.Font(int(tsize),wx.MODERN,wx.NORMAL,wx.NORMAL,False,'微软雅黑')
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
        dc.SetPen(wx.Pen(gmv.COLOR_Front,width=2))
        dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        dc.SetTextForeground(gmv.COLOR_Text)
        dc.DrawText(self.GetValue(),1,0)
        return

    def onEnter(self,e):
        self.on_etr=True
        self.SetBackgroundColour('#555555')
        e.Skip()
        return

    def onLeave(self,e):
        self.on_etr=False
        self.SetBackgroundColour(gmv.COLOR_Back)
        e.Skip()
        return
    pass
