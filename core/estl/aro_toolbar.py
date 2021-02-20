import wx,interval
import _glm as glm
import numpy as np
from core import ESC,esui,esgl,esevt,estl
# AroDrawPart=esgl.drawpart.AroDrawPart
yu=esui.YU

class AroToolbar(estl.UIGLTool):
    def __init__(self):
        super().__init__('AroToolbar',(0,0),(4*yu,esui.ARO_PLC.Size.y))
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.host=esui.ARO_PLC
        self.spos=(0,0)
        self.state_select=['None','Pick']    # enum with [None, Pick, Rect, Picktop]
        self.show_tab=False

        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Aro')
        self.btn_slct=esui.SltBtn(self,(0,2*yu),(4*yu,4*yu),'Slt',option={'border':False})
        # self.btn_rslct=esui.BlSelectBtn(self,(0,6*yu),(4*yu,4*yu),'RS')
        self.btn_del=esui.Btn(self,(0,10*yu),(4*yu,4*yu),'Del',option={'border':False,'ext':True})
        self.btn_mov=esui.SltBtn(self,(0,14*yu),(4*yu,4*yu),'Mov',option={'border':False})

        self.btn_viw=esui.BorderlessMenuBtn(self,(0,self.Size.y-8*yu),(4*yu,4*yu),'Viw',
            ['Origin','Oxy','Oxz','Oyz','Fit','Center'])
        self.btn_prj=esui.BorderlessMenuBtn(self,(0,self.Size.y-4*yu),(4*yu,4*yu),'Prj',
            ['Orth','Prep'])

        self.btn_slct.Bind(wx.EVT_LEFT_DOWN,self.onClkSlct)
        self.btn_slct.Bind(wx.EVT_LEFT_DCLICK,self.onDClkSlct)
        # self.mov_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMoveBtn)
        self.btn_del.Bind(wx.EVT_LEFT_DOWN,self.onClkDel)
        self.btn_viw.PopupControl.lctrl.Bind(wx.EVT_LEFT_DCLICK,self.onDClkViewPopup)
        self.btn_viw.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkViewPopup)
        self.btn_prj.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkProjPopup)

        self.host.Bind(wx.EVT_MOUSEWHEEL,self.onRoWhlGL)
        self.host.Bind(wx.EVT_LEFT_DOWN,self.onClkGL)
        self.host.Bind(wx.EVT_LEFT_DCLICK, self.onDClkGL)
        self.host.Bind(wx.EVT_LEFT_UP, self.onRlsGL)
        self.host.Bind(wx.EVT_MOTION,self.onMoveGL)
        self.host.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhlGL)
        return

    def onClkGL(self,e):
        self.host.SetFocus()
        cpos=e.GetPosition()
        cx,cy=esgl.normPos(cpos)
        self.spos=cpos
        if self.state_select[0]=='Pick':
            if e.controlDown:   # Multi-selecting with ctrl;
                'todo'
            else:
                esgl.ARO_SELECTION=list()
                esgl.selectADP(cpos[0],cpos[1])
                if len(esgl.ARO_SELECTION)==1:
                    esgl.highlight()
                elif len(esgl.ARO_SELECTION)!=0:
                    ClkPopupPlc(self.host,cpos,esgl.ARO_SELECTION)
        else:pass
        esgl.drawGL()
        return

    def onClkWhlGL(self,e):
        self.spos=e.GetPosition()
        e.Skip()
        return

    def onRoWhlGL(self,e):
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

    def onDClkGL(self,e):
        if len(esgl.ARO_SELECTION)==1:
            esui.SIDE_PLC.showDetail(esgl.ARO_SELECTION[0].AroID)
        return

    def onRlsGL(self,e):
        if self.state_select[0]=='Rect':
            esgl.ARO_SELECTION=[]
            cpos=e.GetPosition()
            cx,cy=esgl.normPos(cpos)
            sx,sy=esgl.normPos(self.spos)
            for adp in esgl.DICT_ADP.getAllAdp():
                if not hasattr(adp.Aro,'position'):continue
                slct=False
                for p in adp.VA:
                    p_2d=esgl.getPosFromVertex(adp,p)
                    c1=p_2d[0] in interval.Interval(cx,sx)
                    c2=p_2d[1] in interval.Interval(cy,sy)
                    if c1 and c2:
                        esgl.ARO_SELECTION.append(adp.Aro)
                        adp.highlight=True
                        slct=True
                        break
                if not slct:adp.highlight=False
            self.spos=cpos
            esgl.drawGL()
        return

    def onMoveGL(self,e):
        cpos=e.GetPosition()
        spos=self.spos
        if e.leftIsDown and self.state_select[0]=='Rect':
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
            self.spos=cpos
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

    def onClkSlct(self,e):
        if self.state_select[0]=='None':
            self.state_select[0]=self.state_select[1]
        else:
            self.state_select[0]='None'

        # if self.selecting:
        #     self.selecting=False
        # else:
        #     self.selecting=True
        e.Skip()
        return

    def onDClkSlct(self,e):
        if self.show_tab:return
        else:self.show_tab=True
        self.tab=esui.SIDE_PLC.getTab('Options')
        tx=self.tab.Size.x
        esui.StaticText(self.tab,(yu,yu),(12*yu,4*yu),'Selecting Options:',align='left')
        btn_con=esui.Btn(self.tab,(tx-5*yu,yu),(4*yu,4*yu),'√')
        ops=['Pick','Rect','Picktop']
        menu_option=esui.SelectMenuBtn(
            self.tab,(yu,6*yu),(tx-2*yu,4*yu),self.state_select[1],ops)

        def onClkSlctCon(e):
            self.show_tab=False
            self.state_select=[ops[int(menu_option.Value)]]*2
            self.btn_slct.SetValue(True)
            esui.SIDE_PLC.hideTab('Options',clear=True)

        btn_con.Bind(wx.EVT_LEFT_DOWN,onClkSlctCon)
        self.tab.Show()
        return

    def onClkMove(self,e):
        if esui.ARO_PLC.moving:
            esui.ARO_PLC.moving=False
        else:
            esui.ARO_PLC.moving=True
        e.Skip()
        return

    def onClkDel(self,e):
        for aro in esgl.ARO_SELECTION:
            ESC.delAro(aro.AroID)
        esgl.ARO_SELECTION=list()
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        e.Skip()
        return

    def onClkViewPopup(self,e):
        ppc=self.btn_viw.PopupControl
        if ppc.ipos==0:     # origin;
            esgl.EP=np.array([5,5,5])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            esgl.WHEEL_DIS=0
        elif ppc.ipos==1:   # Oxy;
            esgl.EP=np.array([0,0,5])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            esgl.WHEEL_DIS=0
        elif ppc.ipos==2:   # Oxz;
            esgl.EP=np.array([0,-5,0])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,0,1])
            esgl.WHEEL_DIS=0
        elif ppc.ipos==3:   # Oyz;
            esgl.EP=np.array([-5,0,0])
            esgl.AP=np.array([0,0,0])
            esgl.UP=np.array([0,1,0])
            esgl.WHEEL_DIS=0
        elif ppc.ipos==4:   # Fit;
            pass
        elif ppc.ipos==5:   # Center;
            pass
        elif ppc.ipos==6:     # Grid;
            pass
        esgl.lookAt()
        e.Skip()
        return

    def onDClkViewPopup(self,e):
        ppc=self.btn_viw.PopupControl
        if ppc.ipos==1:     # Oxy;
            esgl.EP=np.array([0,0,-5])
            esgl.UP=np.array([0,1,0])
        elif ppc.ipos==2:   # Oxz;
            esgl.EP=np.array([0,5,0])
            esgl.UP=np.array([0,0,1])
        elif ppc.ipos==3:   # Oyz;
            esgl.EP=np.array([5,0,0])
            esgl.UP=np.array([0,1,0])
        else: return
        esgl.AP=np.array([0,0,0])
        esgl.WHEEL_DIS=0
        esgl.lookAt()
        e.Skip()
        return

    def onClkProjPopup(self,e):
        ppc=self.btn_prj.PopupControl
        if ppc.ipos==0:esgl.projMode(False)
        elif ppc.ipos==1:esgl.projMode(False)
        esgl.lookAt()
        e.Skip()
        return
    pass

class ClkPopupPlc(esui.PopupPlc):
    def __init__(self,parent,p,items):
        super().__init__(parent,p,(10*yu,10*yu))
        self.items=items
        self.SetSize(10*yu,(len(items)*4+1)*yu)
        for i in range(0,len(self.items)):
            self.ItemText(self,(yu,(4*i+.5)*yu),(self.Size.x-2*yu,4*yu-2),self.items[i])
        return

    class ItemText(esui.StaticText):
        def __init__(self,parent,p,s,item):
            super().__init__(parent,p,s,item.AroName,align='left')
            self.item=item
            self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
            self.Bind(wx.EVT_MOTION,self.onMove)
            self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
            return

        def onClk(self,e):
            e.Skip()
            esgl.highlight(self.item)
            self.Parent.DestroyLater()
            return

        def onMove(self,e):
            e.Skip()
            dc=wx.ClientDC(self)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawLine(0,self.Size.y-1,self.Parent.Size.x-yu,self.Size.y-1)
            esgl.highlight(self.item)
            return

        def onLeave(self,e):
            self.Refresh(eraseBackground=False)
            return
        pass
    pass
