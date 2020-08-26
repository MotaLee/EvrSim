import wx
from core import ESC
from core import esui
yu=esui.YU
class TreeItem:
    def __init__(self,label='',tid=0,parent=None,children=None,depth=0):

        self.tid=tid
        self.label=label
        self.depth=depth
        self.is_folded=True
        self.is_selected=False
        self.parent=parent
        self.children=children
        if children is not None:
            self.is_foldable=True
        else:
            self.is_foldable=False
        return
    pass

class TreeItemPlc(esui.Plc):
    def __init__(self,parent,p,s,item):
        super().__init__(parent,p,s)
        self.item=item
        self.on_ctrl=False
        self.timer_ran=False
        self.clk_timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onClkTimer,self.clk_timer)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
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

        tsize=dc.GetTextExtent(self.item.label)
        dc.SetTextForeground(esui.COLOR_TEXT)
        yu=esui.YU
        dc.DrawText(self.item.label,(self.item.depth*2+6)*yu,(self.Size[1]-tsize[1])/2)

        if self.item.depth!=0:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawLine((self.item.depth+6)*yu,0,(self.item.depth+6)*yu,self.Size[1])
            dc.DrawLine((self.item.depth+6)*yu,self.Size[1]/2,(self.item.depth*2+6)*yu,self.Size[1]/2)
        return

    def onClk(self,e):
        e.Skip()
        self.item.is_selected=True
        for ctrl in self.Parent.Children:
            if ctrl!=self:
                ctrl.item.is_selected=False
            ctrl.Refresh()
        if self.clk_timer.IsRunning():
            self.clk_timer.Stop()
            return
        else:
            self.clk_timer.StartOnce(200)
        return

    def onClkTimer(self,e):
        if self.item.is_foldable:
            self.item.is_folded=not self.item.is_folded
            self.Parent.drawTree()
        return
    pass

    def onEnter(self,e):
        self.on_ctrl=True
        self.Refresh()
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.Refresh()
        return

    pass

class TreePlc(esui.ScrolledPlc):
    def __init__(self,parent,p,s,cn=''):
        super().__init__(parent,p,s,cn,axis='Y')
        self.item_list=list()
        self.tree_item=TreeItem
        self.plc=TreeItemPlc
        self.buildTree()
        return

    def buildTree(self):
        'Need to be overrided;'
        return

    def drawTree(self):
        self.DestroyChildren()
        self.Scroll(0,0)
        draw_depth=0
        skip=False
        i=0
        for item in self.item_list:
            if item.depth<=draw_depth:skip=False
            if item.is_folded and item.is_foldable:skip=True
            if skip and item.depth>draw_depth:continue
            self.plc(self,(1,i*4*yu+1),(self.Size[0]-yu,4*yu),item)
            draw_depth=item.depth
            i+=1
        self.ry=0
        self.updateVirtualSize()
        self.afterDraw()
        self.Scroll(self.rx,self.ry)
        return

    def afterDraw(self):
        return

    def getSelection(self):
        item_selection=list()
        for ti_plc in self.Children:
            if ti_plc.item.is_selected:item_selection.append(ti_plc.item)
        return item_selection
    pass

class MapTreePlc(TreePlc):
    def buildTree(self):
        aro_map=ESC.ARO_MAP
        self.item_list=list()
        added_nodes=list()
        for aro in aro_map:
            if not hasattr(aro,'parent'):continue
            if aro.parent is not None:continue
            tstack=[aro.AroID]
            while len(tstack)!=0:
                node=tstack[-1]
                aro=ESC.getAro(node)
                if node not in added_nodes:
                    ti=TreeItem(tid=aro.AroID,
                        label=aro.AroName,
                        parent=getattr(aro,'parent',None),
                        children=getattr(aro,'children',None),
                        depth=len(tstack)-1)
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
        for aro in aro_map:
            if aro.AroID not in added_nodes:
                ti=TreeItem(tid=aro.AroID,
                    label=aro.AroName,
                    children=getattr(aro,'children',None))
                self.item_list.append(ti)
        self.drawTree()
        return

    def afterDraw(self):
        for item_plc in self.Children:
            item_plc.Bind(wx.EVT_LEFT_DOWN,self.onClkItem)
            item_plc.Bind(wx.EVT_LEFT_DCLICK,self.onDClkItem)
        return

    def onClkItem(self,e):
        item_aro=ESC.getAro(e.EventObject.item.tid)
        esui.ARO_PLC.aro_selection=[item_aro]
        esui.ARO_PLC.highlightADP()
        e.Skip()
        return

    def onDClkItem(self,e):
        esui.SIDE_PLC.showDetail(e.EventObject.item.tid)
        e.Skip()
        return
    pass

class MdlTreeItem(TreeItem):
    def __init__(self,label='',parent=None,children=None,depth=0,ena=None):
        super().__init__(label,0,parent,children,depth)
        self.ena=ena
        return
    pass

class MdlTreeItemPlc(TreeItemPlc):
    def __init__(self,parent,p,s,item):
        super().__init__(parent,p,s,item)
        self.ena=item.ena
        self.Unbind(wx.EVT_PAINT)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return
    def onPaint(self,e):
        super().onPaint(e)
        yu=esui.YU
        dc=wx.PaintDC(self)
        if self.ena is None:
            'todo:full mod enability'
            return

        if self.ena:
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
        else:
            dc.SetBrush(wx.Brush(esui.COLOR_BLACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle(self.Size[0]-3*yu,yu,2*yu,2*yu)

        return
    pass

class ModelTreePlc(TreePlc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.plc=MdlTreeItemPlc
        self.tree_item=MdlTreeItem
        return

    def buildTree(self):
        self.item_list=list()
        mdl_src_list=list()
        for mdl_tuple in ESC.ACP_MODELS.keys():
            if mdl_tuple[0] not in mdl_src_list:
                mdl_src_list.append(mdl_tuple[0])
                src_ti=MdlTreeItem(label=mdl_tuple[0],children=list())
                self.item_list.append(src_ti)
            mdl_ti=MdlTreeItem(label=mdl_tuple[1],
                parent=mdl_tuple[0],
                depth=1,
                ena=mdl_tuple not in ESC.MODEL_DISABLE)
            for i in range(0,len(self.item_list)):
                if self.item_list[i].label==mdl_tuple[0]:
                    self.item_list[i].children.append(mdl_tuple[1])
                    self.item_list.insert(i+1,mdl_ti)
                    break
        self.drawTree()
        return

    def afterDraw(self):
        for item_plc in self.Children:
            if item_plc.item.parent is not None:
                item_plc.Bind(wx.EVT_LEFT_DCLICK,self.onDClkItem)
        return

    def onDClkItem(self,e):
        item=e.EventObject.item
        esui.SIDE_PLC.onClkWorkspace(call='ACP_PLC')
        esui.ACP_PLC.drawAcp(mdl_tuple=(item.parent,item.label))
        e.Skip()
        return
    pass
