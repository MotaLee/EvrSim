# -*- coding: UTF-8 -*-
import wx
from core import ESC,esui,esevt
from .manager import MgrDiv
from .detail import DetailDiv
yu=esui.YU

class TabBtn(esui.Div):
    _stl={'s':(8*yu,4*yu),'bgc':esui.COLOR_BACK}
    _stl_active={'bgc':esui.COLOR_LBACK}
    _stl_hover={'bgc':esui.COLOR_ACTIVE}

    def __init__(self, parent, **argkw):
        ''' Button used in TabDiv. Para `argkw` addition:
            * `close`: flag if tab can be closed*;
            * `icon`: img path*;'''
        argkw['style'].update(self._stl)
        argkw['hover']=self._stl_hover
        argkw['active']=self._stl_active
        super().__init__(parent,**argkw)

        if len(self.label)>10:self.SetToolTip(self.label)
        self._flag_close=argkw.get('close',False)

        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e:wx.Event):
        # self._onClk(e)
        self.GrandParent.toggleTab(self.label)
        return

    def act(self):
        self._flag_active=True
        self.Refresh()
        return

    def deact(self):
        self._flag_active=False
        self.Refresh()
        return
    pass
class TabDiv(esui.Div):
    def __init__(self, parent, **argkw):
        '''Para argkw addition:
        * loc_btn: location of tab buttons, enum for udlr;
        * labels: initial list of tabs;'''
        super().__init__(parent, **argkw)
        self._p_tab=(0,5*yu)
        self._s_tab=(self.Size[0],self.Size[1]-5*yu)
        self._loc_btn=argkw.get('loc_btn','u')
        self._dict_tabs=dict()  # {label:(tabbtn,tab),..}
        self._list_shown_tabs=argkw.get('labels',[])
        self._crt_tab=''

        if self._loc_btn=='u':
            self._div_btn=esui.Div(self,style={
                'p':(0,0),'s':(self.Size[0],5*yu)})
        for label in self._list_shown_tabs:self.addTab(label)
        if len(self._list_shown_tabs)!=0:self.toggleTab(self._list_shown_tabs[0])
        return

    def addTab(self,label,tab=None):
        ''' Add a new tab.
            * tab: tab class or None for adding a normal div;'''
        btn=TabBtn(self._div_btn,label=label,style={
            'p':(len(self._list_shown_tabs)*(8*yu+1),yu)})
        if tab is None:
            tab=esui.Div(self,style={
                'p':self._p_tab,'s':self._s_tab,'bgc':esui.COLOR_LBACK})
        else:
            tab=tab(self,style={
                'p':self._p_tab,'s':self._s_tab,'bgc':esui.COLOR_LBACK})
        self._dict_tabs[label]=(btn,tab)
        self._list_shown_tabs.append(label)
        return tab

    def getTab(self,label=''):
        ''' Get a tab div.
            * label: get a tab with existed label;
            * toggle: if toggle to the tab after getting;'''
        if label=='':label=list(self._dict_tabs.keys())[0]
        if label not in self._dict_tabs:return None
        return self._dict_tabs[label][1]

    def toggleTab(self,label=''):
        ''' Toggle to a tab with label including hided tabs.
            * label: default for the first tab.'''
        if label=='':label=list(self._dict_tabs.keys())[0]
        for k,v in self._dict_tabs.items():
            if k==label:
                v[0].act()
                v[0].Show()
                v[1].Show()
                self._crt_tabs=label
                self._list_shown_tabs.append(label)
            else:
                v[0].deact()
                v[1].Hide()
        return

    def hideTab(self,label,clear=False):
        if clear and self._crt_tab==label:self.toggleTab()
        for k,v in self._dict_tabs.items():
            if k==label:
                self._list_shown_tabs.remove(label)
                if clear:
                    v[0].DestroyLater()
                    v[1].DestroyLater()
                    del self._dict_tabs[k]
                else:
                    v[0].Hide()
                    v[1].Hide()
                break
        return
    pass

class SideDiv(TabDiv):
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
