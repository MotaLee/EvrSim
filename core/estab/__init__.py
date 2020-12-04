# -*- coding: UTF-8 -*-
import wx
from core import ESC,esui,esevt
from .manager import ManagerTab
from .detail import DetailTab
yu=esui.YU

class SidePlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.Hide()

        self.map_list=list()
        self.model_list=list()
        self.tab_list=['Manager']

        tab_pos=(2,8*yu)
        tab_size=(s[0],88*yu)
        self.workspace_btn=esui.Btn(self,(1,0),(4*yu,4*yu),'<->',tip='Toggle Aro/Acp')
        self.manager_btn=esui.TabBtn(self,(1,4*yu),(8*yu,4*yu),'Manager')
        self.manager_tab=ManagerTab(self,tab_pos,tab_size,'Manager')

        self.detail_btn=esui.TabBtn(self,(8*yu,4*yu),(8*yu,4*yu),'Detail')
        self.detail_tab=DetailTab(self,tab_pos,tab_size,'Detail')

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)

        self.workspace_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkWorkspace)

        self.updateAroTree=self.manager_tab.map_block.map_tree.buildTree
        self.showDetail=self.detail_tab.showDetail
        self.clearDetail=self.detail_tab.clearDetail
        self.Hide()
        return

    def loadMaps(self,maps=None):
        '''Load maps;'''
        if maps is None:
            maps=list(ESC.MAP_LIST)
        self.map_list=maps
        self.manager_tab.map_block.map_menu.setItems(maps)
        self.manager_tab.map_block.onClkMapMenu(None)
        self.toggleTab('Manager')
        return

    def loadModels(self,models=None):
        if models is None:
            models=list(ESC.ACP_MODELS.keys())
        for model in models:
            if model not in self.model_list:
                self.model_list.append(model)
        self.manager_tab.model_block.model_tree.buildTree()
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_UPDATE_MAP:
            self.updateAroTree()
        elif etype==esevt.ETYPE_RESET_SIM:
            self.updateAroTree()
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.loadMaps()
            self.loadModels()
            self.manager_tab.sim_block.sim_tree.buildTree()
            self.Show()
        return

    def onClkWorkspace(self,e=None,call=None):
        status=esui.ARO_PLC.IsShown()
        if status or call=='ACP_PLC':
            esui.ARO_PLC.Hide()
            esui.ACP_PLC.Show()
            esui.ACP_PLC.drawConnection()
        elif not status or call=='ARO_PLC':
            esui.ARO_PLC.Show()
            esui.ACP_PLC.Hide()
        if e is not None and call is None:e.Skip()
        return

    def toggleTab(self,tablabel='Manager'):
        for ctrl in self.Children:
            if type(ctrl)==esui.TabBtn and tablabel==ctrl.Label:
                ctrl.onClk(None)
        return

    def getTab(self,tablabel):
        for ctrl in self.Children:
            if ctrl.GetLabel()==tablabel and isinstance(ctrl,esui.Plc):
                return ctrl
        i=len(self.tab_list)
        yu=esui.YU
        btn=esui.TabBtn(self,(8*yu*i,4*yu),(8*yu,4*yu),tablabel)
        tab=esui.ScrolledPlc(self,(0,8*yu),(self.Size.x,self.Size.y-8*yu),cn=tablabel)
        self.tab_list.append(tablabel)
        btn.onClk(None)
        return tab

    def delTab(self,tablabel):
        for ctrl in self.Children:
            if ctrl.GetLabel()==tablabel:
                ctrl.DestroyLater()
        self.toggleTab()
        return

    pass
