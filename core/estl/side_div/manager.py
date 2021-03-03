import wx
from core import ESC,esui,esgl,esevt
yu=esui.YU

class MgrDiv(esui.ScrollDiv):
    def __init__(self, parent: wx.Window, **argkw):
        super().__init__(parent, **argkw)
        self.txt_search=esui.InputText(self,(yu,yu),(self.Size[0]-10*yu,3*yu))
        self.btn_search=esui.Btn(self,(self.Size[0]-8*yu,yu),(3*yu,3*yu),'Sr')
        self.btn_clear=esui.Btn(self,(self.Size[0]-4*yu,yu),(3*yu,3*yu),'X')

        self.txt_sim=esui.StaticText(self,(yu,5*yu),(8*yu,3*yu),'Sim:',align='left')
        self.menu_tree=esui.SelectMenuBtn(self,
            (self.Size[0]-9*yu,5*yu),(8*yu,3*yu),'Sim',
            ['Sim','Map','Model','Mod'])

        stl_toolset={'p':(yu,9*yu),'s':(self.Size[0]-2*yu,3*yu)}
        stl_tree={'p':(yu,13*yu),'s':(self.Size[0]-2*yu,40*yu)}

        self.toolset_sim=esui.Div(self,style=stl_toolset)
        self.toolset_map=esui.Div(self,style=stl_toolset)
        self.btn_add_space=esui.Btn(self.toolset_map,
            (self.toolset_map.Size[0]-11*yu,0),(3*yu,3*yu),'Spc')
        self.btn_add_group=esui.Btn(self.toolset_map,
            (self.toolset_map.Size[0]-7*yu,0),(3*yu,3*yu),'Grp')
        self.btn_filter=esui.MenuBtn(self.toolset_map,
            (self.toolset_map.Size[0]-3*yu,0),(3*yu,3*yu),
            'Flr',['None','Space','Group'])
        self.toolset_mdl=esui.Div(self,style=stl_toolset)
        self.btn_en_mdl=esui.Btn(self.toolset_mdl,
            (self.toolset_mdl.Size[0]-7*yu,0),(3*yu,3*yu),'En')
        self.btn_del_mdl=esui.Btn(self.toolset_mdl,
            (self.toolset_mdl.Size[0]-3*yu,0),(3*yu,3*yu),'Del')
        self.toolset_map.Hide()
        self.toolset_mdl.Hide()

        self.tree_sim=SimTreeDiv(self,style=stl_tree)
        self.tree_map=MapTreeDiv(self,style=stl_tree)
        self.tree_mdl=MdlTreeDiv(self,style=stl_tree)
        self.updateMaxSize()
        self.menu_tree.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMenu)
        self.btn_en_mdl.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
        return

    def onClkMenu(self,e:wx.Event):
        label=self.menu_tree.getCurrent()
        self.toggleTree(label)
        e.Skip()
        return

    def toggleTree(self,label):
        if label=='Sim':
            self.tree_sim.Show()
            self.tree_map.Hide()
            self.tree_mdl.Hide()
            self.toolset_sim.Show()
            self.toolset_map.Hide()
            self.toolset_mdl.Hide()
            self.txt_sim.setLabel('Sim:')
        elif label=='Map':
            self.tree_sim.Hide()
            self.tree_map.Show()
            self.tree_mdl.Hide()
            self.toolset_sim.Hide()
            self.toolset_map.Show()
            self.toolset_mdl.Hide()
            self.txt_sim.setLabel('Sim:')
        elif label=='Model':
            self.tree_sim.Hide()
            self.tree_map.Hide()
            self.tree_mdl.Show()
            self.toolset_sim.Hide()
            self.toolset_map.Hide()
            self.toolset_mdl.Show()
            self.txt_sim.setLabel('Model:')
        elif label=='Mod':pass
        return

    def onClkEnable(self,e):
        enable_list=list(ESC.MODEL_ENABLE)
        for div in self.tree_mdl.getChildren():
            if div.flag_selected and div.depth!=0:
                mdl=self.tree_mdl.getModelTuple(div)
                flag_enabled=mdl in ESC.MODEL_ENABLE
                if flag_enabled:enable_list.remove(mdl)
                else:enable_list.append(mdl)
        ESC.setSim({'MODEL_ENABLE':enable_list})
        self.tree_mdl.drawBadges()
        e.Skip()
        return

    def onClkMapMenu(self,e):

        return
    pass

class SimItemDiv(esui.TreeItemDiv):
    def __init__(self, parentdiv, **argkw):
        super().__init__(parentdiv, **argkw)
        self.stl_en={
            'p':(self.Size[0]-4*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'bgc':esui.COLOR_FRONT}
        self.stl_dis={
            'p':(self.Size[0]-4*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'border':esui.COLOR_FRONT}
        self.plabel=''
        self.updateItem()
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        return

    def updateItem(self):
        self.DestroyChildren()
        if self.parent is None:self.plabel=''
        else:self.plabel=self.Parent.dict_nid[self.parent].label

        if self.plabel=='Map' and self.label==ESC.MAP_ACTIVE:
            self.dict_badge['active map']=esui.Div(self,style=self.stl_en)
        if self.plabel=='Model':
            if (ESC.SIM_NAME,self.label) in ESC.MODEL_ENABLE:
                self.dict_badge['enable mdl']=esui.Div(self,style=dict(self.stl_en))
            else:
                self.dict_badge['enable mdl']=esui.Div(self,style=dict(self.stl_dis))
        return

    def onDClk(self,e:wx.Event):
        if self.plabel=='Map':
            if self.label!=ESC.MAP_ACTIVE:
                ESC.loadMapFile(self.label)
                esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
            else:esui.toggleWorkspace(target='ARO')
        elif self.plabel=='Model':
            esui.IDX.MDL_DIV.drawMdl((ESC.SIM_NAME,self.label))
            esui.toggleWorkspace(target='ACP')
        e.Skip()
        return
    pass
class SimTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.ItemClass=SimItemDiv
        # self.ItemClass.setClass(s=(self.Size[0]-yu,3*yu))
        self.stl_en={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'bgc':esui.COLOR_FRONT}
        self.stl_dis={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'border':esui.COLOR_FRONT}
        return

    def drawBadges(self):
        for ctrl in self.getChildren():
            if ctrl.parent is None:continue
            else:pctrl=self.dict_nid[ctrl.parent]
            if pctrl.label=='Map' and ctrl.label==ESC.MAP_ACTIVE:
                ctrl.dict_badge['active map']=esui.Div(ctrl,style=self.stl_en)
            if pctrl.label=='Model':
                if (ESC.SIM_NAME,ctrl.label) in ESC.MODEL_ENABLE:
                    ctrl.dict_badge['enable mdl']=esui.Div(ctrl,style=dict(self.stl_en))
                else:
                    ctrl.dict_badge['enable mdl']=esui.Div(ctrl,style=dict(self.stl_dis))
        return

    def buildTree(self):
        if not ESC.isSimOpened():return
        self.list_item=list()
        self.dict_nid=dict()
        self.delChildren()
        tree=ESC.SIM_TREE
        track=tree.travsalTree(reverse=True)
        for nid in track:
            node=tree.getNode(nid)
            self.addItem(node=node)
        self.drawTree()
        # self.drawBadges()
        return

    def updateTree(self):
        tree=ESC.SIM_TREE
        track=tree.travsalTree(reverse=True)
        list_new=list()
        for i in range(len(track)):
            if track[i] in self.dict_nid:
                self.dict_nid[track[i]].updateItem()
                list_new.append(self.dict_nid[track[i]])
            else:
                node=tree.getNode(track[i])
                self.addItem(node=node)
        for k in self.dict_nid.keys():
            if k not in track:del self.dict_nid[k]
        self.list_item=list_new
        self.drawTree()
        return
    pass

# Maps;
class MapItemDiv(esui.TreeItemDiv):
    def __init__(self,parentdiv,**argkw):
        super().__init__(parentdiv,**argkw)
        self.Bind(wx.EVT_LEFT_UP,self.onRls)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        self.Bind(wx.EVT_MOTION,self.onMove)
        return

    def onClk(self,e):
        super().onClk(e)
        items=self.Parent.getSelection()
        aro_selection=[ESC.getAro(aroid) for aroid in items]
        esgl.highlight(aro_selection)
        return

    def onDClk(self,e):
        aro=ESC.getAro(self.nid)
        esui.IDX.SIDE_DIV.showDetail(aro)
        e.Skip()
        return

    def onMove(self,e):
        e.Skip()
        if e.leftIsDown:
            self_aro=ESC.getAro(self.nid)
            if self_aro not in esgl.ARO_SELECTION:
                self.Parent.SetCursor(self.Parent.csr_rEnter)
                self.Parent._flag_dragging=True
        return

    def onRls(self,e):
        e.Skip()
        self.Parent.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.Parent._flag_dragging:
            self.Parent._flag_dragging=False
            if self.nid!=-1:
                ESC.sortAro(esgl.ARO_SELECTION,ESC.getAro(self.nid))
            self.Parent.timer_sort.StartOnce(100)
        return
    pass
class MapTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        img=wx.Image('res/img/Icon_rEnter.png',type=wx.BITMAP_TYPE_PNG)
        self.csr_rEnter=wx.Cursor(img)
        self._flag_dragging=False
        self.ItemClass=MapItemDiv
        self.timer_sort=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.sortTree,self.timer_sort)
        self.Hide()
        return

    def buildTree(self,e=None):
        if not ESC.isSimOpened():return
        ESC.sortMap()
        self.list_item=list()
        self.dict_nid=dict()
        self.delChildren()
        self.addItem(nid=-1,label=ESC.MAP_ACTIVE,children=list())
        for aroid in ESC.ARO_ORDER:
            if aroid in self.dict_nid:continue
            aro=ESC.getAro(aroid)
            children= getattr(aro,'children',None)
            if children is None:
                self.addItem(nid=aro.AroID,label=aro.AroName,
                    parent=-1,children=children,depth=1)
                continue
            tstack=[aroid]
            while len(tstack)!=0:
                node=tstack[-1]
                aro=ESC.getAro(node)
                if node not in self.dict_nid:
                    self.addItem(nid=aro.AroID,label=aro.AroName,
                        parent=getattr(aro,'parent',None),
                        children=getattr(aro,'children',None),
                        depth=len(tstack))
                allow_popout=True
                if hasattr(aro,'children'):
                    for child in aro.children:
                        if child not in self.dict_nid:
                            allow_popout=False
                            tstack.append(child)
                            break
                if allow_popout:tstack.pop()
                continue

        self.drawTree()
        return


    def sortTree(self,e=None):
        list_new=[self.dict_nid[-1]]
        for aroid in ESC.ARO_ORDER:
            list_new.append(self.dict_nid[aroid])
        self.list_item=list_new
        self.drawTree()
        return
    pass

class MdlTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.ItemClass.setClass(parent=self,s=(self.Size[0]-yu,3*yu))
        self.stl_en={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'bgc':esui.COLOR_FRONT}
        self.stl_dis={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(1.5*yu,1.5*yu),
            'border':esui.COLOR_FRONT}
        self.Hide()
        return

    def buildTree(self):
        if not ESC.isSimOpened():return
        self.list_item=list()
        self.dict_nid=dict()
        self.delChildren()
        self.addItem(nid=0,label=ESC.SIM_NAME,children=list())
        for mdl in ESC.SIM_TREE.node_model.data:
            self.addItem(
                nid=len(self.list_item),depth=1,
                label=mdl,parent=0)
        for mod in ESC.SIM_TREE.node_mod.data:
            pnid=len(self.list_item)
            self.addItem(nid=pnid,label=mod,children=list())
            for mdl in ESC.MOD_TREE_DICT[mod].node_mdl.data:
                self.addItem(nid=len(self.list_item),depth=1,
                label=mdl,parent=pnid)
        self.drawTree()
        self.drawBadges()
        return

    def afterDraw(self):
        for item in self.getChildren():
            if item.parent is not None:
                item.Bind(wx.EVT_LEFT_DCLICK,self.onDClkItem)
        return

    def onDClkItem(self,e):
        mdl=self.getModelTuple(e.EventObject)
        esui.toggleWorkspace(target='ACP')
        esui.IDX.MDL_DIV.drawMdl(mdl)
        e.Skip()
        return

    def getModelTuple(self,div):
        pitem=self.dict_nid[div.parent]
        return (pitem.label,div.label)

    def drawBadges(self):
        for ctrl in self.getChildren():
            ctrl.DestroyChildren()
            if ctrl.depth==0:mod=ctrl.label
            if ctrl.depth==1:
                if (mod,ctrl.label) in ESC.MODEL_ENABLE:
                    ctrl.dict_badge['enable mdl']=esui.Div(ctrl,style=dict(self.stl_en))
                else:
                    ctrl.dict_badge['enable mdl']=esui.Div(ctrl,style=dict(self.stl_dis))
        return
    pass
