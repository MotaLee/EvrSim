from core.esqt import qt,qg,qc
from core.esqt import Box,Btn,BtnMenu
from core.esqt import YU,ESQTAPP

# import _glm as glm
import numpy as np
from core import esc,esgl,esqt
ESC=esc.ESC
GLC=esgl.GLC
glm=esgl.glm
class GLToolbar(Box):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.host:esqt.GLBox=ESQTAPP.MAP_DIV
        self.spos=(0,0)
        self.enum_slt=esc.EsEnum(['deact','pick','rect','picktop'],prev='pick')
        # self.queue_select=['None','Pick']    # enum with [None, Pick, Rect, Picktop]
        self.flag_tab_shown=False
        self.flag_middle=False

        self.header=Btn(self,text='Aro',size=(0,2*YU))
        self.btn_slct=Btn(self,text='Slt',size=(4*YU,4*YU),border=False,toggle=True)
        self.btn_del=Btn(self,text='Del',size=(4*YU,4*YU),border=False)

        self.btn_viw=BtnMenu(self,text='Viw',border=False,size=(4*YU,4*YU),
            item=['Origin','Oxy','Oxz','Oyz','Fit','Center'],pos_popup=9)
        self.btn_prj=BtnMenu(self,text='Prj',border=False,size=(4*YU,4*YU),
            item=['Orth','Prep'],pos_popup=9)

        self.btn_slct.clicked.connect(self.onClkSlct)
        # self.btn_slct.clicked.connect(self.onDClkSlct)
        self.btn_del.clicked.connect(self.onClkDel)
        # self.btn_viw.bindPopup(self.onDClkViewPopup)
        self.btn_viw.bindPopup(self.onClkViewPopup)
        self.btn_prj.bindPopup(self.onClkProjPopup)

        self.host.mousePressEvent=self.onClkGL
        self.host.wheelEvent=self.onWheelGL
        self.host.mouseMoveEvent=self.onMoveGL
        self.host.mouseReleaseEvent=self.onReleaseGL

        vbox=qt.QVBoxLayout(self)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)
        vbox.addWidget(self.header)
        vbox.addWidget(self.btn_slct)
        vbox.addWidget(self.btn_del)
        vbox.addStretch(0)
        vbox.addWidget(self.btn_viw)
        vbox.addWidget(self.btn_prj)
        return

    def onClkGL(self,e:qg.QMouseEvent):
        cpos=(e.x(),e.y())
        self.spos=cpos
        if e.button()==qc.Qt.MiddleButton:
            self.flag_middle=True
            return
        if self.enum_slt.val('pick'):

            if e.modifiers()==qc.Qt.ControlModifier:   # Multi-selecting with ctrl;
                'todo'
            else:
                self.host.makeCurrent()
                GLC.clearSelection()
                selection=GLC.selectAdp(cpos[0],cpos[1])
                if len(selection)<=1:GLC.highlightAdp()
                # else:SelectPopup(self.host,cpos,selection)
        else:
            pass
        self.host.update()
        return

    def onWheelGL(self, e:qg.QWheelEvent) -> None:
        t=np.sign(e.angleDelta().y())
        if GLC.WHEEL_DIS==-10 and t>0:return
        if GLC.WHEEL_DIS==15 and t<0:return
        cpos=(e.position().x(),e.position().y())
        cx,cy=GLC.cvtPosToCoord(cpos)

        ep=np.array(GLC.EP)
        ap=np.array(GLC.AP)
        v_ae=ep-ap
        z1=(v_ae)/np.linalg.norm(v_ae)    # ev_ae;
        x1=np.cross(np.array(GLC.UP),z1)
        x1=x1/np.linalg.norm(x1)
        y1=np.cross(z1,x1)
        y1=y1/np.linalg.norm(y1)
        v_ac=0.414/GLC.SPEED_ZOOM*np.array([cx*GLC.RATIO_WH,cy,0])
        v_ac=v_ac[0]*x1+v_ac[1]*y1
        GLC.AP=(ap+t*v_ac-t/GLC.SPEED_ZOOM*z1).tolist()
        GLC.EP=(ep+t*v_ac-t/GLC.SPEED_ZOOM*z1).tolist()
        GLC.WHEEL_DIS-=t
        # GLC.setProjMode()
        self.host.makeCurrent()
        GLC.lookAt()
        return

    def onMoveGL(self, e: qg.QMouseEvent) -> None:
        cpos=(e.x(),e.y())
        spos=self.spos
        b=e.buttons()
        if e.modifiers()==qc.Qt.ControlModifier and self.enum_slt.val('rect'):
            self.update()
            # dc=wx.ClientDC(self.host)
            # dc.SetBrush(wx.TRANSPARENT_BRUSH)
            # dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            # dc.DrawRectangle(spos[0],spos[1],
            #     cpos[0]-spos[0],cpos[1]-spos[1])
        elif self.flag_middle:
            GLC.UP=[0,1,0]
            dx=(cpos[0]-spos[0])/self.h*glm.pi()
            dy=(spos[1]-cpos[1])/self.h*glm.pi()
            self.spos=cpos
            ep=np.array(GLC.EP)
            ap=np.array(GLC.AP)
            v_ae=ep-ap
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
            GLC.EP=(v_ae+ap).tolist()
            self.host.makeCurrent()
            GLC.lookAt()
            return

    def onReleaseGL(self, e:qg.QMouseEvent) -> None:
        self.flag_middle=False
        if self.enum_slt.val('rect'):
            GLC.clearSelection()
            cpos=(e.x(),e.y())
            cx,cy=GLC.cvtPosToCoord(cpos)
            sx,sy=GLC.cvtPosToCoord(self.spos)
            for adp in GLC.getAllAdp():
                if not hasattr(adp.Aro,'position'):continue
                slct=False
                for p in adp.VA:
                    p_2d=GLC.getPosFromVtx(adp,p)
                    c1=p_2d[0] in esc.Itv(cx,sx)
                    c2=p_2d[1] in esc.Itv(cy,sy)
                    if c1 and c2:
                        GLC.ARO_SELECTION.append(adp.Aro)
                        adp.highlight=True
                        slct=True
                        break
                if not slct:adp.highlight=False
            self.spos=cpos
            GLC.drawGL()
        return

    def onDClkGL(self):
        selection=GLC.getSelection()
        if len(selection)==1:
            esui.UMR.SIDE_DIV.showDetail(selection[0])
        return

    def onClkSlct(self):
        if self.enum_slt.val('deact'):
            self.enum_slt.rollback()
        else:
            self.enum_slt.set('deact')
        return

    def onDClkSlct(self):
        if self.flag_tab_shown:return
        else:self.flag_tab_shown=True
        self.tab=esui.UMR.SIDE_DIV.getTab('Options')
        tx=self.tab.Size.x
        esui.StaticText(self.tab,(YU,YU),(12*YU,4*YU),'Selecting Options:',align='left')
        btn_con=esui.Btn(self.tab,(tx-5*YU,YU),(4*YU,4*YU),'√')
        ops=['pick','rect','picktop']
        menu_option=esui.MenuBtnDiv(self.tab,items=ops,select=True,
            label=self.enum_slt.getPrev(),style={'p':(YU,6*YU),'s':(tx-2*YU,4*YU)})

        def onClkSlctCon(e):
            self.flag_tab_shown=False
            self.enum_slt.set(ops[int(menu_option.Value)])
            self.btn_slct.SetValue(True)
            esui.UMR.SIDE_DIV.delTab('Options')

        btn_con.Bind(wx.EVT_LEFT_DOWN,onClkSlctCon)
        self.tab.Show()
        return

    def onClkDel(self):
        selection=GLC.getSelection()
        for aro in selection:ESC.delAro(aro.AroID)
        GLC.clearSelection()
        ESQTAPP.emitSignal(esqt.SIG_UPDATE_MAP)
        return

    def onClkViewPopup(self):
        if pi==0:     # origin;
            GLC.lookAt([5,5,5],[0,0,0],[0,1,0])
            GLC.WHEEL_DIS=0
        elif pi==1:   # Oxy;
            GLC.lookAt([0,0,5],[0,0,0],[0,1,0])
            GLC.WHEEL_DIS=0
        elif pi==2:   # Oxz;
            GLC.lookAt([0,-5,0],[0,0,0],[0,1,0])
            GLC.WHEEL_DIS=0
        elif pi==3:   # Oyz;
            GLC.lookAt([-5,0,0],[0,0,0],[0,1,0])
            GLC.WHEEL_DIS=0
        elif pi==4:   # Fit;
            pass
        elif pi==5:   # Center;
            pass
        elif pi==6:     # Grid;
            pass
        return

    def onDClkViewPopup(self,action:qg.QAction):
        pi=action.text()
        self.host.makeCurrent()
        if pi=='Oxy':     # Oxy;
            GLC.lookAt([0,0,-5],[0,0,0],[0,1,0])
        elif pi=='Oxz':   # Oxz;
            GLC.lookAt([0,5,0],[0,0,0],[0,1,0])
        elif pi=='Oyz':   # Oyz;
            GLC.lookAt([5,0,0],[0,0,0],[0,1,0])
        else: return
        GLC.WHEEL_DIS=0
        return

    def onClkProjPopup(self,action:qg.QAction):
        pi=action.text()
        self.host.makeCurrent()
        if pi==0:GLC.setProjMode(True)
        elif pi==1:GLC.setProjMode(False)
        GLC.lookAt()
        return
    pass

# class SelectPopup(esui.IndePopupDiv):
#     def __init__(self,parent,cpos,items):
#         super().__init__(parent,style={'p':(0,0),'s':(10*YU,len(items)*4*YU)})
#         self.items=items
#         for i in range(0,len(self.items)):
#             item=esui.Div(self,label=self.items[i].AroName,
#                 style={'p':(YU,4*i*YU+1),'s':(self.Size.x-2*YU,3*YU)})
#         self.bindPopup(wx.EVT_MOTION,self.onMoveItem)
#         self.bindPopup(wx.EVT_LEFT_DOWN,self.onClkItem)
#         self.setPopupPos(cpos)
#         self.Show()
#         return

#     def onClkItem(self,e):
#         e.Skip()
#         self.DestroyLater()
#         return

#     def onMoveItem(self,e):
#         e.Skip()
#         GLC.highlightAdp(ESC.getAro(e.EventObject.label))
#         return
#     pass
