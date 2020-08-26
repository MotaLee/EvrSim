import wx
import numpy as np
from core import ESC
from core import esui
from core import esevt
from core import esgl
from .drawpart import AroDrawPart

class AroToolbarPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.selecting=False
        self.rect_selecting=False
        # self.moving=False

        yu=esui.YU
        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Aro')
        self.btn_slct=esui.BlSelectBtn(self,(0,2*yu),(4*yu,4*yu),'Slt')
        self.btn_rslct=esui.BlSelectBtn(self,(0,6*yu),(4*yu,4*yu),'RS')
        self.del_btn=esui.BorderlessBtn(self,(0,10*yu),(4*yu,4*yu),'Del')
        # self.mov_btn=esui.BlSelectBtn(self,(0,10*yu),(4*yu,4*yu),'Mov')

        self.viw_btn=esui.BorderlessMenuBtn(self,(0,self.Size[1]-12*yu),(4*yu,4*yu),'Viw',
            ['Origin','Oxy','Oxz','Oyz','Fit','Center'])
        self.prj_btn=esui.BorderlessMenuBtn(self,(0,self.Size[1]-8*yu),(4*yu,4*yu),'Prj',
            ['Orth','Prep'])
        self.grd_btn=esui.BlSelectBtn(self,(0,self.Size[1]-4*yu),(4*yu,4*yu),'Grd')

        self.btn_slct.Bind(wx.EVT_LEFT_DOWN,self.onClkBtnSlct)
        self.btn_rslct.Bind(wx.EVT_LEFT_DOWN,self.onClkBtnRS)
        # self.mov_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMoveBtn)
        self.del_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkDeleteBtn)
        self.viw_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DCLICK,self.onDClkViewBtn)
        self.viw_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkViewBtn)
        self.prj_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkProjBtn)
        return

    def onClkBtnSlct(self,e):
        if self.selecting:
            self.selecting=False
        else:
            self.selecting=True
        e.Skip()
        return

    def onClkBtnRS(self,e):
        if self.rect_selecting:
            self.rect_selecting=False
        else:
            self.rect_selecting=True
        e.Skip()
        return

    def onClkMoveBtn(self,e):
        if esui.ARO_PLC.moving:
            esui.ARO_PLC.moving=False
        else:
            esui.ARO_PLC.moving=True
        e.Skip()
        return

    def onClkDeleteBtn(self,e):
        for aro in esui.ARO_PLC.aro_selection:
            aro.adp.delDP()
            ESC.delAro(aro.AroID)
        esui.ARO_PLC.aro_selection=list()
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        e.Skip()
        return

    def onClkViewBtn(self,e):
        ppc=self.viw_btn.PopupControl
        if ppc.ipos==0:     # origin;
            esgl.EP=np.array([5,5,5])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            # esgl.TDP_LIST['GRID']=xz_grid
            esgl.WHEEL_DIS=0
        elif ppc.ipos==1:   # Oxy;
            esgl.EP=np.array([0,0,5])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            # esgl.TDP_LIST['GRID']=xy_grid
            esgl.WHEEL_DIS=0
        elif ppc.ipos==2:   # Oxz;
            esgl.EP=np.array([0,-5,0])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,0,1])
            # esgl.TDP_LIST['GRID']=xz_grid
            esgl.WHEEL_DIS=0
        elif ppc.ipos==3:   # Oyz;
            esgl.EP=np.array([-5,0,0])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            # esgl.TDP_LIST['GRID']=yz_grid
            esgl.WHEEL_DIS=0
        elif ppc.ipos==4:   # Fit;
            pass
        elif ppc.ipos==5:   # Center;
            pass
        elif ppc.ipos==6:     # Grid;
            # del esgl.TDP_LIST['GRID']
            pass
        esui.ARO_PLC.lookAt()
        e.Skip()
        return

    def onDClkViewBtn(self,e):
        ppc=self.viw_btn.PopupControl
        if ppc.ipos==1:     # Oxy;
            esgl.EP=np.array([0,0,-5])
            esgl.UP=np.array([0,1,0])
            # esgl.TDP_LIST['GRID']=xy_grid
        elif ppc.ipos==2:   # Oxz;
            esgl.EP=np.array([0,5,0])
            esgl.UP=np.array([0,0,1])
            # esgl.TDP_LIST['GRID']=xz_grid
        elif ppc.ipos==3:   # Oyz;
            esgl.EP=np.array([5,0,0])
            esgl.UP=np.array([0,1,0])
            # esgl.TDP_LIST['GRID']=yz_grid
        else: return
        esgl.AP=np.array([0,0,0])
        esgl.WHEEL_DIS=0
        esui.ARO_PLC.lookAt()
        e.Skip()
        return

    def onClkProjBtn(self,e):
        ppc=self.prj_btn.PopupControl
        if ppc.ipos==0:esgl.projMode(False)
        elif ppc.ipos==1:esgl.projMode(False)
        esui.ARO_PLC.lookAt()
        e.Skip()
        return
    pass
