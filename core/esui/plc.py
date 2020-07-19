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
        wx.Panel.__init__(self,parent,
            pos=p,
            size=s,
            name=cn,
            style=wx.NO_BORDER)
        self.SetBackgroundColour(esui.COLOR_BACK)
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
        # self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
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
        dc.SetPen(wx.Pen(esui.COLOR_SECOND))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRectangle((0,0),self.Size)
        return

    def onRotateWheel(self,e):
        t=-1*np.sign(e.WheelRotation)

        if self.axis=='X':
            rx_max=(self.VirtualSize[0]-self.Size[0])/esui.YU
            if self.rx+t not in interval.Interval(0,rx_max):return
            self.rx+=t
        elif self.axis=='Y':
            ry_max=(self.VirtualSize[1]-self.Size[1])/esui.YU
            if self.ry+t not in interval.Interval(0,ry_max):return
            self.ry+=t
        self.Scroll(self.rx,self.ry)
        dc=wx.ClientDC(self)
        dc.Clear()
        dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        if self.axis=='X':
            'totest: x axis scroll'
            dc.DrawRectangle(self.Size[1]-0.75*esui.YU,
                self.rx*esui.YU*(1+self.Size[0]/self.VirtualSize[0]),
                0.5*esui.YU,
                self.Size[0]**2/self.VirtualSize[0])
        elif self.axis=='Y':
            dc.DrawRectangle(self.Size[0]-0.75*esui.YU,
                self.ry*esui.YU*(1+self.Size[1]/self.VirtualSize[1]),
                0.5*esui.YU,
                self.Size[1]**2/self.VirtualSize[1])
        return

    def onLeave(self,e):
        # dc=wx.ClientDC(self)
        # dc.Clear(eraseBackground=False)
        self.Refresh(eraseBackground=False)
    pass

class ComPlc(Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'compl')
        xu=esui.XU
        yu=esui.YU
        self.histxt=esui.Mtc(self,(0,0),(75*xu,17*yu),exstl=wx.TE_READONLY)
        self.comhead=esui.Stc(self,(yu,17*yu),(8*xu,4*yu),'EvrSim>>',align='left')
        self.comtxt=esui.Tcc(self,(9*yu,17*yu),(75*xu-10*yu,4*yu),exstl=wx.TE_PROCESS_ENTER)
        # tsize=1.5*yu,exstl=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL)
        # est=subprocess.Popen('python est.py wx',
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     universal_newlines=True,encoding='utf-8')
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.comtxt.Bind(wx.EVT_TEXT_ENTER,self.onCom)

        self.Hide()
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle((0,0),self.Size)
        return

    def onCom(self,e):
        self.histxt.AppendText('EvrSim>>'+e.String+'\n')
        self.histxt.Refresh()
        return
    pass

class AroTreePlc(ScrolledPlc):
    def __init__(self,parent,p,s,cn=''):
        super().__init__(parent,p,s,cn,axis='Y')
        self.item_list=list()
        self.drawed_list=list()
        self.buildTree()
        return

    class TreeItem:
        def __init__(self,depth=0,aro=None):
            self.aro=aro
            self.depth=depth
            self.is_folded=True
            self.is_selected=False
            if hasattr(aro,'parent'):
                self.parent=aro.parent
            if hasattr(aro,'children'):
                self.children=aro.children
                self.is_foldable=True
            else:
                self.is_foldable=False
            return
        pass

    def buildTree(self):
        tree=ESC.ARO_MAP
        self.item_list=list()
        added_nodes=list()
        for item in tree:
            if not hasattr(item,'parent'):continue
            if item.parent is not None:continue
            tstack=[item.AroID]
            while len(tstack)!=0:
                node=tstack[-1]
                aro=ESC.getAro(node)
                if node not in added_nodes:
                    ti=self.TreeItem(aro=aro,depth=len(tstack)-1)
                    self.item_list.append(ti)
                    added_nodes.append(node)
                allow_popout=True
                if hasattr(aro,'children'):
                    for child in aro.children:
                        if child not in added_nodes:
                            allow_popout=False
                            tstack.append(child)
                            break
                if allow_popout:
                    tstack.pop()
                continue
        for item in tree:
            if item.AroID not in added_nodes:
                ti=self.TreeItem(aro=item)
                self.item_list.append(ti)
        self.drawTree()
        return

    def drawTree(self):
        self.DestroyChildren()
        self.drawed_list=list()
        yu=esui.YU
        draw_depth=0
        skip=False
        i=0
        for item in self.item_list:
            if item.depth<=draw_depth:skip=False
            if item.is_folded and item.is_foldable:skip=True
            if skip and item.depth>draw_depth:continue
            TreeItemPlc(self,(1,i*4*yu),(self.Size[0]-2,4*yu),item)
            draw_depth=item.depth
            self.drawed_list.append(item.aro.AroID)
            i+=1
        return
    pass

class TreeItemPlc(Plc):
    def __init__(self,parent,p,s,item):
        super().__init__(parent,p,s)
        self.item=item
        self.on_ctrl=False
        self.select_ctrl=False
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        yu=esui.YU
        dc=wx.PaintDC(self)
        if self.on_ctrl:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        else:
            dc.SetPen(wx.Pen(esui.COLOR_BACK))
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.DrawRectangle((0,0),self.Size)

        if self.item.is_selected:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
            dc.DrawRectangle(yu,yu,2*yu,2*yu)

        tsize=dc.GetTextExtent(self.item.aro.AroName)
        dc.SetTextForeground(esui.COLOR_TEXT)
        yu=esui.YU
        dc.DrawText(self.item.aro.AroName,(self.item.depth+4)*yu,(self.Size[1]-tsize[1])/2)
        return

    def onClk(self,e):
        if e.controlDown:
            pass
        else:
            self.item.is_selected=True
            esui.ARO_PLC.aro_selection=[self.item.aro]
            for ctrl in self.Parent.Children:
                if ctrl!=self:
                    ctrl.item.is_selected=False
                    ctrl.Refresh()
            if self.item.is_foldable:
                self.item.is_folded=not self.item.is_folded
                self.Parent.drawTree()
                return

        esui.ARO_PLC.highlightADP()
        self.Refresh()
        e.Skip()
        return

    def onDClk(self,e):
        esui.SIDE_PLC.showArove(self.item.aro.AroID)
        e.Skip()
        return

    def onEnter(self,e):
        self.on_ctrl=True
        self.Refresh()
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.Refresh()
        return

    pass
