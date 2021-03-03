import wx,interval,copy
import numpy as np
from core import ESC,esui,esevt
yu=esui.YU
Itv=interval.Interval
# Panel container wx sub class;
class Plc(wx.Panel):
    ''' Base container.

        Para argkw: cn/bgcolor/border.

        Ctrl in Plc can only call other TopPlc;'''
    def __init__(self,parent,p,s,**argkw):
        super().__init__(parent,pos=p,size=s,style=wx.NO_BORDER)
        self._flag_hover=False
        self.border=argkw.get('border',{'all':None})
        self.SetName(argkw.get('cn',''))
        self.SetBackgroundColour(argkw.get('bgcolor',esui.COLOR_LBACK))
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
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

    def onEnter(self,e):
        self._flag_hover=True
        self.Refresh()
        return

    def onLeave(self,e):
        self._flag_hover=False
        self.Refresh()
        return

    pass

class ScrolledPlc(wx.ScrolledWindow):

    def __init__(self,parent,p,s,**argkw):
        ''' Para argkw: cn/bgcolor/border/axis.

            `axis`: Y default for vertical scroll, X for horizontal scroll.'''
        super().__init__(parent,pos=p,size=s)
        self.rx=0
        self.ry=0
        self.axis=argkw.get('axis','Y')
        self.border=argkw.get('border',{'all':None})
        self.SetName(argkw.get('cn',''))
        self.SetBackgroundColour(argkw.get('bgcolor',esui.COLOR_LBACK))
        self.SetScrollRate(int(esui.YU),int(esui.YU))
        self.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotateWheel)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        return

    def updateVirtualSize(self):
        max_width=max([
            ctrl.Position[0]+ctrl.Size[0] for ctrl in self.Children]+[self.Size[0]])
        max_height=max([
            ctrl.Position[1]+ctrl.Size[1] for ctrl in self.Children]+[self.Size[1]])
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
        self._bug=ESC.err
        ESC.err=self.bug

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

class Div(wx.Panel):
    def __init__(self,parent:wx.Window,**argkw):
        ''' Styled div control. Para argkw including:
            * label: a text showing in control;
            * style: A dict allowed following keys:
                * `p`: position, zreos default. `(int,int)`;
                * `s`: size, zreos default. `(int,int)`;
                * `bgc`: background color, COLOR_LBACK default;
                * `fgc`: foreground color, COLOR_FRONT default;
                * `bgi`: background image path;
                * `border`: all border color;
                * `border_width`: all border width;
                * `border_dir`: one side border color, dir for up/bottom/left/right;
                * `border_dir_width`: one side border width;
                * `text`: text color;
            * active: A style dict applied when active;
            * hover: A style dict applied when mouse on;'''
        super().__init__(parent,style=wx.NO_BORDER)
        self._flag_hover=False
        self._flag_active=False
        self._bgi=None
        self._style_cache=dict()

        self.parent=parent
        self.label=argkw.get('label','')
        self.style=copy.deepcopy(esui.STL_DFT)
        self.style_active=dict()
        self.style_hover=dict()
        self.updateStyle(**argkw)

        self.Bind(wx.EVT_PAINT,self._onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Bind(wx.EVT_LEFT_DOWN,self._onClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self._onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self._onLeave)
        return

    def _onPaint(self,e):
        dc=wx.PaintDC(self)
        self._style_cache=copy.deepcopy(self.style)
        if self._flag_active:
            self.style.update(self.style_active)
        if self._flag_hover:
            self.style.update(self.style_hover)

        dc.SetPen(wx.Pen(self.style['bgc']))
        dc.SetBrush(wx.Brush(self.style['bgc']))
        dc.DrawRectangle((0,0),self.Size)
        if 'bgi' in self.style:
            dc.DrawBitmap(self._bgi,0,0)

        border_width_all=self.style.get('border_width',1)
        if 'border_up' in self.style:
            bw=self.style.get('border_up_width',border_width_all)
            dc.SetPen(wx.Pen(self.style['border_up'],width=bw))
            dc.DrawLine(0,1,self.Size.x,1)
        if 'border_bottom' in self.style:
            bw=self.style.get('border_bottom_width',border_width_all)
            dc.SetPen(wx.Pen(self.style['border_bottom'],width=bw))
            dc.DrawLine(0,self.Size.y-1,self.Size.x,self.Size.y-1)
        if 'border_left' in self.style:
            bw=self.style.get('border_left_width',border_width_all)
            dc.SetPen(wx.Pen(self.style['border_left'],width=bw))
            dc.DrawLine(1,0,1,self.Size.y)
        if 'border_right' in self.style:
            bw=self.style.get('border_right_width',border_width_all)
            dc.SetPen(wx.Pen(self.style['border_right'],width=bw))
            dc.DrawLine(self.Size.x-1,0,self.Size.x-1,self.Size.y)

        if 'border' in self.style:
            dc.SetPen(wx.Pen(self.style['border'],
                width=border_width_all))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle((0,0),self.Size)
        if self.label!='':
            dc.SetTextForeground(self.style['text'])
            tsize=dc.GetTextExtent(self.label)
            dc.DrawText(self.label,(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        self.style=copy.deepcopy(self._style_cache)
        return

    def updateStyle(self,**argkw):
        if 'style' in argkw:
            self.style.update(argkw.get('style',{}))
        if 'active' in argkw:
            self.style_active.update(argkw.get('active',{}))
        if 'hover' in argkw:
            self.style_hover.update(argkw.get('hover',{}))

        self.SetSize(self.style['s'])
        self.SetPosition(self.style['p'])
        self.BackgroundColour=self.style['bgc']
        self.ForegroundColour=self.style['fgc']
        if 'bgi' in self.style:
            self._bgi=wx.Image(self.style['bgi']).Scale(
                self.Size[0],self.Size[1]).ConvertToBitmap()
        self.Refresh()
        return

    def _onClk(self,e:wx.Event):
        self.toggleActive()
        e.Skip()
        return

    def _onEnter(self,e:wx.Event):
        self._flag_hover=True
        self.Refresh()
        e.Skip()
        return

    def _onLeave(self,e:wx.Event):
        self._flag_hover=False
        self.Refresh()
        e.Skip()
        return

    def toggleActive(self,active=None):
        if active is None:
            self._flag_active=not self._flag_active
        else:
            self._flag_active=active
        self.Refresh()
        return

    def isActive(self):
        return self._flag_active
    pass

class ScrollDiv(Div):
    def __init__(self, parent: wx.Window, **argkw):
        ''' Scrollable div.
            * `axis` : 'Y' default for vertical scroll, 'X' for horizontal;
            * `bar` : if display scroll bar,False default;'''
        super().__init__(parent, **argkw)
        self.rx=0   # Current x;
        self.ry=0   # Current y;
        self.mx=self.Size[0]    # Max width;
        self.my=self.Size[1]    # Max height;
        self.axis=argkw.get('axis','Y')
        self._flag_bar=argkw.get('bar',False)
        self.div_bar=Div(self,style={
            'p':(self.Size[0]-0.75*yu,yu),
            's':(yu/2,self.Size[1]-2*yu),
            'bgc':esui.COLOR_FRONT})
        self._list_block=[self.div_bar]

        if not self._flag_bar:self.div_bar.Hide()
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotWhl)
        self.Bind(wx.EVT_LEAVE_WINDOW,self._onLeave)
        return

    def scroll(self,dx,dy):
        dx=int(dx*yu)
        dy=int(dy*yu)
        self.rx+=dx
        self.ry+=dy
        for ctrl in self.Children:
            ctrl.SetPosition((ctrl.Position[0]-dx,ctrl.Position[1]-dy))
        return

    def updateMaxSize(self):
        xlist=[self.Size[0]]
        ylist=[self.Size[1]]
        for ctrl in self.Children:
            if ctrl.Shown and ctrl not in self._list_block:
                xlist.append(ctrl.Position[0]+ctrl.Size[0])
                ylist.append(ctrl.Position[1]+ctrl.Size[1])
        self.mx=max(xlist)
        self.my=max(ylist)
        if self.axis=='X':
            self.div_bar.SetSize(self.Size[1]**2/self.mx,yu/2)
        else:
            self.div_bar.SetSize(yu/2,self.Size[1]**2/self.my)
        self.Refresh()
        return

    def onRotWhl(self,e):
        t=-1*np.sign(e.WheelRotation)
        if self.axis=='X':
            if self.rx+t*yu not in Itv(0,self.mx-self.Size[0]):return
            self.scroll(t,0)
            self.div_bar.SetPosition((
                self.Size[1]-0.75*yu,
                self.rx*(self.Size[0]/self.mx)))
        elif self.axis=='Y':
            if self.ry+t*yu not in Itv(0,self.my-self.Size[1]):return
            self.scroll(0,t)
            self.div_bar.SetPosition((
                self.Size[0]-0.75*yu,
                self.ry*(self.Size[1]/self.my)))
        self.div_bar.Show()
        for ctrl in self.Children:
            ctrl.Refresh()
        return

    def getChildren(self):
        children=[ctrl for ctrl in self.Children if ctrl not in self._list_block]
        return children

    def delChildren(self):
        for ctrl in self.Children:
            if ctrl not in self._list_block:
                ctrl.Destroy()
        return

    def _onLeave(self,e:wx.Event):
        if not self._flag_bar:self.div_bar.Hide()
        super()._onLeave(e)
        return
    pass
