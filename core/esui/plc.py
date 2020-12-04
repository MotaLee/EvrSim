import wx
import numpy as np
import interval
from core import ESC
from core import esui
from core import esevt
yu=esui.YU
# Panel container wx sub class;
class Plc(wx.Panel):
    ''' Base container.

        Para argkw: cn/bgcolor/border.

        Ctrl in Plc can only call other TopPlc;'''
    def __init__(self,parent,p,s,**argkw):
        super().__init__(parent,pos=p,size=s,style=wx.NO_BORDER)
        cn=argkw.get('cn','')
        bgcolor=argkw.get('bgcolor',esui.COLOR_LBACK)
        self.border=argkw.get('border',{'all':None})
        self.SetName(cn)
        self.SetBackgroundColour(bgcolor)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        bg=self.GetBackgroundColour()
        dc.SetPen(wx.Pen(bg))
        dc.SetBrush(wx.Brush(bg))
        dc.DrawRectangle((0,0),self.Size)
        if 'all' in self.border:
            if self.border['all'] is None:return
            dc.SetPen(wx.Pen(self.border['all']))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle((0,0),self.Size)
        if 'up' in self.border:
            dc.SetPen(wx.Pen(self.border['up']))
            dc.DrawLine(0,1,self.Size.x,1)
        if 'bottom' in self.border:
            dc.SetPen(wx.Pen(self.border['bottom']))
            dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        if 'left' in self.border:
            dc.SetPen(wx.Pen(self.border['left']))
            dc.DrawLine(1,0,1,self.Size.y)
        if 'right' in self.border:
            dc.SetPen(wx.Pen(self.border['right']))
            dc.DrawLine(self.Size.x-1,0,self.Size.x-1,self.Size.y)
        return
    pass

class ScrolledPlc(wx.ScrolledWindow):
    ''' Para argkw: cn/bgcolor/border/axis.

        `axis`: Y default for vertical scroll, X for horizontal scroll.'''
    def __init__(self,parent,p,s,**argkw):
        super().__init__(parent,pos=p,size=s)
        cn=argkw.get('cn','')
        self.rx=0
        self.ry=0
        self.axis=argkw.get('axis','Y')
        self.border=argkw.get('border',{'all':None})
        self.SetName(cn)
        bgcolor=argkw.get('bgcolor',esui.COLOR_LBACK)
        self.SetBackgroundColour(bgcolor)
        self.SetScrollRate(int(esui.YU),int(esui.YU))
        self.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotateWheel)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        return

    def updateVirtualSize(self):
        max_width=0
        max_height=0
        for ctrl in self.Children:
            max_width=max(max_width,ctrl.Position[0]+ctrl.Size[0])
            max_height=max(max_height,ctrl.Position[1]+ctrl.Size[1])
        max_width=max(max_width,self.Size[0])
        max_height=max(max_height,self.Size[1])
        self.SetVirtualSize(max_width,max_height)
        self.Refresh()
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        bg=self.GetBackgroundColour()
        dc.SetPen(wx.Pen(bg))
        dc.SetBrush(wx.Brush(bg))
        dc.DrawRectangle((0,0),self.Size)
        if 'all' in self.border:
            if self.border['all'] is None:return
            dc.SetPen(wx.Pen(self.border['all']))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle((0,0),self.Size)
        if 'up' in self.border:
            dc.SetPen(wx.Pen(self.border['up']))
            dc.DrawLine(0,1,self.Size.x,1)
        if 'bottom' in self.border:
            dc.SetPen(wx.Pen(self.border['bottom']))
            dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        if 'left' in self.border:
            dc.SetPen(wx.Pen(self.border['left']))
            dc.DrawLine(1,0,1,self.Size.y)
        if 'right' in self.border:
            dc.SetPen(wx.Pen(self.border['right']))
            dc.DrawLine(self.Size.x-1,0,self.Size.x-1,self.Size.y)
        return

    def onRotateWheel(self,e):
        t=-1*np.sign(e.WheelRotation)

        if self.axis=='X':
            rx_max=(self.VirtualSize[0]-self.Size[0])/yu
            if self.rx+t not in interval.Interval(0,rx_max):return
            self.rx+=t
        elif self.axis=='Y':
            ry_max=(self.VirtualSize[1]-self.Size[1])/yu
            if self.ry+t not in interval.Interval(0,ry_max):return
            self.ry+=t
        self.Scroll(self.rx,self.ry)
        dc=wx.ClientDC(self)
        dc.Clear()
        dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        if self.axis=='X':
            'todo: x axis scroll test'
            dc.DrawRectangle(self.Size[1]-0.75*yu,
                self.rx*yu*(self.Size[0]/self.VirtualSize[0]),
                0.5*yu,
                self.Size[0]**2/self.VirtualSize[0])
        elif self.axis=='Y':
            dc.DrawRectangle(self.Size[0]-0.75*yu,
                self.ry*yu*(self.Size[1]/self.VirtualSize[1]),
                0.5*yu,
                self.Size[1]**2/self.VirtualSize[1])
        return

    def onLeave(self,e):
        self.Refresh(eraseBackground=False)
        return
    pass

class CmdPlc(Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        xu=esui.XU
        yu=esui.YU
        self.histxt=esui.MultilineText(self,(0,0),(75*xu,17*yu),exstl=wx.TE_READONLY)
        self.comhead=esui.StaticText(self,(yu,17*yu),(8*xu,4*yu),'EvrSim>>',align='left')
        self.comtxt=esui.InputText(self,(9*yu,17*yu),(75*xu-10*yu,4*yu),exstl=wx.TE_PROCESS_ENTER)
        # est=subprocess.Popen('python est.py wx',
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     universal_newlines=True,encoding='utf-8')
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.comtxt.Bind(wx.EVT_TEXT_ENTER,self.onCmd)
        self._bug=ESC.bug
        ESC.bug=self.bug

        self.Hide()
        return

    def bug(self,bugstr,report=False):
        # self._bug(bugstr,report)
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_OPEN_CMD)
        self.histxt.AppendText(bugstr+'\n')
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle((0,0),self.Size)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_OPEN_CMD:
            self.Show()
        elif etype==esevt.ETYPE_CLOSE_CMD:
            self.Hide()
        elif etype==esevt.ETYPE_KEY_DOWN:
            self.onKeyDown(e.GetEventArgs(1))
        return

    def onCmd(self,e):
        self.histxt.AppendText('EvrSim>>'+e.String+'\n')
        self.histxt.Refresh()
        return

    def onKeyDown(self,e):
        if e.GetKeyCode()==wx.WXK_ESCAPE:
            esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_CLOSE_CMD)
        e.Skip()
        return
    pass

class PopupPlc(Plc):
    def __init__(self,parent,p,s,**argkw):
        super().__init__(parent,p,s,border={'all':esui.COLOR_FRONT})
        self.mode=argkw.get('mode',None)
        # if self.mode=='list':
            # list_items=argkw.get('list_items',list())
            # list_height=argkw.get('list_height',4*yu)

        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        e.Skip()
        self.DestroyLater()
        return
    pass
