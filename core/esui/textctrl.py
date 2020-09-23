# Parent lib;
import wx
# import numpy as np
from core import esui

# Static text ctrl;
class StaticText(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=(p[0]+1,p[1]+1),
            size=(s[0]-2,s[1]-2),label=txt,style=wx.NO_BORDER)
        self.align_type=align
        self.txtfont=esui.ESFont(size=tsize)
        self.SetFont(self.txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Refresh()
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        bg=self.Parent.GetBackgroundColour()
        dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.Pen(bg))
        dc.DrawRectangle((0,0),self.Size)

        dc.SetFont(self.GetFont())
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.SetTextBackground(bg)
        tsize=dc.GetTextExtent(self.GetLabel())
        if self.align_type=='left':tx=0
        elif self.align_type=='right':tx=self.Size[0]-tsize[0]
        else:tx=(self.Size[0]-tsize[0])//2
        dc.DrawText(self.GetLabel(),tx,(self.Size[1]-tsize[1])//2)
        return
    pass
# Transparent StaticText wx sub class;
class TransText(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        super().__init__(parent,pos=p,size=s,label=txt,
            style=wx.NO_BORDER | wx.TRANSPARENT_WINDOW)
        self.align=align
        self.txtfont=esui.ESFont(size=tsize)
        self.SetFont(self.txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(esui.COLOR_TEXT)
        tsize=dc.GetTextExtent(self.GetLabel())
        if self.align=='left':tx=0
        elif self.align=='right':tx=self.Size.x-tsize[0]
        else:tx=(self.Size.x-tsize[0])//2
        dc.DrawText(self.GetLabel(),tx,(self.Size.y-tsize[1])//2)
        return
    pass
# TextCtrl wx sub class;
class InputText(esui.Plc):
    ''' Para argkw: hint, tsize, tip, exstl.'''
    def __init__(self,parent,p,s,cn='',**argkw):
        super().__init__(parent,p,s,cn=cn)
        hint=argkw.get('hint','')
        tsize=argkw.get('tsize',s[1]/2)
        tip=argkw.get('tip','')
        exstl=argkw.get('exstl',0)
        self.input=wx.TextCtrl(self,value=hint,
            pos=(1,1),size=(s[0]-2,s[1]-2),
            style=wx.NO_BORDER | exstl)
        self.SetToolTip(tip)
        self.input.SetBackgroundColour(esui.COLOR_BACK)
        self.input.SetForegroundColour(esui.COLOR_TEXT)
        txtfont=esui.ESFont(size=tsize)
        self.input.SetFont(txtfont)
        self.input.SetValue(hint)

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.input.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.SetValue=self.input.SetValue
        self.GetValue=self.input.GetValue
        self.input.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.input.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        bg=self.GetBackgroundColour()
        dc.SetPen(wx.Pen(bg))
        dc.SetBrush(wx.Brush(bg))
        dc.DrawRectangle((0,0),self.Size)
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        return

    def onEnter(self,e):
        self.input.SetBackgroundColour(esui.COLOR_ACTIVE)
        e.Skip()
        return

    def onLeave(self,e):
        self.input.SetBackgroundColour(esui.COLOR_BACK)
        e.Skip()
        return
    pass
# Multiline text ctrl;
class MultilineText(esui.ScrolledPlc):
    def __init__(self,parent,p,s,hint='',tsize=12,cn='',exstl=0):
        super().__init__(parent,p,s,cn=cn)
        self.mtc=wx.TextCtrl(self,
            pos=(1,1),
            size=(s[0]-2,s[1]-2),
            value=hint,
            style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_NO_VSCROLL| exstl)
        self.mtc.SetBackgroundColour(esui.COLOR_BACK)
        self.mtc.SetForegroundColour(esui.COLOR_TEXT)
        txtfont=esui.ESFont(size=tsize)
        self.mtc.SetFont(txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.mtc.Bind(wx.EVT_MOUSEWHEEL,self.onMtcRoWhl)
        self.SetValue=self.mtc.SetValue
        self.GetValue=self.mtc.GetValue
        self.AppendText=self.mtc.AppendText
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(0,0,self.Size.x,self.Size.y)
        return

    def onMtcRoWhl(self,e):
        # t=-1*np.sign(e.WheelRotation)
        if e.WheelRotation<0:
            self.mtc.PageDown()
        else:
            self.mtc.PageUp()
        return
    pass

class HintText(TransText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        super().__init__(parent,p,s,txt,tsize,align)
        self.hide_timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onHideTimer,self.hide_timer)
        self.hide_timer.StartOnce(1000)
        return

    def onHideTimer(self,e):
        self.DestroyLater()
        return
    pass
