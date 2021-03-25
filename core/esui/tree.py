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
        ''' * Para argkw: node/tid/label/depth/parent/children/icon'''
        super().__init__(parentdiv,style={'s':self.s})
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
        self.dict_icon=dict()
        self.flag_folded=True
        self.flag_selected=False
        self.flag_foldable=self.children is not None

        self.timer_clk=wx.Timer(self)
        dict_icon=dict(esui.ICON)
        dict_icon.update(argkw.get('icon',{}))
        for k,path in dict_icon.items():
            self.dict_icon[k]=esui.UMR.getImg(path=path,w=2*yu,h=2*yu)
        self.Bind(wx.EVT_TIMER,self.onClkTimer,self.timer_clk)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRotWhl)
        self.updateStyle(
            style={'bgc':esui.COLOR_BACK,'text':esui.COLOR_BACK},
            hover={'border':esui.COLOR_FRONT})
        self.Hide()
        return

    def _onPaint(self,e):
        super()._onPaint(e)
        dc=wx.PaintDC(self)

        icon=self.dict_icon['normal']
        if self.flag_selected:
            dc.SetPen(wx.Pen(esui.COLOR_HOVER))
            dc.SetBrush(wx.Brush(esui.COLOR_HOVER))
            dc.DrawRectangle(1,1,self.Size[0]-2,self.Size[1]-2)
            icon=self.dict_icon.get('select',icon)
        if  not self.flag_folded and self.flag_foldable:
            icon=self.dict_icon.get('unfold',icon)
        dc.DrawBitmap(icon,(self.depth*2+1)*yu,yu/2)

        tsize=dc.GetTextExtent(self.label)
        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.DrawText(self.label,(self.depth*2+4)*yu,(self.Size[1]-tsize[1])/2)


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
