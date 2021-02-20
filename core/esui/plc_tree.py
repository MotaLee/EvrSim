import wx
from core import ESC,esui
yu=esui.YU
xu=esui.XU

class TreeItemDiv(esui.Div):
    s=(0,0)

    @classmethod
    def setClass(cls,**argkw):
        ''' Para argkw: parent/s.'''
        cls.s=argkw.get('s')
        return

    def __init__(self,parentdiv,**argkw):
        super().__init__(parentdiv,style={'s':self.s})
        ''' Para argkw: node/tid/label/depth/parent/children'''
        self.node=argkw.get('node',None)
        if isinstance(self.node,ESC.TreeNode):
            self.nid=self.node.nid
            self.label=self.node.label
            self.depth=self.node.depth
            self.parent=self.node.parent
            self.children=self.node.children
        else:
            self.nid=argkw.get('nid',0)
            self.label=argkw.get('label',0)
            self.depth=argkw.get('depth',0)
            self.parent=argkw.get('parent',None)
            self.children=argkw.get('children',None)
        self.dict_badge=dict()
        self.flag_folded=True
        self.flag_selected=False
        self.flag_foldable=self.children is not None

        self.timer_clk=wx.Timer(self)
        icon_path=argkw.get('icon','res/img/aro.png')
        self.icon=wx.Image(icon_path,type=wx.BITMAP_TYPE_PNG)
        self.icon=self.icon.Scale(2*yu,2*yu).ConvertToBitmap()

        self.Bind(wx.EVT_TIMER,self.onClkTimer,self.timer_clk)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotWhl)
        self.Hide()
        return

    def onPaint(self,e):
        dc=wx.BufferedPaintDC(self)
        if self._flag_hover:dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        else:dc.SetPen(wx.Pen(esui.COLOR_BACK))
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.DrawRectangle((0,0),self.Size)

        if self.flag_selected:
            dc.SetPen(wx.Pen(esui.COLOR_ACTIVE))
            dc.SetBrush(wx.Brush(esui.COLOR_ACTIVE))
            dc.DrawRectangle(1,1,self.Size[0]-2,self.Size[1]-2)

        tsize=dc.GetTextExtent(self.label)
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.DrawText(self.label,(self.depth*2+4)*yu,(self.Size[1]-tsize[1])/2)
        dc.DrawBitmap(self.icon,(self.depth*2+1)*yu,yu/2)

        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        for i in range(self.depth):
            dc.DrawLine((i*2+2)*yu,0,(i*2+2)*yu,self.Size[1])
        return

    def onClk(self,e):
        e.Skip()
        self.flag_selected=True
        if not e.controlDown:
            for ctrl in self.Parent.Children:
                if ctrl!=self:
                    ctrl.flag_selected=False
                ctrl.Refresh()
        else:
            'todo'

        if self.timer_clk.IsRunning():self.timer_clk.Stop()
        else:self.timer_clk.StartOnce(300)
        return

    def onClkTimer(self,e):
        if self.flag_foldable:
            self.flag_folded=not self.flag_folded
            self.Parent.drawTree()
        return

    def onRotWhl(self,e):
        self.Parent.onRotWhl(e)
        return
    pass
class TreeDiv(esui.ScrollDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        'todo: optimize'
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.list_item=list()
        self.dict_nid=dict()
        self.ItemClass=TreeItemDiv
        self.buildTree()
        return

    def addItem(self,**argkw):
        item=self.ItemClass(self,**argkw)
        if item.parent is not None and 'node' not in argkw:
            self.dict_nid[item.parent].children.append(item.nid)
        self.list_item.append(item)
        self.dict_nid[item.nid]=item
        return

    def buildTree(self,tree:ESC.EsTree=None):
        'Need to be overrided, fill item_list with instances of TreeItem;'
        return

    def drawTree(self):
        # self.scroll(0,0)
        draw_depth=0
        skip=False
        i=0
        for item in self.list_item:
            if skip and item.depth>draw_depth:
                item.Hide()
                continue
            else:
                item.SetPosition((1,i*3*yu+1))
                item.Show()
                draw_depth=item.depth
                i+=1
                if item.depth<=draw_depth:skip=False
                if item.flag_folded and item.flag_foldable:skip=True
        self.updateMaxSize()
        self.afterDraw()
        return

    def afterDraw(self):
        return

    def getSelection(self):
        item_selection=list()
        for div in self.getChildren():
            if div.flag_selected:item_selection.append(div.nid)
        return item_selection
    pass
