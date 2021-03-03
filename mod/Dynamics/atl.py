import wx
import numpy as np
from core import ESC,esui,esgl,esevt,estl
from .aro import RigidGroup
from .bullet import BulletEngine

class DynamicsTool(estl.TextTool):
    def __init__(self, name, parent, p, s, label):
        super().__init__(name, parent, p, s, label)
        self.bullet_engine=None
        esui.IDX.TOOL_DIV.regToolEvent(self)
        self.Bind(esevt.EVT_RESET_SIM,self.onResetSim)
        return

    def onResetSim(self,e):
        for acplist in ESC.ACP_MODELS.values():
            for acp in acplist:
                if isinstance(acp,BulletEngine):
                    self.bullet_engine=acp
                    break
        if self.bullet_engine is not None:
            self.bullet_engine.resetSimulation()
        return
    pass

class RGMenu(estl.SelectMenuTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(esevt.EVT_UPDATE_MAP,self.onUpdateMap)
        # self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        esui.IDX.TOOL_DIV.regToolEvent(self)
        return

    def onUpdateMap(self,e):
        item_list=list()
        for aro in ESC.getFullMap():
            if type(aro)==RigidGroup:
                item_list.append(aro.AroName)
        self.setItems(item_list)
        popup=self.PopupControl
        if len(popup.items)!=0:
            self.SetLabel(popup.items[-1])
        self.Refresh()
        return

    # def onClk(self,e):
    #     popup=self.PopupControl
    #     self.SetLabel(popup.items[popup.ipos])
    #     e.Skip()
    #     return
    pass

class NewRGBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        ESC.initAro(RigidGroup,{'AroName':'New RG'})
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class DelRGBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        'todo'
        return
    pass

class ConnectRGBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if len(esgl.ARO_SELECTION)!=2:return
        aro1=esgl.ARO_SELECTION[0]
        aro2=esgl.ARO_SELECTION[1]
        rg_menu=estl.getToolByName('rg_menu','Dynamics')
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
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class RemoveFromRGBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        'todo'
        rg_menu=estl.getToolByName('rg_menu','Dynamics')
        now_rg=ESC.getAroByName(rg_menu.Label)
        rg_dict=dict(now_rg.group_dict)
        for aro in esgl.ARO_SELECTION:
            if aro.AroID in rg_dict:
                for aroid in rg_dict[aro.AroID]:
                    rg_dict[aroid].remove(aro.AroID)
                del rg_dict[aro.AroID]
        ESC.setAro(now_rg.AroID,{'group_dict':rg_dict})
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        return
    pass
