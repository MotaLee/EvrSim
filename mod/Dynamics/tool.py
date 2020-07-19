import wx
import numpy as np
from core import ESC
from core import esui
from core import esevt
from core import estool
from .aro import RigidGroup

class RGMenuTool(estool.SelectMenuTool):
    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(esevt.EVT_UPDATE_MAP,self.onUpdateMap)
        self.ctrl.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        esui.MOD_PLC.regToolEvent(self)
        return

    def onUpdateMap(self,e):
        item_list=list()
        for aro in ESC.ARO_MAP:
            if type(aro)==RigidGroup:
                item_list.append(aro.AroName)
        self.ctrl.setItems(item_list)
        popup=self.ctrl.PopupControl
        if len(popup.items)!=0:
            self.ctrl.SetLabel(popup.items[-1])
        self.ctrl.Refresh()
        return

    def onClk(self,e):
        popup=self.ctrl.PopupControl
        self.ctrl.SetLabel(popup.items[popup.ipos])
        e.Skip()
        return
    pass

class NewRGTool(estool.ButtonTool):
    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        ESC.initAro(RigidGroup,{'AroName':'New RG'})
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_UPDATE_MAP)
        return
    pass

class DelRGTool(estool.ButtonTool):
    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):

        return
    pass

class ConnectRGTool(estool.ButtonTool):
    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if len(esui.ARO_PLC.aro_selection)!=2:return
        aro1=esui.ARO_PLC.aro_selection[0]
        aro2=esui.ARO_PLC.aro_selection[1]
        rg_menu=self.getToolCtrlByName('rg_menu')
        now_rg=ESC.getAroByName(rg_menu.Label)
        rg_dict=dict(now_rg.group_dict)
        if aro1.AroID not in rg_dict:
            rg_dict[aro1.AroID]=[aro2.AroID]
        else:
            rg_dict[aro1.AroID].append(aro2.AroID)
        if aro2.AroID not in rg_dict:
            rg_dict[aro2.AroID]=[aro1.AroID]
        else:
            rg_dict[aro2.AroID].append(aro1.AroID)

        ESC.setAro(now_rg.AroID,{'group_dict':rg_dict})
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_UPDATE_MAP)
        return
    pass

class RemoveFromRGTool(estool.ButtonTool):
    def build(self,parent):
        super().build(parent)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):

        return
    pass
