import wx
from core import ESC,esui,esgl
GLC=esgl.GLC
from .aro import BodyCombo,RigidBody,Beam2D,RefPoint
from .bullet import BulletEngine

class DynamicsTool(esui.DivText):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.bullet_engine=None
        self.z3_solver=None
        self.Bind(esui.EBIND_RESET_SIM,self.onResetSim)
        self.Bind(esui.EBIND_UPDATE_MAP,self.onUpdateMap)
        esui.UMR.ESMW.regToolEvent(self)
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

    def onUpdateMap(self,e):
        refs=[ESC.getLinkAro(aro,'refs')
            for aro in ESC.getFullMap()
            if isinstance(aro,BodyCombo)]

        for child in ESC.getLinkAro(refs[0],'children'):
            if isinstance(child,RefPoint):
                ref_aro=ESC.getLinkAro(child,'ref')
                if isinstance(ref_aro,Beam2D):
                    ESC.setAro(child,position=getattr(ref_aro,child.refattr))
        return
    pass

class MenuBC(esui.MenuBtnDiv):
    def __init__(self, parent, **argkw):
        super().__init__(parent, **argkw)
        self.list_aroid=[]
        self.list_name=[]
        self.Bind(esui.EBIND_OPEN_SIM,self.onUpdateMap)
        self.Bind(esui.EBIND_UPDATE_MAP,self.onUpdateMap)
        esui.UMR.ESMW.regToolEvent(self)
        return

    def onUpdateMap(self,e):
        self.list_aroid.clear()
        self.list_name.clear()
        for aro in ESC.getFullMap():
            if isinstance(aro,BodyCombo):
                self.list_name.append(aro.AroName)
                self.list_aroid.append(aro.AroName)
        self.setItems(self.list_name)
        if len(self.items)!=0:
            self.setLabel(self.items[-1])
        return

    def getCurrentBC(self):
        name=self.label
        try:
            idx=self.list_name.index(name)
            aroid=self.list_aroid[idx]
        except BaseException:aroid=-1
        bc:BodyCombo=ESC.getAro(aroid)
        return bc
    pass

class BtnBC(esui.DivBtn):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        from . import menu_bc
        bc=menu_bc.getCurrentBC()
        if bc is None:return
        refs=ESC.getLinkAro(bc,'refs')
        tar=GLC.getSelection()
        if len(tar)==0:return
        else: tar:RigidBody=tar[0]

        if self.label=='Append':
            if isinstance(tar,Beam2D):
                ESC.linkAro(bc,tar)
                ptf=ESC.addAro(AroClass=RefPoint,
                    AroName='RP1-'+tar.AroName,
                    ref=tar.AroID,refattr='ptf')
                pts=ESC.addAro(AroClass=RefPoint,
                    AroName='RP2-'+tar.AroName,
                    ref=tar.AroID,refattr='pts')
                ESC.linkAro(refs,[ptf,pts])
            esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        elif self.label=='Remove':
            if tar.AroID not in bc.children:return
            ESC.linkAro(bc,tar)
            children=ESC.getLinkAro(refs,'children')
            for child in children:
                if child.ref==tar.AroID:
                    ESC.linkAro(refs,child)
                    ESC.delAro(child)
            esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        elif self.label=='Connect':
            pass
        return
    pass
