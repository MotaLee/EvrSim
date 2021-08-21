# -*- coding: UTF-8 -*-
import wx
from core import ESC,esui,esgl,esc
GLC=esgl.GLC
yu=esui.YU
UMR=esui.UMR

class SideDiv(esui.TabDiv):
    def __init__(self, parent, **argkw):
        super().__init__(parent,**argkw)
        self.div_mgr=self.addTab('Manager',MgrDiv)
        self.div_detail=self.addTab('Detail',DetailDiv)
        self.hideTab('Detail')
        self.toggleTab()

        self.buildMapTree=self.div_mgr.tree_map.buildTree
        self.showDetail=self.div_detail.showDetail
        self.clearDetail=self.div_detail.clearDetail
        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.Hide()
        return

    def onComEvt(self,e:esui.ESEvent):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_UPDATE_MAP:
            self.buildMapTree()
            self.div_mgr.tree_sim.updateTree()
        elif etype==esui.ETYPE_RESET_SIM:
            self.buildMapTree()
        elif etype==esui.ETYPE_OPEN_SIM:
            self.div_mgr.tree_sim.buildTree()
            self.div_mgr.tree_map.buildTree()
            self.div_mgr.tree_mdl.buildTree()
            self.Show()
        return

    pass

class MgrDiv(esui.ScrollDiv):
    def __init__(self, parent:SideDiv, **argkw):
        super().__init__(parent, **argkw)
        self.txt_search=esui.InputText(self,style={'p':(yu,yu),'s':(self.Size[0]-10*yu,3*yu)})
        self.btn_search=esui.Btn(self,(self.Size[0]-8*yu,yu),(3*yu,3*yu),'Sr')
        self.btn_clear=esui.Btn(self,(self.Size[0]-4*yu,yu),(3*yu,3*yu),'X')

        self.txt_sim=esui.StaticText(self,(yu,5*yu),(8*yu,3*yu),'Sim:',align='left')
        self.menu_tree=esui.MenuBtnDiv(self,label='Sim',select=True,
            style={'p':(self.Size[0]-9*yu,5*yu),'s':(8*yu,3*yu)},
            items=['Sim','Map','Model','Mod'])

        stl_toolset={'p':(yu,9*yu),'s':(self.Size[0]-2*yu,3*yu)}
        stl_tree={'p':(yu,13*yu),'s':(self.Size[0]-2*yu,40*yu)}

        self.toolset_sim=esui.Div(self,style=stl_toolset)
        self.toolset_map=esui.Div(self,style=stl_toolset)
        self.btn_add_space=esui.Btn(self.toolset_map,
            (self.toolset_map.Size[0]-11*yu,0),(3*yu,3*yu),'Spc')
        self.btn_add_group=esui.Btn(self.toolset_map,
            (self.toolset_map.Size[0]-7*yu,0),(3*yu,3*yu),'Grp')
        self.btn_filter=esui.MenuBtnDiv(self.toolset_map,
            style={'p':(self.toolset_map.Size[0]-3*yu,0),'s':(3*yu,3*yu)},
            label='Flr',items=['None','Space','Group'])
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
        self.menu_tree.bindPopup(esui.EBIND_LEFT_CLK,self.onClkMenu)
        self.btn_en_mdl.Bind(esui.EBIND_LEFT_CLK,self.onClkEnable)
        return

    def onClkMenu(self,e:esui.ESEvent):
        label=e.EventObject.label
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
            self.txt_sim.setLabel('Map:')
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
            div:MdlItemDiv
            if div.flag_selected and div.depth!=0:
                flag_enabled=div.mdl in ESC.MODEL_ENABLE
                if flag_enabled:enable_list.remove(div.mdl)
                else:enable_list.append(div.mdl)
                break
        ESC.setSim({'MODEL_ENABLE':enable_list})
        div.checkModelStatus()
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
        self.Bind(esui.EBIND_LEFT_DCLK,self.onDClk)
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

    def onDClk(self,e:esui.ESEvent):
        if self.plabel=='Map':
            if self.label!=ESC.MAP_ACTIVE:
                ESC.loadMapFile(self.label)
                ESC.setSim({'MAP_ACTIVE':self.label})
                esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
            else:esui.toggleWorkspace(target='ARO')
        elif self.plabel=='Model':
            UMR.MDL_DIV.drawMdl((ESC.SIM_NAME,self.label))
            esui.toggleWorkspace(target='ACP')
        e.Skip()
        return
    pass
class SimTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.ItemClass=SimItemDiv
        self.ItemClass.setClass(s=(self.Size[0]-yu,3*yu))
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
        self.Bind(esui.EBIND_LEFT_DCLK,self.onDClk)
        self.Bind(wx.EVT_MOTION,self.onMove)
        return

    def onClk(self,e):
        super().onClk(e)
        items=self.Parent.getSelection()
        aro_selection=[ESC.getAro(aroid) for aroid in items]
        GLC.highlightAdp(aro_selection)
        return

    def onDClk(self,e):
        aro=ESC.getAro(self.nid)
        UMR.SIDE_DIV.showDetail(aro)
        e.Skip()
        return

    def onMove(self,e):
        e.Skip()
        if e.leftIsDown:
            self_aro=ESC.getAro(self.nid)
            if self_aro not in GLC.getSelection():
                self.Parent.SetCursor(self.Parent.csr_rEnter)
                self.Parent._flag_dragging=True
        return

    def onRls(self,e):
        e.Skip()
        self.Parent.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if self.Parent._flag_dragging:
            self.Parent._flag_dragging=False
            if self.nid!=-1:
                ESC.sortAro(GLC.getSelection(),ESC.getAro(self.nid))
            self.Parent.timer_sort.StartOnce(100)
        return
    pass
class MapTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.csr_rEnter=UMR.getCursor(path='res/img/Icon_rEnter.png')
        self._flag_dragging=False
        self.ItemClass=MapItemDiv
        self.ItemClass.setClass(s=(self.Size[0]-yu,3*yu))
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
        for aroid in ESC.getMapOrder():
            if aroid in self.dict_nid:continue
            aro=ESC.getAro(aroid)
            if aro.children==[]:
                self.addItem(nid=aro.AroID,label=aro.AroName,
                    icon=getattr(aro,'icon',dict()),
                    parent=-1,children=None,depth=1)
                continue
            tstack=[aroid]
            while len(tstack)!=0:
                node=tstack[-1]
                aro=ESC.getAro(node)
                if node not in self.dict_nid:
                    self.addItem(nid=aro.AroID,label=aro.AroName,
                        parent=aro.parent,
                        children=list(aro.children),
                        icon=getattr(aro,'icon',dict()),
                        depth=len(tstack))
                allow_popout=True
                if len(aro.children)!=0:
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
        for aroid in ESC.getMapOrder():
            list_new.append(self.dict_nid[aroid])
        self.list_item=list_new
        self.drawTree()
        return
    pass

class MdlItemDiv(esui.TreeItemDiv):
    def __init__(self,parentdiv,**argkw):
        super().__init__(parentdiv,**argkw)
        self.mdl:tuple=argkw.get('mdl',())

        self.badge_sim=esui.Div(self,
            style={
                'p':(self.Parent.Size.x-4*yu,0.5*yu),
                's':(3*yu,3*yu),
                'border':esui.COLOR_FRONT},
            active={'bgc':esui.COLOR_FRONT})

        self.checkModelStatus()
        self.Bind(esui.EBIND_LEFT_DCLK,self.onDClk)
        return

    def onDClk(self,e):
        if self.mdl==():return
        esui.toggleWorkspace(target='ACP')
        UMR.MDL_DIV.drawMdl(self.mdl)
        e.Skip()
        return

    def checkModelStatus(self):
        if self.mdl in ESC.MODEL_ENABLE:
            self.badge_sim.setActive(True)
        else:
            self.badge_sim.setActive(False)
        return
    pass
class MdlTreeDiv(esui.TreeDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.ItemClass=MdlItemDiv
        self.ItemClass.setClass(s=(self.Size[0]-yu,3*yu))
        self.stl_en={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(yu,1.5*yu),
            'bgc':esui.COLOR_FRONT}
        self.stl_dis={
            'p':(self.Size[0]-3*yu,0.75*yu),
            's':(yu,1.5*yu),
            'border':esui.COLOR_FRONT}
        self.Hide()
        return

    def buildTree(self):
        if not ESC.isSimOpened():return
        self.list_item=list()
        self.dict_nid=dict()
        self.delChildren()
        self.addItem(nid=0,label=ESC.SIM_NAME,children=list())
        for model in ESC.SIM_TREE.node_model.data:
            self.addItem(
                nid=len(self.list_item),depth=1,
                label=model,parent=0,mdl=(ESC.SIM_NAME,model))
        for mod in ESC.SIM_TREE.node_mod.data:
            pnid=len(self.list_item)
            self.addItem(nid=pnid,label=mod,children=list())
            for model in ESC.MOD_TREE_DICT[mod].node_mdl.data:
                self.addItem(nid=len(self.list_item),depth=1,
                label=model,parent=pnid,mdl=(mod,model))
        self.drawTree()
        return
    pass

class DetailDiv(esui.Div):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.aro=None
        self.list_history=[]
        self.list_base=['AroID','AroName','visible',
            'enable','parent','children','AbbrClass',
            'AroClass','adp','desc']
        self.dict_ext=dict()
        esui.StaticText(self,(yu,yu),(8*yu,4*yu),'Detail:',align='left')
        # self.btn_for=esui.DivBtn(self,label='>>',enable=False,
        #     style={'p':(self.Size.x-20*yu,yu),'s':(4*yu,4*yu)})
        # self.btn_back=esui.DivBtn(self,label='<<',enable=False,
        #     style={'p':(self.Size.x-15*yu,yu),'s':(4*yu,4*yu)})
        self.btn_con=esui.DivBtn(self,label='√',
            style={'p':(self.Size.x-12*yu,yu),'s':(3*yu,4*yu)})
        self.btn_pcon=esui.DivBtn(self,label='P',
            style={'p':(self.Size.x-9*yu,yu),'s':(3*yu,4*yu)})
        self.btn_can=esui.DivBtn(self,label='×',
            style={'p':(self.Size.x-5*yu,yu),'s':(4*yu,4*yu)})

        self.div_arove=esui.ScrollDiv(self,style={
            'p':(0,6*yu),
            's':(self.Size.x,self.Size.y-6*yu),
            'bgc':esui.COLOR_LBACK})
        self.txt_aroid=esui.DivText(self.div_arove,label='AroID',
            style={'p':(yu,0),'s':(6*yu,3*yu)})
        self.btn_aroid=esui.DivBtn(self.div_arove,
            style={'p':(yu,4*yu),'s':(6*yu,4*yu)})
        self.txt_aroname=esui.DivText(self.div_arove,label='AroName',
            style={'p':(8*yu,0),'s':(6*yu,3*yu)})
        self.input_aroname=esui.InputText(self.div_arove,cn='AroName',
            style={'p':(8*yu,4*yu),'s':(self.Size.x-9*yu,4*yu)})
        self.btn_enable=esui.TglBtn(self.div_arove,label='Enable',
            style={'p':(yu,9*yu),'s':(self.Size.x/2-1.5*yu,3*yu)})
        self.btn_visible=esui.TglBtn(self.div_arove,label='Visible',
            style={'p':(self.Size.x/2+yu/2,9*yu),'s':(self.Size.x/2-1.5*yu,3*yu)})
        self.txt_abbrclass=esui.DivText(self.div_arove,label='AbbrClass',
            style={'p':(yu,13*yu),'s':(6*yu,3*yu),'align':'left'})
        self.input_abbrclass=esui.InputText(self.div_arove,readonly=True,
            style={'p':(8*yu,13*yu),'s':(self.Size.x-9*yu,3*yu)})
        self.txt_adp=esui.DivText(self.div_arove,label='ADP',
            style={'p':(yu,17*yu),'s':(6*yu,3*yu),'align':'left'})
        self.input_adp=esui.InputText(self.div_arove,readonly=True,
            style={'p':(8*yu,17*yu),'s':(self.Size.x-9*yu,3*yu)})
        self.txt_parent=esui.DivText(self.div_arove,label='Parent',
            style={'p':(yu,21*yu),'s':(6*yu,3*yu),'align':'left'})
        self.btn_parent=esui.DivBtn(self.div_arove,
            style={'p':(8*yu,21*yu),'s':(self.Size.x-9*yu,3*yu)})
        self.txt_children=esui.DivText(self.div_arove,label='Children',
            style={'p':(yu,25*yu),'s':(6*yu,3*yu),'align':'left'})
        self.btn_children=esui.MenuBtnDiv(self.div_arove,
            style={'p':(8*yu,25*yu),'s':(self.Size.x-9*yu,3*yu)})
        self.txt_desc=esui.DivText(self.div_arove,label='Desc',
            style={'p':(yu,29*yu),'s':(6*yu,3*yu),'align':'left'})
        self.input_desc=esui.MultilineText(self.div_arove,cn='desc',
            style={'p':(yu,33*yu),'s':(self.Size.x-2*yu,9*yu)})

        self.btn_con.Bind(esui.EBIND_LEFT_CLK,self.onClkConfirm)
        self.btn_can.Bind(esui.EBIND_LEFT_CLK,self.onClkCancel)
        return

    def onClkConfirm(self,e):
        arove=dict()
        for ctrl in self.div_arove.getChildren():
            if ctrl.cn=='':continue
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                if ctrl.isReadonly():continue
                v=ctrl.getValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif isinstance(ctrl,esui.TglBtn):
                v_eval=ctrl.isActive()
            else:continue
            if v_eval!=getattr(self.aro,ctrl.cn):
                arove[ctrl.cn]=v_eval
        ESC.setAro(self.aro.AroID,**arove)
        # esui.sendComEvt(esui.ETYPE_RUN_PRESET)
        esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        esui.HintText(self,label='Updated.',
            style={'p':(self.Size[0]-20*yu,yu),'s':(8*yu,4*yu)})
        return

    def onClkCancel(self,e):
        UMR.SIDE_DIV.hideTab('Detail')
        UMR.SIDE_DIV.toggleTab('Manager')
        return

    def showDetail(self,aro=None):
        UMR.SIDE_DIV.toggleTab('Detail')
        if aro is None:aro:esc.Aro=GLC.getSelection()[0]
        self.aro=ESC.getAro(aro)
        self.clearDetail()

        self.btn_aroid.setLabel(aro.AroID)
        self.input_aroname.setValue(aro.AroName)
        self.btn_visible.setActive(aro.visible)
        self.btn_enable.setActive(aro.enable)
        self.input_abbrclass.setValue(aro.AbbrClass)
        self.input_adp.setValue(aro.adp)
        self.input_desc.setValue(aro.desc)
        if aro.parent==-1:
            self.btn_parent.setLabel('(None)')
        else:
            p=ESC.getLinkAro(aro,'parent')
            self.btn_parent.setLabel(str(p.AroID)+' : '+p.AroName)
        if len(aro.children)==0:
            self.btn_children.setLabel('(Empty)')
        else:
            children=ESC.getLinkAro(aro,'children')
            self.btn_children.setItems([
                str(aro.AroID)+' : '+aro.AroName
                for aro in children])
            self.btn_children.setLabel(str(len(children))+' items')

        ys=43*yu
        i=0
        for k,v in vars(aro).items():
            if k in self.list_base or k in aro._flag['hide']:continue
            key=esui.DivText(self.div_arove,label=k,
                style={'p':(yu,ys+i*4*yu),'s':(6*yu,3*yu),'align':'left'})

            if k in aro._flag['long']:
                value=esui.MultilineText(self.div_arove,
                    hint=str(v),cn=k,
                    readonly=k in aro._flag['lock'],
                    style={'p':(yu,ys+(i+1)*4*yu),'s':(self.Size.x-2*yu,12*yu)})
                i+=3
            elif k in aro._flag['link']:
                if isinstance(v,list):
                    value=esui.MenuBtnDiv(self.div_arove,
                        style={'p':(8*yu,i*4*yu),'s':(self.Size.x-9*yu,3*yu)})
                    links=ESC.getLinkAro(aro,k)
                    value.setItems([
                        str(aro.AroID)+' : '+aro.AroName
                        for aro in links])
                    value.setLabel(str(len(links))+' items')
                else:
                    link=ESC.getLinkAro(aro,k)
                    if link is None:string='(Empty)'
                    else:string=str(link.AroID)+' : '+link.AroName
                    value=esui.DivBtn(self.div_arove,label=string,
                        style={'p':(8*yu,4*i*yu),'s':(self.Size.x-9*yu,3*yu)})
            elif isinstance(v,bool):
                value=esui.TglBtn(self.div_arove,select=v,cn=k,
                    style={'p':(8*yu,ys+(i*4+0.5)*yu),'s':(3*yu,3*yu)})
            else:
                value=esui.InputText(self.div_arove,
                    hint=str(v),cn=k,
                    readonly=k in aro._flag['lock'],
                    style={'p':(8*yu,ys+i*4*yu),'s':(self.Size.x-9*yu,3.5*yu)})
            i+=1
            self.dict_ext[k]=(key,value)
        self.div_arove.updateMaxSize()
        return

    def clearDetail(self):
        for tpl in self.dict_ext.values():
            tpl[0].Destroy()
            tpl[1].Destroy()
        self.dict_ext.clear()
        return

    def onClkLink(self,e):
        'todo: click link'
        label=e.EventObject.label

        aroid=label[0:label.find('.')]
        self.showDetail(aroid)
        return
    pass
