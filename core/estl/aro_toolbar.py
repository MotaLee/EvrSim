import wx
import _glm as glm
import numpy as np
from core import ESC,esui,esgl
GLC=esgl.glc
yu=esui.YU
class AroToolbar(esui.Div):
    def __init__(self):
        super().__init__(esui.UMR.MAP_DIV,style={
                'p':(0,0),'bgc':esui.COLOR_LBACK,
                's':(4*yu,GLC.GLDIV_HEIGHT)})
        self.host=esui.UMR.MAP_DIV
        self.spos=(0,0)
        # self.queue_select=['None','Pick']    # enum with [None, Pick, Rect, Picktop]
        self.enum_slt=ESC.EsEnum(['deact','pick','rect','picktop'],prev='pick')
        self.flag_tab_shown=False

        self.head=esui.DivBtn(self,label='Aro',style={'p':(0,0),'s':(4*yu,2*yu)})
        self.btn_slct=esui.TglBtn(self,label='Slt',
            style={'p':(0,2*yu),'s':(4*yu,4*yu),'border':'','bgc':''})
        self.btn_del=esui.DivBtn(self,label='Del',
            style={'p':(0,10*yu),'s':(4*yu,4*yu),'border':'','bgc':''})
        self.btn_mov=esui.TglBtn(self,label='Mov',
            style={'p':(0,6*yu),'s':(4*yu,4*yu),'border':'','bgc':''})

        self.btn_viw=esui.MenuBtnDiv(self,label='Viw',no_border=True,
            style={'p':(0,self.Size.y-8*yu),'s':(4*yu,4*yu)},
            items=['Origin','Oxy','Oxz','Oyz','Fit','Center'])
        self.btn_prj=esui.MenuBtnDiv(self,label='Prj',no_border=True,
            style={'p':(0,self.Size.y-4*yu),'s':(4*yu,4*yu)},
            items=['Orth','Prep'])

        self.btn_slct.Bind(esui.EBIND_LEFT_CLK,self.onClkSlct)
        self.btn_slct.Bind(esui.EBIND_LEFT_DCLK,self.onDClkSlct)
        # self.mov_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMoveBtn)
        self.btn_del.Bind(esui.EBIND_LEFT_CLK,self.onClkDel)
        self.btn_viw.bindPopup(esui.EBIND_LEFT_DCLK,self.onDClkViewPopup)
        self.btn_viw.bindPopup(esui.EBIND_LEFT_CLK,self.onClkViewPopup)
        self.btn_prj.bindPopup(esui.EBIND_LEFT_CLK,self.onClkProjPopup)

        self.host.Bind(wx.EVT_MOUSEWHEEL,self.onRoWhlGL)
        self.host.Bind(esui.EBIND_LEFT_CLK,self.onClkGL)
        self.host.Bind(esui.EBIND_LEFT_DCLK, self.onDClkGL)
        self.host.Bind(wx.EVT_LEFT_UP, self.onRlsGL)
        self.host.Bind(wx.EVT_MOTION,self.onMoveGL)
        self.host.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhlGL)
        return

    def onClkGL(self,e):
        e.Skip()
        cpos=e.GetPosition()
        self.spos=cpos
        if self.enum_slt.val('pick'):
            if e.controlDown:   # Multi-selecting with ctrl;
                'todo'
            else:
                GLC.clearSelection()
                selection=GLC.selectAdp(cpos[0],cpos[1])
                if len(selection)<=1:GLC.highlightAdp()
                else:SelectPopup(self.host,cpos,selection)
        else:pass
        GLC.drawGL()
        return

    def onClkWhlGL(self,e):
        e.Skip()
        self.spos=e.GetPosition()
        return

    def onRoWhlGL(self,e):
        t=np.sign(e.WheelRotation)
        if GLC.WHEEL_DIS==-10 and t>0:return
        if GLC.WHEEL_DIS==15 and t<0:return
        cpos=e.GetPosition()
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
        GLC.lookAt()
        e.Skip()
        return

    def onDClkGL(self,e):
        selection=GLC.getSelection()
        if len(selection)==1:
            esui.UMR.SIDE_DIV.showDetail(selection[0].AroID)
        return

    def onRlsGL(self,e):
        if self.enum_slt.val('rect'):
            GLC.clearSelection()
            cpos=e.GetPosition()
            cx,cy=GLC.cvtPosToCoord(cpos)
            sx,sy=GLC.cvtPosToCoord(self.spos)
            for adp in GLC.getAllAdp():
                if not hasattr(adp.Aro,'position'):continue
                slct=False
                for p in adp.VA:
                    p_2d=GLC.getPosFromVtx(adp,p)
                    c1=p_2d[0] in ESC.Itv(cx,sx)
                    c2=p_2d[1] in ESC.Itv(cy,sy)
                    if c1 and c2:
                        GLC.ARO_SELECTION.append(adp.Aro)
                        adp.highlight=True
                        slct=True
                        break
                if not slct:adp.highlight=False
            self.spos=cpos
            GLC.drawGL()
        return

    def onMoveGL(self,e):
        cpos=e.GetPosition()
        spos=self.spos
        if e.leftIsDown and self.enum_slt.val('rect'):
            GLC.drawGL()
            dc=wx.ClientDC(self.host)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawRectangle(spos[0],spos[1],
                cpos[0]-spos[0],cpos[1]-spos[1])
        elif e.middleIsDown:
            GLC.UP=[0,1,0]
            dx=(cpos.x-spos.x)/self.Size.y*glm.pi()
            dy=(spos.y-cpos.y)/self.Size.y*glm.pi()
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
            GLC.lookAt()
        e.Skip()
        return

    def onClkSlct(self,e):
        e.Skip()
        if self.enum_slt.val('deact'):
            self.enum_slt.rollback()
        else:
            self.enum_slt.set('deact')
        return

    def onDClkSlct(self,e):
        if self.flag_tab_shown:return
        else:self.flag_tab_shown=True
        self.tab=esui.UMR.SIDE_DIV.getTab('Options')
        tx=self.tab.Size.x
        esui.StaticText(self.tab,(yu,yu),(12*yu,4*yu),'Selecting Options:',align='left')
        btn_con=esui.Btn(self.tab,(tx-5*yu,yu),(4*yu,4*yu),'√')
        ops=['pick','rect','picktop']
        menu_option=esui.MenuBtnDiv(self.tab,items=ops,select=True,
            label=self.enum_slt.getPrev(),style={'p':(yu,6*yu),'s':(tx-2*yu,4*yu)})

        def onClkSlctCon(e):
            self.flag_tab_shown=False
            self.enum_slt.set(ops[int(menu_option.Value)])
            self.btn_slct.SetValue(True)
            esui.UMR.SIDE_DIV.delTab('Options')

        btn_con.Bind(wx.EVT_LEFT_DOWN,onClkSlctCon)
        self.tab.Show()
        return

    def onClkDel(self,e):
        selection=GLC.getSelection()
        for aro in selection:ESC.delAro(aro.AroID)
        GLC.clearSelection()
        esui.sendComEvt(esui.ETYPE_UPDATE_MAP)
        e.Skip()
        return

    def onClkViewPopup(self,e):
        e.Skip()
        pi=e.EventObject.popup_index
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

    def onDClkViewPopup(self,e):
        pi=e.EventObject.popup_index
        if pi==1:     # Oxy;
            GLC.lookAt([0,0,-5],[0,0,0],[0,1,0])
        elif pi==2:   # Oxz;
            GLC.lookAt([0,5,0],[0,0,0],[0,1,0])
        elif pi==3:   # Oyz;
            GLC.lookAt([5,0,0],[0,0,0],[0,1,0])
        else: return
        GLC.WHEEL_DIS=0
        e.Skip()
        return

    def onClkProjPopup(self,e):
        pi=e.EventObject.popup_index
        if pi==0:GLC.setProjMode(False)
        elif pi==1:GLC.setProjMode(False)
        GLC.lookAt()
        e.Skip()
        return
    pass

class SelectPopup(esui.IndePopupDiv):
    def __init__(self,parent,cpos,items):
        super().__init__(parent,style={'p':(0,0),'s':(10*yu,len(items)*4*yu)})
        self.items=items
        for i in range(0,len(self.items)):
            item=esui.Div(self,label=self.items[i].AroName,
                style={'p':(yu,4*i*yu+1),'s':(self.Size.x-2*yu,3*yu)})
        self.bindPopup(wx.EVT_MOTION,self.onMoveItem)
        self.bindPopup(wx.EVT_LEFT_DOWN,self.onClkItem)
        self.Position((self.parent.Position.x+cpos[0],self.parent.Position.y+cpos[1]),(0,0))
        self.Show()
        return

    def onClkItem(self,e):
        e.Skip()
        self.DestroyLater()
        return

    def onMoveItem(self,e):
        e.Skip()
        GLC.highlightAdp(ESC.getAro(e.EventObject.label))
        return
    pass
