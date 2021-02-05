import wx
from core import ESC
from core import esui
from core import esevt
xu=esui.XU
yu=esui.YU

class HeadBar(esui.Plc):
    ''' Base Head Bar.

        Para argkw accepts:

        `title`: Title text displaying in head.;'''
    def __init__(self,parent,p='default',s='default',**argkw):
        if p=='default':p=(0,0)
        if s=='default':s=(parent.Size.x,4*yu)
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.ori_size=s

        self.btn_min=esui.BorderlessBtn(self,(self.Size[0]-8*yu,0),(4*yu,4*yu),'-')
        self.btn_min.Bind(wx.EVT_LEFT_DOWN,self.onClkMin)
        self.btn_ext=esui.BorderlessBtn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'X')
        self.btn_ext.Bind(wx.EVT_LEFT_DOWN,self.onClkExt)

        if 'title' in argkw:
            self.title=esui.StaticText(self,(self.Size.x/2-10*yu,0),(20*yu,4*yu-1),argkw['title'])

        if isinstance(parent,esui.EsWindow):
            self.btn_es=esui.BlSelectBtn(self,(0,1),(4*yu,4*yu-2),'ES')
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return

    def onClkMin(self,e):
        SP=self.Parent
        if isinstance(SP,esui.EsWindow):
            SP.Iconize()
        else:
            if SP.Size.x<self.ori_size[0]:
                SP.SetSize(esui.YU*8,esui.YU*4)
            else:SP.SetSize(self.ori_size)
        return

    def onClkExt(self,e):
        if ESC.SIM_NAME!='':ESC.closeSim()
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_CLOSE_ES)
        # wxapp.Destroy()
        exit()
        return
    pass

class HeadPlc(HeadBar):
    ''' Head Panel Container.

        Para argkw accepts: None;'''
    def __init__(self,parent,p='default',s='default',**argkw):
        ctrl_h=4*yu-1
        super().__init__(parent,p,s)

        self.menu_sim=esui.BorderlessMenuBtn(self,(4*yu,0),(8*yu,ctrl_h),
            'Sim',['New..','Open..','Save','Save as..','Setting..','Close'])
        self.menu_edit=esui.BorderlessMenuBtn(self,(12*yu,0),(8*yu,ctrl_h),
            'Edit',['Undo','Redo','Copy','Cut','Paste'])
        self.menu_map=esui.BorderlessMenuBtn(self,(20*yu,0),(8*yu,ctrl_h),
            'Map',['New..','Rename..','Save as..','Delete'])
        self.menu_model=esui.BorderlessMenuBtn(self,(28*yu,0),(8*yu,ctrl_h),
            'Model',['New..','Rename..','Save as..','Delete'])
        self.menu_mod=esui.BorderlessMenuBtn(self,(36*yu,0),(8*yu,ctrl_h),
            'Mod',['Manager','Pack'])
        self.menu_help=esui.BorderlessMenuBtn(self,(44*yu,0),(8*yu,ctrl_h),
            'Help',['Help..','Read me..','About..'])

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.btn_es.Bind(wx.EVT_LEFT_DOWN,self.onClkES)
        self.menu_sim.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkSim)
        self.menu_edit.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkEdit)
        self.menu_map.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMap)
        self.menu_model.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkModel)
        self.menu_mod.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMod)

        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_OPEN_CMD:
            self.btn_es.SetValue(True)
        elif etype==esevt.ETYPE_CLOSE_CMD:
            self.btn_es.SetValue(False)
        e.Skip()
        return

    def onClkES(self,e):
        if ESC.SIM_NAME=='':return
        if e.EventObject.GetValue():
            esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_CLOSE_CMD)
        else:
            esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_OPEN_CMD)
        return

    def onClkSim(self,e):
        DlgType=None
        fc=self.menu_sim.GetPopupControl()
        if fc.ipos==0:
            if ESC.SIM_NAME=='':
                DlgType=esui.NewDialog
            else:
                'todo: new sim after already opened another sim;'
        elif fc.ipos==1:
            DlgType=esui.OpenDialog

        if not ESC.SIM_NAME and DlgType is None:return
        if fc.ipos==2:  # Save;
            DlgType=None
            ESC.saveSim()
            self.menu_sim.HidePopup()
        elif fc.ipos==3:    # Save as;
            DlgType=esui.SaveAsDialog
        elif fc.ipos==4:    # Setting;
            DlgType=esui.SettingDialog
        elif fc.ipos==5:    # Close;
            ESC.closeSim()
            esui.SIDE_PLC.Hide()
            esui.ARO_PLC.Hide()
            esui.ACP_PLC.Hide()
            esui.TOOL_PLC.Hide()

        if DlgType is not None:
            xu=esui.XU
            yu=esui.YU
            esui.WXMW.dialog=DlgType(esui.WXMW,(20*xu,20*yu),(60*xu,60*yu))
            esui.WXMW.dialog.ShowModal()
        e.Skip()
        return

    def onClkEdit(self,e):
        if not ESC.SIM_NAME:return
        pc=self.menu_edit.GetPopupControl()

        if pc.ipos==0:  # Undo
            pass
        elif pc.ipos==1:    # Redo
            pass
        elif pc.ipos==2:    # Copy
            if esui.ACP_PLC.IsShown():
                esui.ACP_PLC.onKeyDown(None,operation='Copy')
        elif pc.ipos==3:    # Cut
            if esui.ACP_PLC.IsShown():
                esui.ACP_PLC.onKeyDown(None,operation='Cut')
        elif pc.ipos==4:    # Paste
            if esui.ACP_PLC.IsShown():
                esui.ACP_PLC.onKeyDown(None,operation='Paste')
        e.Skip()
        return

    def onClkMap(self,e):
        if not ESC.SIM_NAME:return
        pc=self.menu_map.GetPopupControl()
        if pc.ipos==0:  # New;
            operation='New'
        elif pc.ipos==1:    # Rename;
            operation='Rename'
        elif pc.ipos==2:    # Save as;
            operation='Saveas'
        xu=esui.XU
        yu=esui.YU
        wxmw=self.Parent
        wxmw.dlgw=esui.MapDialog(wxmw,(30*xu,40*yu),(40*xu,20*yu),operation)
        wxmw.dlgw.ShowModal()
        e.Skip()
        return

    def onClkModel(self,e):
        if not ESC.SIM_NAME:return
        pc=self.menu_model.GetPopupControl()
        if pc.ipos==0:  # New;
            operation='New'
        elif pc.ipos==1:    # Rename;
            if len(esui.ACP_PLC.model_tuple)==0:
                return ESC.bug('Model not opened.')
            elif esui.ACP_PLC.model_tuple[0]!=ESC.SIM_NAME:
                return ESC.bug('#: Model in mod cannot be modified.')
            operation='Rename'
        elif pc.ipos==2:    # Save as;
            operation='Saveas'
        elif pc.ipos==3:
            operation='Delete'
        wxmw=self.Parent
        wxmw.dlgw=esui.ModelDialog(wxmw,(30*xu,40*yu),(40*xu,20*yu),operation)
        wxmw.dlgw.ShowModal()
        e.Skip()
        return

    def onClkMod(self,e):
        if not ESC.SIM_NAME:return
        DlgType=None
        fc=self.menu_mod.GetPopupControl()
        if fc.ipos==0:  # Load;
            DlgType=esui.ModDialog
            pass
        elif fc.ipos==1:    # Pack;
            pass

        if DlgType is not None:
            xu=esui.XU
            yu=esui.YU
            esui.WXMW.dialog=DlgType(esui.WXMW,(20*xu,20*yu),(60*xu,60*yu))
            esui.WXMW.dialog.ShowModal()
        e.Skip()
        return
    pass
