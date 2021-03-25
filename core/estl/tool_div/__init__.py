import wx
import mod
from core import ESC,esui
yu=esui.YU
xu=esui.XU

class ToolDiv(esui.TabDiv):
    def __init__(self,parent,**argkw):
        argkw['style'].update({'border_bottom':esui.COLOR_FRONT})
        super().__init__(parent,**argkw)
        self.list_tab=list()
        self.flag_single=False
        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.Hide()
        return

    def onComEvt(self,e):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_OPEN_CMD:
            self.Hide()
        elif etype==esui.ETYPE_CLOSE_CMD:
            self.Show()
        elif etype==esui.ETYPE_OPEN_SIM:
            self.Show()
        elif etype==esui.ETYPE_LOAD_MOD:
            self.Show()
            self.toggleTab()

        return

    def getModTab(self,modname):
        ''' Get the mod tab.'''
        tab=self.getTab(modname)
        if tab is None:
            tab=self.addTab(modname,ModTab)
            tab.Label=modname
        return tab

    def toggleSingleMode(self,modname):
        tab=self.getTab(modname)
        if tab is None:ESC.err('Tab not found.')
        self.toggleTab(modname)
        if not self.flag_single:
            self.div_btn.Hide()
            self._dict_tabs[modname][1].SetPosition((0,0))
            self._dict_tabs[modname][1].SetSize(self.Size)
        else:
            self.div_btn.Show()
            self._dict_tabs[modname][1].updateStyle(self.stl_tab)
        self.flag_single=not self.flag_single
        return
    pass

class ModTab(esui.ScrollDiv):
    def __init__(self,parent,**argkw):
        super().__init__(parent,axis='X',**argkw)
        self.Hide()
    pass
