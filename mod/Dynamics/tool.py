import wx
import numpy as np
from core import ESC
from core import esui
from core import esevt
from core import estool
from .aro import RigidGroup

class RGMenu(estool.SelectMenuTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(esevt.EVT_UPDATE_MAP,self.onUpdateMap)
        self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        esui.TOOL_PLC.regToolEvent(self)
        return

    def onUpdateMap(self,e):
        item_list=list()
        for aro in ESC.ARO_MAP:
            if type(aro)==RigidGroup:
                item_list.append(aro.AroName)
        self.setItems(item_list)
        popup=self.PopupControl
        if len(popup.items)!=0:
            self.SetLabel(popup.items[-1])
        self.Refresh()
        return

    def onClk(self,e):
        popup=self.PopupControl
        self.SetLabel(popup.items[popup.ipos])
        e.Skip()
        return
    pass

class NewRGBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        ESC.initAro(RigidGroup,{'AroName':'New RG'})
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class DelRGBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        'todo'
        return
    pass

class ConnectRGBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if len(esui.ARO_PLC.aro_selection)!=2:return
        aro1=esui.ARO_PLC.aro_selection[0]
        aro2=esui.ARO_PLC.aro_selection[1]
        rg_menu=estool.getToolByName('rg_menu','Dynamics')
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
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class RemoveFromRGBtn(estool.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        'todo'
        rg_menu=estool.getToolByName('rg_menu','Dynamics')
        now_rg=ESC.getAroByName(rg_menu.Label)
        rg_dict=dict(now_rg.group_dict)
        for aro in esui.ARO_PLC.aro_selection:
            if aro.AroID in rg_dict:
                for aroid in rg_dict[aro.AroID]:
                    rg_dict[aroid].remove(aro.AroID)
                del rg_dict[aro.AroID]
        ESC.setAro(now_rg.AroID,{'group_dict':rg_dict})
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        return
    pass
