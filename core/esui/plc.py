import wx
import numpy as np
import interval
from core import ESC
from core import esui
from core import esevt
# Panel container wx sub class;
class Plc(wx.Panel):
    '''Base container.

        Ctrl in Plc can only call other TopPlc;'''
    def __init__(self,parent,p,s,cn=''):
        super().__init__(parent,
            pos=p,
            size=s,
            name=cn,
            style=wx.NO_BORDER)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        bg=self.GetBackgroundColour()
        dc.SetPen(wx.Pen(bg))
        dc.SetBrush(wx.Brush(bg))
        dc.DrawRectangle((0,0),self.Size)
        return
    pass

class ScrolledPlc(wx.ScrolledWindow):
    def __init__(self,parent,p,s,cn='',axis='Y'):
        ''' Para axis: Y default for vertical scroll;

            Y for horizontal scroll;'''
        super().__init__(parent,pos=p,size=s,name=cn)
        self.axis=axis
        self.rx=0
        self.ry=0
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.SetScrollRate(int(esui.YU),int(esui.YU))
        self.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotateWheel)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
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
        dc=wx.BufferedPaintDC(self)
        dc.SetPen(wx.Pen(self.GetBackgroundColour()))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRectangle((0,0),self.Size)
        return

    def onRotateWheel(self,e):
        yu=esui.YU
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
        # dc=wx.ClientDC(self)
        # dc.Clear(eraseBackground=False)
        self.Refresh(eraseBackground=False)
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
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_OPEN_CMD)
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
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_CLOSE_CMD)
        e.Skip()
        return
    pass
