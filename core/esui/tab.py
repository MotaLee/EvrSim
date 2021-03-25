import wx
from core import ESC,esui
yu=esui.YU
class TabBtn(esui.Div):
    _stl={'s':(8*yu,4*yu),'bgc':esui.COLOR_BACK}
    _stl_active={'bgc':esui.COLOR_LBACK}
    _stl_hover={'bgc':esui.COLOR_HOVER}

    def __init__(self, parent, **argkw):
        ''' Button used in TabDiv. Para `argkw` addition:
            * `close`: flag if tab can be closed*;
            * `icon`: img path*;'''
        # argkw['style'].update(self._stl)
        # argkw['hover']=self._stl_hover
        # argkw['active']=self._stl_active
        super().__init__(parent,**argkw)
        if len(self.label)>10:self.SetToolTip(self.label)
        self._flag_close=argkw.get('close',False)
        self.updateStyle(style={'bgc':esui.COLOR_BACK},
            hover={'bgc':esui.COLOR_HOVER},
            active={'bgc':esui.COLOR_LBACK})
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
        self._loc_btn=argkw.get('loc_btn','u')
        self._list_shown_tabs=argkw.get('labels',[])
        self.stl_tab={'p':(0,5*yu),'s':(self.Size[0],self.Size[1]-5*yu),'bgc':esui.COLOR_LBACK}
        self._dict_tabs=dict()  # {label:(tabbtn,tab),..}
        self._crt_tab=''

        if self._loc_btn=='u':
            self.div_btn=esui.Div(self,style={
                'p':(0,0),'s':(self.Size[0],5*yu)})
        for label in self._list_shown_tabs:self.addTab(label)
        if len(self._list_shown_tabs)!=0:self.toggleTab(self._list_shown_tabs[0])
        return

    def addTab(self,label,tabclass=None):
        ''' Add a new tab.
            * tab: tab class or None for adding a normal div;'''
        if label in self._dict_tabs:ESC.err('Tab existed.')
        btn=TabBtn(self.div_btn,label=label,style={
            'p':(len(self._list_shown_tabs)*(8*yu+1),yu)})
        if tabclass is None:tab=esui.Div(self,style=self.stl_tab)
        else:tab=tabclass(self,style=self.stl_tab)
        self._dict_tabs[label]=(btn,tab)
        self._list_shown_tabs.append(label)
        return tab

    def getTab(self,label=''):
        ''' Get a tab div.
            * label: Empty default for getting 1st tab;'''
        if label=='':
            if len(self._dict_tabs)==0:ESC.err('No tab.')
            label=list(self._dict_tabs.keys())[0]
        if label not in self._dict_tabs:return None
        return self._dict_tabs[label][1]

    def toggleTab(self,label=''):
        ''' Toggle to a tab with label including hided tabs.
            * label: default for the first tab.'''
        if len(self._dict_tabs)==0:ESC.err('No tab.')
        if label=='':label=list(self._dict_tabs.keys())[0]
        for k,v in self._dict_tabs.items():
            if k==label:
                v[0].act()
                v[0].Show()
                v[1].Show()
                self._crt_tabs=label
                if label not in self._list_shown_tabs:
                    self._list_shown_tabs.append(label)
            else:
                v[0].deact()
                v[1].Hide()
        return

    def hideTab(self,label):
        if len(self._dict_tabs)==0:ESC.err('No tab.')
        if self._crt_tab==label:self.toggleTab()
        self._list_shown_tabs.remove(label)
        self._dict_tabs[label][0].Hide()
        self._dict_tabs[label][1].Hide()
        return

    def clearTab(self,label):
        ''' Clear up a tab.
            * Para label: label;'''
        if len(self._dict_tabs)==0:ESC.err('No tab.')
        self._dict_tabs[label][1].DestroyChildren()
        return

    def delTab(self,label=''):
        ''' Delete tab.
            * Para label: Empty default for deleting all tabs;'''
        if len(self._dict_tabs)==0:ESC.err('No tab.')
        if label=='':
            for btn,tab in self._dict_tabs.values():
                btn.DestroyLater()
                tab.DestroyLater()
            self._dict_tabs.clear()
            self._list_shown_tabs.clear()
        else:
            if self._crt_tab==label:self.toggleTab()
            self._dict_tabs[label][0].DestroyLater()
            self._dict_tabs[label][1].DestroyLater()
            del self._dict_tabs[label]
            if label in self._list_shown_tabs:
                del self._list_shown_tabs[label]
        return
    pass
