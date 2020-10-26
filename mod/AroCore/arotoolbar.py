import wx,glm,interval
import numpy as np
from core import ESC,esui,esgl,esevt,estool
AroDrawPart=esgl.drawpart.AroDrawPart
yu=esui.YU

class AroToolbarPlc(estool.UIGLTool):
    def __init__(self):
        super().__init__('AroToolbar',(0,0),(4*yu,esui.ARO_PLC.Size.y))
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.host=esui.ARO_PLC
        self.selecting=False
        self.rect_selecting=False
        # self.moving=False

        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Aro')
        self.btn_slct=esui.BlSelectBtn(self,(0,2*yu),(4*yu,4*yu),'Slt')
        self.btn_rslct=esui.BlSelectBtn(self,(0,6*yu),(4*yu,4*yu),'RS')
        self.del_btn=esui.BorderlessBtn(self,(0,10*yu),(4*yu,4*yu),'Del')
        self.mov_btn=esui.BlSelectBtn(self,(0,14*yu),(4*yu,4*yu),'Mov')

        self.viw_btn=esui.BorderlessMenuBtn(self,(0,self.Size.y-8*yu),(4*yu,4*yu),'Viw',
            ['Origin','Oxy','Oxz','Oyz','Fit','Center'])
        self.prj_btn=esui.BorderlessMenuBtn(self,(0,self.Size.y-4*yu),(4*yu,4*yu),'Prj',
            ['Orth','Prep'])

        self.btn_slct.Bind(wx.EVT_LEFT_DOWN,self.onClkBtnSlct)
        self.btn_rslct.Bind(wx.EVT_LEFT_DOWN,self.onClkBtnRS)
        # self.mov_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMoveBtn)
        self.del_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkDeleteBtn)
        self.viw_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DCLICK,self.onDClkViewBtn)
        self.viw_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkViewBtn)
        self.prj_btn.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkProjBtn)

        self.host.Bind(wx.EVT_MOUSEWHEEL,self.onRoWhl)
        self.host.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.host.Bind(wx.EVT_LEFT_DCLICK, self.onDClk)
        self.host.Bind(wx.EVT_LEFT_UP, self.onRls)
        self.host.Bind(wx.EVT_MOTION,self.onMove)
        self.host.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhl)

        return

    def onClk(self,e):
        TOR=0.05
        self.host.SetFocus()
        cpos=e.GetPosition()
        cx,cy=esgl.normPos(cpos)
        self.host.spos=cpos
        all_adp=list()
        if self.selecting:
            if e.controlDown:
                for adplist in esgl.ADP_DICT.values():
                    all_adp+=adplist()
                for adp in all_adp:
                    if not hasattr(adp.Aro,'position'):continue
                    slct=False
                    for p in adp.VA:
                        p_2d=esgl.getPosFromVertex(adp,p)
                        if abs(cx-p_2d[0])<TOR and abs(cy-p_2d[1])<TOR:
                            self.host.aro_selection.append(adp.Aro)
                            adp.highlight=True
                            slct=True
                            break
                    if slct:break
            else:
                self.host.aro_selection=[]
                for adplist in esgl.ADP_DICT.values():
                    all_adp+=adplist
                for adp in all_adp:
                    if not hasattr(adp.Aro,'position'):continue
                    slct=False
                    for p in adp.VA:
                        p_2d=esgl.getPosFromVertex(adp,p)
                        if abs(cx-p_2d[0])<TOR and abs(cy-p_2d[1])<TOR:
                            self.host.aro_selection=[adp.Aro]
                            adp.highlight=True
                            slct=True
                            break
                    if slct:break
                    else:adp.highlight=False
        else:pass
        esgl.drawGL()
        return

    def onClkWhl(self,e):
        self.host.spos=e.GetPosition()
        e.Skip()
        return

    def onRoWhl(self,e):
        t=np.sign(e.WheelRotation)
        if esgl.WHEEL_DIS==-10 and t>0:return
        if esgl.WHEEL_DIS==15 and t<0:return
        cpos=e.GetPosition()
        cx,cy=esgl.normPos(cpos)

        v_ae=esgl.EP-esgl.AP
        z1=(v_ae)/np.linalg.norm(v_ae)    # ev_ae;
        x1=np.cross(esgl.UP,z1)
        x1=x1/np.linalg.norm(x1)
        y1=np.cross(z1,x1)
        y1=y1/np.linalg.norm(y1)
        v_ac=0.414/esgl.ZS*np.array([cx*esgl.ASPECT_RATIO,cy,0])
        v_ac=v_ac[0]*x1+v_ac[1]*y1
        esgl.AP=esgl.AP+t*v_ac-t/esgl.ZS*z1
        esgl.EP=esgl.EP+t*v_ac-t/esgl.ZS*z1
        esgl.WHEEL_DIS-=t
        esgl.projMode()
        esgl.lookAt()
        e.Skip()
        return

    def onDClk(self,e):
        if len(self.host.aro_selection)==1:
            esui.SIDE_PLC.showDetail(self.aro_selection[0].AroID)
        return

    def onRls(self,e):
        if self.rect_selecting:
            self.host.aro_selection=[]
            cpos=e.GetPosition()
            cx,cy=esgl.normPos(cpos)
            sx,sy=esgl.normPos(self.host.spos)
            all_adp=list()
            for adplist in esgl.ADP_DICT.values():
                all_adp+=adplist
            for adp in all_adp:
                if not hasattr(adp.Aro,'position'):continue
                slct=False
                for p in adp.VA:
                    p_2d=esgl.getPosFromVertex(adp,p)
                    c1=p_2d[0] in interval.Interval(cx,sx)
                    c2=p_2d[1] in interval.Interval(cy,sy)
                    if c1 and c2:
                        self.host.aro_selection.append(adp.Aro)
                        adp.highlight=True
                        slct=True
                        break
                if not slct:adp.highlight=False
            self.host.spos=cpos
            esgl.drawGL()
        return

    def onMove(self,e):
        cpos=e.GetPosition()
        spos=self.host.spos
        if e.leftIsDown and self.rect_selecting:
            esgl.drawGL()
            dc=wx.ClientDC(self.host)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawRectangle(spos[0],spos[1],
                cpos[0]-spos[0],cpos[1]-spos[1])
        elif e.middleIsDown:
            esgl.UP=np.array([0,1,0])
            dx=(cpos.x-spos.x)/self.host.Size.y*glm.pi()
            dy=(spos.y-cpos.y)/self.host.Size.y*glm.pi()
            self.host.spos=cpos
            v_ae=esgl.EP-esgl.AP
            r=np.linalg.norm(v_ae)
            tmp=v_ae[1]/r
            if abs(tmp)>1: tmp=1
            if v_ae[0]==0:
                theta=glm.acos(tmp)
                psi=np.sign(v_ae[2])*glm.pi()/2
            else:
                psi=glm.atan(v_ae[2]/v_ae[0])
                theta=glm.acos(tmp)*np.sign(v_ae[0])
            if abs(theta)<0.1:
                if dy<0:dy=0
            elif abs(theta-glm.pi())<0.1:
                if dy>0:dy=0
            if v_ae[0]==0:theta+=dy
            else:theta+=(dy*np.sign(v_ae[0]))
            psi+=dx
            v_ae=np.array([r*glm.sin(theta)*glm.cos(psi),
                r*glm.cos(theta),
                r*glm.sin(theta)*glm.sin(psi)])
            esgl.EP=v_ae+esgl.AP
            esgl.lookAt()
        e.Skip()
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
            ESC.delAro(aro.AroID)
        esui.ARO_PLC.aro_selection=list()
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
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
        esgl.lookAt()
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
        esgl.lookAt()
        e.Skip()
        return

    def onClkProjBtn(self,e):
        ppc=self.prj_btn.PopupControl
        if ppc.ipos==0:esgl.projMode(False)
        elif ppc.ipos==1:esgl.projMode(False)
        esgl.lookAt()
        e.Skip()
        return
    pass
