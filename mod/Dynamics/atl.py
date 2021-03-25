import wx
from core import ESC,esui,esgl
GLC=esgl.glc
from .aro import BodyCombo
from .bullet import BulletEngine

class DynamicsTool(esui.DivText):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.bullet_engine=None
        esui.UMR.ESMW.regToolEvent(self)
        self.Bind(esui.EBIND_RESET_SIM,self.onResetSim)
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

class MenuBC(esui.MenuBtnDiv):
    def __init__(self, parent, **argkw):
        super().__init__(parent, **argkw)
        self.Bind(esui.EBIND_UPDATE_MAP,self.onUpdateMap)
        esui.UMR.ESMW.regToolEvent(self)
        return

    def onUpdateMap(self,e):
        item_list=[aro.AroName
            for aro in ESC.getFullMap()
            if isinstance(aro,BodyCombo)]
        self.setItems(item_list)
        if len(self.items)!=0:
            self.setLabel(self.items[-1])
        return
    pass

class BtnBC(esui.DivBtn):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):

        if self.label=='Append':
            ESC.addAro(AroClass=BodyCombo,AroName='New RG')
            esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        elif self.label=='Remove':
            pass
        return
    pass
