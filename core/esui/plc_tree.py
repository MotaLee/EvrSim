import wx
from core import ESC
from core import esui
from core import esgl
yu=esui.YU
xu=esui.XU
class TreeItem:
    def __init__(self,tid=0,label='',parent=None,children=None,depth=0):
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
        self.icon=wx.Image(getattr(item,'_icon','res/img/aro.ico'),type=wx.BITMAP_TYPE_ICO)
        self.icon=self.icon.Scale(2*yu,2*yu).ConvertToBitmap()

        self.Bind(wx.EVT_TIMER,self.onClkTimer,self.clk_timer)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.on_ctrl:dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        else:dc.SetPen(wx.Pen(esui.COLOR_BACK))
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.DrawRectangle((0,0),self.Size)

        if self.item.is_selected:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.SetBrush(wx.Brush(esui.COLOR_FRONT))
            dc.DrawRectangle(0,0,0.5*yu,4*yu)

        tsize=dc.GetTextExtent(self.item.label)
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.DrawText(self.item.label,(self.item.depth*2+4)*yu,(self.Size[1]-tsize[1])/2)
        dc.DrawBitmap(self.icon,(self.item.depth*2+1)*yu,yu)

        # if self.item.depth!=0:
        #     dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        #     dc.DrawLine((self.item.depth+4)*yu,0,(self.item.depth+4)*yu,self.Size[1])
        #     dc.DrawLine((self.item.depth+4)*yu,self.Size[1]/2,(self.item.depth*2+4)*yu,self.Size[1]/2)
        return

    def onClk(self,e):
        e.Skip()
        self.item.is_selected=True
        if not e.controlDown:
            for ctrl in self.Parent.Children:
                if ctrl!=self:
                    ctrl.item.is_selected=False
                ctrl.Refresh()

        if self.clk_timer.IsRunning():self.clk_timer.Stop()
        else:self.clk_timer.StartOnce(300)
        return

    def onClkTimer(self,e):
        if self.item.is_foldable:
            self.item.is_folded=not self.item.is_folded
            self.Parent.drawTree()
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

class TreePlc(esui.ScrolledPlc):
    def __init__(self,parent,p,s,cn=''):
        super().__init__(parent,p,s,cn=cn,axis='Y')
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.item_list=list()
        self.tree_item=TreeItem
        self.plc=TreeItemPlc
        self.buildTree()
        return

    def buildTree(self):
        'Need to be overrided, fill item_list with instances of TreeItem;'
        return

    def drawTree(self):
        if len(self.Children)==0:
            self.plc_dict=dict()
            for item in self.item_list:
                self.plc_dict[item.tid]=self.plc(self,(0,0),(self.Size[0]-yu,4*yu),item)
                self.plc_dict[item.tid].Hide()
        self.Scroll(0,0)
        draw_depth=0
        skip=False
        i=0
        for item in self.item_list:
            if item.depth<=draw_depth:skip=False
            if item.is_folded and item.is_foldable:skip=True
            if skip and item.depth>draw_depth:
                self.plc_dict[item.tid].Hide()
            else:
                self.plc_dict[item.tid].SetPosition((1,i*4*yu+1))
                self.plc_dict[item.tid].Show()
                draw_depth=item.depth
                i+=1
        self.updateVirtualSize()
        self.afterDraw()
        return

    def afterDraw(self):
        return

    def getSelection(self):
        item_selection=list()
        for ti_plc in self.Children:
            if ti_plc.item.is_selected:item_selection.append(ti_plc.item)
        return item_selection
    pass

class SimTreePlc(TreePlc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        return
    def buildTree(self):
        if ESC.SIM_NAME=='':return
        self.item_list=list()
        self.item_list+=[TreeItem(tid=0,label=ESC.SIM_NAME,children=['Setting','Map'])]
        self.item_list+=[TreeItem(tid=len(self.item_list),label='Setting',depth=1)]
        self.item_list+=[TreeItem(tid=len(self.item_list),
            label='Map',depth=1,children=ESC.MAP_LIST)]
        for mapname in ESC.MAP_LIST:
            self.item_list+=[TreeItem(tid=len(self.item_list),label=mapname,depth=2)]
        self.item_list+=[TreeItem(tid=len(self.item_list),label='Model',depth=1,children=list())]
        for mdl in ESC.ACP_MODELS.keys():
            if mdl[0]==ESC.SIM_NAME:
                self.item_list+=[TreeItem(tid=len(self.item_list),label=mdl[1],depth=2)]
        self.item_list+=[TreeItem(tid=len(self.item_list),label='Mod',depth=1,children=list())]
        for modname in ESC.MOD_LIST:
            self.item_list+=[TreeItem(tid=len(self.item_list),label=modname,depth=2)]

        # self.item_list+=[TreeItem(tid=len(self.item_list),label='AroClass',depth=1)]
        # self.item_list+=[TreeItem(tid=len(self.item_list),label='AcpClass',depth=1)]

        self.drawTree()
        return
    pass

# Maps;
class MapItemPlc(TreeItemPlc):
    def __init__(self,parent,p,s,item):
        super().__init__(parent,p,s,item)

        self.Bind(wx.EVT_LEFT_UP,self.onRlsItem)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClkItem)
        self.Bind(wx.EVT_MOTION,self.onMoveItem)
        return

    def onClk(self,e):
        super().onClk(e)
        items=self.Parent.getSelection()
        aro_selection=list()
        for item in items:
            aro_selection.append(ESC.getAro(item.tid))
        esgl.highlight(aro_selection)
        return

    def onDClkItem(self,e):
        item_aro=ESC.getAro(self.item.tid)
        # ddlg=esgl.DetailDialog(esui.WXMW,(25*xu,10*yu),(50*xu,80*yu),item_aro)
        # ddlg.ShowModal()
        esui.SIDE_PLC.showDetail(item_aro)
        e.Skip()
        return

    def onMoveItem(self,e):
        e.Skip()
        if e.leftIsDown:
            self_aro=ESC.getAro(self.item.tid)
            if self_aro not in esgl.ARO_SELECTION:
                self.Parent.SetCursor(self.Parent.cursor_rEnter)
                self.Parent.dragging_item=True
        return

    def onRlsItem(self,e):
        e.Skip()
        self.Parent.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.Parent.dragging_item:
            self.Parent.dragging_item=False
            ESC.sortAro(esgl.ARO_SELECTION,ESC.getAro(self.item.tid))
            self.Parent.build_timer.StartOnce(100)
        return
    pass

class MapTreePlc(TreePlc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        img=wx.Image('res/img/Icon_rEnter.png',type=wx.BITMAP_TYPE_PNG)
        self.cursor_rEnter=wx.Cursor(img)
        self.dragging_item=False
        self.plc=MapItemPlc
        self.build_timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.buildTree,self.build_timer)
        return

    def buildTree(self,e=None):
        ESC.sortAroMap()
        self.DestroyChildren()
        self.item_list=list()
        added_nodes=list()
        for aroid in ESC.ARO_ORDER:
            if aroid in added_nodes:continue
            aro=ESC.getAro(aroid)
            if getattr(aro,'children',None) is None:
                ti=TreeItem(tid=aroid,
                    label=aro.AroName,
                    children=getattr(aro,'children',None))
                self.item_list.append(ti)
                continue
            tstack=[aroid]
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

        self.drawTree()
        return

    pass

# Models;
class MdlTreeItem(TreeItem):
    def __init__(self,tid=0,label='',parent=None,children=None,depth=0,ena=None):
        super().__init__(tid,label,parent,children,depth)
        self.ena=ena
        return
    pass

class MdlItemPlc(TreeItemPlc):
    def __init__(self,parent,p,s,item):
        super().__init__(parent,p,s,item)
        self.ena=item.ena
        self.Unbind(wx.EVT_PAINT)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.icon=wx.Image('res/img/icon_model.png',type=wx.BITMAP_TYPE_PNG)
        self.icon=self.icon.Scale(2*yu,2*yu).ConvertToBitmap()
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
        self.plc=MdlItemPlc
        self.tree_item=MdlTreeItem
        return

    def buildTree(self):
        self.item_list=list()
        mdl_src_list=list()
        self.DestroyChildren()
        for mdl_tuple in ESC.ACP_MODELS.keys():
            if mdl_tuple[0] not in mdl_src_list:
                mdl_src_list.append(mdl_tuple[0])
                src_ti=MdlTreeItem(tid=len(self.item_list),
                    label=mdl_tuple[0],
                    children=list())
                self.item_list.append(src_ti)
            mdl_ti=MdlTreeItem(tid=len(self.item_list),
                label=mdl_tuple[1],
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
