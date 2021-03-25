# Parent lib;
import wx
# import numpy as np
from core import esui

# Static text ctrl;
class StaticText(wx.StaticText):
    def __init__(self,parent,p,s,txt,tsize=12,align='center'):
        wx.StaticText.__init__(self,parent,
            pos=(p[0]+1,p[1]+1),size=(s[0]-2,s[1]-2),
            label=txt,style=wx.NO_BORDER)
        self.align_type=align
        self.txtfont=esui.ESFont(size=tsize)
        self.SetFont(self.txtfont)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Refresh()
        return

    def onPaint(self,e):
        dc = wx.BufferedPaintDC(self)
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

    def setLabel(self,label):
        self.Label=label
        self.Refresh()
        return
    pass
# Transparent StaticText wx sub class;

# TextCtrl wx sub class;
class InputText(esui.Div):
    ''' Input text contorl.'''
    def __init__(self,parent,**argkw):
        ''' * Argkw hint: Hint text;
            * Argkw tsize: Text size. Half height default;
            * Argkw readonly: False default;'''
        super().__init__(parent,**argkw)
        self.updateStyle(style={'border_bottom':esui.COLOR_FRONT})
        hint=argkw.get('hint','')
        s=self.style['s']
        tsize=argkw.get('tsize',s[1]/2)
        readonly=argkw.get('readonly',0)
        if readonly:readonly=wx.TE_READONLY
        self.input=wx.TextCtrl(self,pos=(1,1),
            size=(s[0]-2,s[1]-2),
            style=wx.NO_BORDER | readonly)
        self.input.SetBackgroundColour(esui.COLOR_BACK)
        self.input.SetForegroundColour(esui.COLOR_TEXT)
        self.input.SetFont(esui.ESFont(size=tsize))
        self.input.SetValue(hint)

        self.setValue=self.input.SetValue
        self.getValue=self.input.GetValue
        self.input.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.input.Bind(wx.EVT_ENTER_WINDOW,self.onEnterInput)
        self.input.Bind(wx.EVT_LEAVE_WINDOW,self.onLeaveInput)
        return

    def onEnterInput(self,e):
        self.input.SetBackgroundColour(esui.COLOR_HOVER)
        e.Skip()
        return

    def onLeaveInput(self,e):
        self.input.SetBackgroundColour(esui.COLOR_BACK)
        e.Skip()
        return

    pass

# Multiline text ctrl;
class MultilineText(esui.ScrollDiv):
    def __init__(self,parent,tsize=12,**argkw):
        ''' Multiline text control.
            * Argkw cn: control name;
            * Argkw readonly: False default;
            * Argkw hint: Hint text;
            * Argkw tsize: Text size, 12 default;'''
        argkw['style']['border']=esui.COLOR_FRONT
        super().__init__(parent,**argkw)
        self.SetName(argkw.get('cn',''))
        if argkw.get('readonly',False):exstl=wx.TE_READONLY
        else:exstl=0
        # self.SetToolTip(hint)
        self.mtc=wx.TextCtrl(self,
            pos=(1,1),
            size=(argkw['style']['s'][0]-2,argkw['style']['s'][1]-2),
            value=argkw.get('hint',''),
            style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_NO_VSCROLL| exstl)
        self.mtc.SetBackgroundColour(esui.COLOR_BACK)
        self.mtc.SetForegroundColour(esui.COLOR_TEXT)
        self.mtc.SetFont(esui.ESFont(size=argkw.get('tsize',12)))
        self.mtc.Bind(wx.EVT_MOUSEWHEEL,self.onMtcRoWhl)
        self.setValue=self.mtc.SetValue
        self.getValue=self.mtc.GetValue
        self.appendText=self.mtc.AppendText
        return

    def onMtcRoWhl(self,e):
        # t=-1*np.sign(e.WheelRotation)
        if e.WheelRotation<0:self.mtc.PageDown()
        else:self.mtc.PageUp()
        return
    pass

class DivText(esui.Div):
    def __init__(self, parent: wx.Window, **argkw):
        ''' Text using div. LBACK bgc defalut
            Argkw label: Label text to display;'''
        argkw['passing']=True
        super().__init__(parent, **argkw)
        self.updateStyle(style={'bgc':esui.COLOR_LBACK})
        return
    pass

class HintText(esui.Div):
    ''' Hint Text. Destroy self after 1s.'''
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.timer_hide=wx.Timer(self)

        self.updateStyle(style={'bgc':esui.COLOR_LBACK})
        self.Bind(wx.EVT_TIMER,self.onHideTimer,self.timer_hide)
        self.timer_hide.StartOnce(1000)
        return

    def onHideTimer(self,e):
        self.DestroyLater()
        return
    pass

class TransText(esui.Div):
    ''' Transparent Text.'''
    def __init__(self,parent,**argkw):
        argkw['passing']=True
        super().__init__(parent,**argkw)
        self.updateStyle(style={'bgc':''})
        return
    pass
