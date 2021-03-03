# -*- coding: UTF-8 -*-
import wx
from core import esui,esevt
from .manager import MgrDiv
from .detail import DetailDiv
yu=esui.YU

class SideDiv(esui.TabDiv):
    def __init__(self, parent, **argkw):
        super().__init__(parent,**argkw)
        self.div_mgr=self.addTab('Manager',MgrDiv)
        self.div_detail=self.addTab('Detail',DetailDiv)
        self.hideTab('Detail')
        self.toggleTab()

        self.updateAroTree=self.div_mgr.tree_map.buildTree
        self.showDetail=self.div_detail.showDetail
        self.clearDetail=self.div_detail.clearDetail
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Hide()
        return

    def onComEvt(self,e:wx.Event):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_UPDATE_MAP:
            self.updateAroTree()
            self.div_mgr.tree_sim.updateTree()
        elif etype==esevt.ETYPE_RESET_SIM:
            self.updateAroTree()
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.div_mgr.tree_sim.buildTree()
            self.div_mgr.tree_map.buildTree()
            self.div_mgr.tree_mdl.buildTree()
            self.Show()
        return

    pass
