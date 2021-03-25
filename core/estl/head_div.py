import wx
from core import ESC,esui
xu=esui.XU
yu=esui.YU

class HeadBar(esui.Div):
    ''' Base Head Bar.
        * Argkw `title`: Title text displaying in head.;'''
    def __init__(self,parent,p='default',s='default',**argkw):
        if 'style' not in argkw:argkw['style']={}
        if 'p' not in argkw['style']:argkw['style']['p']=(0,0)
        if 's' not in argkw['style']:argkw['style']['s']=(parent.Size.x,4*yu)
        argkw['style'].update({'bgc':esui.COLOR_LBACK,'border_bottom':esui.COLOR_FRONT})
        super().__init__(parent,**argkw)

        self.ori_size=argkw['style']['s']

        self.btn_min=esui.Btn(self,(self.Size[0]-8*yu,0),(4*yu,4*yu),'-',option={'border':False})
        self.btn_min.Bind(wx.EVT_LEFT_DOWN,self.onClkMin)
        self.btn_ext=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'X',option={'border':False})
        self.btn_ext.Bind(wx.EVT_LEFT_DOWN,self.onClkExt)

        if 'title' in argkw:
            self.title=esui.StaticText(self,(self.Size.x/2-10*yu,0),(20*yu,4*yu-1),argkw['title'])

        if isinstance(parent,esui.EsWindow):
            self.btn_es=esui.SltBtn(self,(0,1),(4*yu,4*yu-2),'ES',option={'border':False})
        return

    def onClkMin(self,e):
        SP=self.Parent
        if isinstance(SP,esui.EsWindow):
            SP.Iconize()
        else:
            if SP.Size.x<self.ori_size[0]:
                SP.SetSize(yu*8,yu*4)
            else:SP.SetSize(self.ori_size)
        return

    def onClkExt(self,e):
        if ESC.isSimOpened():ESC.closeSim()
        esui.sendComEvt(esui.ETYPE_CLOSE_ES)
        # wxapp.Destroy()
        exit()
        return
    pass

class HeadDiv(HeadBar):
    ''' Head Panel Container.
        * Argkw : None;'''
    def __init__(self,parent,**argkw):
        ctrl_h=4*yu-1
        super().__init__(parent,**argkw)

        self.menu_sim=esui.MenuBtnDiv(self,label='Sim',no_border=True,
            style={'p':(4*yu,0),'s':(8*yu,ctrl_h)},
            items=['New..','Open..','Save','Save as..','Setting..','Close'])
        self.menu_edit=esui.MenuBtnDiv(self,label='Edit',no_border=True,
            style={'p':(12*yu,0),'s':(8*yu,ctrl_h)},
            items=['Undo','Redo','Copy','Cut','Paste'])
        self.menu_map=esui.MenuBtnDiv(self,label='Map',no_border=True,
            style={'p':(20*yu,0),'s':(8*yu,ctrl_h)},
            items=['New..','Rename..','Save as..','Delete'])
        self.menu_model=esui.MenuBtnDiv(self,label='Model',no_border=True,
            style={'p':(28*yu,0),'s':(8*yu,ctrl_h)},
            items=['New..','Rename..','Save as..','Delete'])
        self.menu_mod=esui.MenuBtnDiv(self,label='Mod',no_border=True,
            style={'p':(36*yu,0),'s':(8*yu,ctrl_h)},
            items=['Manager','Pack'])
        self.menu_help=esui.MenuBtnDiv(self,label='Help',no_border=True,
            style={'p':(44*yu,0),'s':(8*yu,ctrl_h)},
            items=['Help..','Read me..','About..'])

        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.btn_es.Bind(wx.EVT_LEFT_DOWN,self.onClkES)
        self.menu_sim.bindPopup(wx.EVT_LEFT_DOWN,self.onClkSim)
        self.menu_edit.bindPopup(wx.EVT_LEFT_DOWN,self.onClkEdit)
        self.menu_map.bindPopup(wx.EVT_LEFT_DOWN,self.onClkMap)
        self.menu_model.bindPopup(wx.EVT_LEFT_DOWN,self.onClkModel)
        self.menu_mod.bindPopup(wx.EVT_LEFT_DOWN,self.onClkMod)

        return

    def onComEvt(self,e):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_OPEN_CMD:
            self.btn_es.SetValue(True)
        elif etype==esui.ETYPE_CLOSE_CMD:
            self.btn_es.SetValue(False)
        e.Skip()
        return

    def onClkES(self,e):
        if not ESC.isSimOpened():return
        if e.EventObject.GetValue():
            esui.sendComEvt(esui.ETYPE_CLOSE_CMD)
        else:
            esui.sendComEvt(esui.ETYPE_OPEN_CMD)
        return

    def onClkSim(self,e:wx.Event):
        DlgType=None
        pi=e.EventObject.popup_index
        if pi==0:
            if not ESC.isSimOpened():
                DlgType=esui.NewDialog
            else:
                'todo: new sim after already opened another sim;'
        elif pi==1:
            DlgType=esui.OpenDialog

        if not ESC.isSimOpened() and DlgType is None:return
        if pi==2:  # Save;
            DlgType=None
            ESC.saveSim()
            self.menu_sim.HidePopup()
        elif pi==3:    # Save as;
            DlgType=esui.SaveAsDialog
        elif pi==4:    # Setting;
            DlgType=esui.SettingDialog
        elif pi==5:    # Close;
            ESC.closeSim()
            esui.UMR.SIDE_DIV.Hide()
            esui.UMR.MAP_DIV.Hide()
            esui.UMR.MDL_DIV.Hide()
            esui.UMR.TOOL_DIV.Hide()

        if DlgType is not None:
            esui.UMR.ESMW.dialog=DlgType(esui.UMR.ESMW,(20*xu,20*yu),(60*xu,60*yu))
            esui.UMR.ESMW.dialog.ShowModal()
        e.Skip()
        return

    def onClkEdit(self,e):
        if not ESC.isSimOpened():return
        pi=e.EventObject.popup_index
        if pi==0:  # Undo
            pass
        elif pi==1:    # Redo
            pass
        elif pi==2:    # Copy
            if esui.UMR.MDL_DIV.IsShown():
                esui.UMR.MDL_DIV.onKeyDown(None,operation='Copy')
        elif pi==3:    # Cut
            if esui.UMR.MDL_DIV.IsShown():
                esui.UMR.MDL_DIV.onKeyDown(None,operation='Cut')
        elif pi==4:    # Paste
            if esui.UMR.MDL_DIV.IsShown():
                esui.UMR.MDL_DIV.onKeyDown(None,operation='Paste')
        e.Skip()
        return

    def onClkMap(self,e):
        if not ESC.isSimOpened():return
        pi=e.EventObject.popup_index
        if pi==0:  # New;
            operation='New'
        elif pi==1:    # Rename;
            operation='Rename'
        elif pi==2:    # Save as;
            operation='Saveas'
        wxmw=self.Parent
        wxmw.dlgw=esui.MapDialog(wxmw,(30*xu,40*yu),(40*xu,20*yu),operation)
        wxmw.dlgw.ShowModal()
        e.Skip()
        return

    def onClkModel(self,e):
        if not ESC.isSimOpened():return
        pi=e.EventObject.popup_index
        if pi==0:  # New;
            operation='New'
        elif pi==1:    # Rename;
            if len(esui.UMR.MDL_DIV.model_tuple)==0:
                return ESC.err('Model not opened.')
            elif esui.UMR.MDL_DIV.model_tuple[0]!=ESC.SIM_NAME:
                return ESC.err('#: Model in mod cannot be modified.')
            operation='Rename'
        elif pi==2:    # Save as;
            operation='Saveas'
        elif pi==3:
            operation='Delete'
        wxmw=self.Parent
        wxmw.dlgw=esui.ModelDialog(wxmw,(30*xu,40*yu),(40*xu,20*yu),operation)
        wxmw.dlgw.ShowModal()
        e.Skip()
        return

    def onClkMod(self,e):
        if not ESC.isSimOpened():return
        DlgType=None
        pi=e.EventObject.popup_index
        if pi==0:  # Load;
            DlgType=esui.ModDialog
            pass
        elif pi==1:    # Pack;
            pass

        if DlgType is not None:
            esui.UMR.ESMW.dialog=DlgType(esui.UMR.ESMW,(20*xu,20*yu),(60*xu,60*yu))
            esui.UMR.ESMW.dialog.ShowModal()
        e.Skip()
        return
    pass
