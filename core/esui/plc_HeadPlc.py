import wx
from core import ESC
from core import esui
from core import esevt

class HeadPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'headpl')
        self.SetBackgroundColour(esui.COLOR_LBACK)

        yu=esui.YU
        self.es_btn=esui.BlSelectBtn(self,(1,1),(4*yu-2,4*yu-2),'ES')
        self.sim_menu=esui.BorderlessMenuBtn(self,(4*yu+1,1),(8*yu-2,4*yu-2),
            'Sim',['New','Open','Save','Save as','Setting','Manager','Close'])
        self.edit_menu=esui.BorderlessMenuBtn(self,(12*yu+1,1),(8*yu-2,4*yu-2),
            'Edit',['Undo','Redo','Copy','Cut','Paste'])
        self.map_menu=esui.BorderlessMenuBtn(self,(20*yu+1,1),(8*yu-2,4*yu-2),
            'Map',['New','Rename','Save as','Delete'])
        self.model_menu=esui.BorderlessMenuBtn(self,(28*yu+1,1),(8*yu-2,4*yu-2),
            'Model',['New','Rename','Save as','Delete'])
        self.help_menu=esui.BorderlessMenuBtn(self,(36*yu+1,1),(8*yu-2,4*yu-2),
            'Help',['Help','Read me','About'])

        self.min_btn=esui.BorderlessBtn(self,(self.Size[0]-8*yu,0),(4*yu,4*yu),'-')
        self.ext_btn=esui.BorderlessBtn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'X')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.es_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkES)
        self.min_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMin)
        self.ext_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkExt)
        self.sim_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkSim)
        self.edit_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkEdit)
        self.map_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMap)
        self.model_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkModel)

        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_LBACK))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)

        return

    def onClkES(self,e):
        if ESC.SIM_NAME=='':return
        if esui.COM_PLC.IsShown():
            esui.COM_PLC.Hide()
            esui.MOD_PLC.Show()
        else:
            esui.MOD_PLC.Hide()
            esui.COM_PLC.Show()
        e.Skip()
        return

    def onClkSim(self,e):
        DlgType=None
        fc=self.sim_menu.GetPopupControl()
        if fc.ipos==0:
            DlgType=esui.NewDialog
        elif fc.ipos==1:
            DlgType=esui.OpenDialog

        if not ESC.SIM_NAME and DlgType is None:return
        if fc.ipos==2:  # Save;
            DlgType=None
            ESC.saveSim()
            self.sim_menu.HidePopup()
        elif fc.ipos==3:    # Save as;
            DlgType=esui.SaveAsDialog
        elif fc.ipos==4:    # Setting;
            DlgType=esui.SettingDialog
        elif fc.ipos==5:    # Manager;
            pass
        elif fc.ipos==6:    # Close;
            ESC.closeSim()
            esui.SIDE_PLC.Hide()
            esui.ARO_PLC.Hide()
            esui.ACP_PLC.Hide()
            esui.MOD_PLC.Hide()
            esui.WEL_PLC.Show()

        if DlgType is not None:
            xu=esui.XU
            yu=esui.YU
            wxmw=self.Parent
            wxmw.dlgw=DlgType(wxmw,(20*xu,20*yu),(60*xu,60*yu))
            wxmw.dlgw.ShowModal()
        e.Skip()
        return

    def onClkEdit(self,e):
        if not ESC.SIM_NAME:return
        pc=self.model_menu.GetPopupControl()

        if pc.ipos==0:  # New;
            pass
        elif pc.ipos==1:    # Delete;
            pass
        elif pc.ipos==2:    # Rename;
            pass
        elif pc.ipos==3:    # Save as;
            pass
        elif pc.ipos==4:    # Manage;
            pass
        e.Skip()
        return

    def onClkMap(self,e):
        if not ESC.SIM_NAME:return
        pc=self.model_menu.GetPopupControl()

        if pc.ipos==0:  # New;
            ESC.newMapFile('New model')
            esui.SIDE_PLC.loadMaps(ESC.ARO_MAP_LIST)
        elif pc.ipos==1:    # Delete;
            pass
        elif pc.ipos==2:    # Rename;
            pass
        elif pc.ipos==3:    # Save as;
            pass
        e.Skip()
        return

    def onClkModel(self,e):
        if not ESC.SIM_NAME:return
        pc=self.model_menu.GetPopupControl()

        if pc.ipos==0:  # New;
            ESC.newModelFile('New model')
            esui.SIDE_PLC.loadModels([(ESC.SIM_NAME,'New model')])
            esui.SIDE_PLC.acp_btn.onClk(None)
            esui.SIDE_PLC.onClkAcpTabBtn(None)
        elif pc.ipos==1:    # Delete;
            pass
        elif pc.ipos==2:    # Rename;
            pass
        elif pc.ipos==3:    # Save as;
            pass
        e.Skip()
        return

    def onClkMin(self,e):
        self.Parent.Iconize()
        return

    def onClkExt(self,e):
        if ESC.SIM_FD is not None:ESC.closeSim()
        # est.kill()
        # wxapp.Destroy()
        exit()
        return

    pass
