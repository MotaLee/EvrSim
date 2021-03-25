# Acp panel relavant;
import copy,wx
import numpy as np
from interval import Interval as Itv
from core import ESC,esui
from .detail import DetailDialog
yu=esui.YU
xu=esui.XU

class MdlDiv(esui.Div):
    def __init__(self, parent: wx.Window, **argkw):
        super().__init__(parent, **argkw)
        self.mdl=tuple()
        self.canvas=AcpCanvas(self,(4*yu,2*yu),(self.Size[0]-4*yu,self.Size[1]-2*yu))
        self.toolpl=AcpToolbar(self,style={'p':(0,0),'s':(4*yu,self.Size[1]),'bgc':esui.COLOR_LBACK})
        self.stc_left=esui.StaticText(self,(4*yu,0),(12*yu,2*yu),'',tsize=8,align='left')
        self.stc_right=esui.StaticText(self,(self.Size[0]-16*yu,0),(12*yu,2*yu),'',tsize=8,align='right')
        CP=self.canvas
        self.selection=CP.list_active
        self.drawConnection=CP.drawLink
        self.addAcpNode=CP.addAcpNode
        self.onKeyDown=CP.onKeyDown

        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.Hide()
        return

    def onComEvt(self,e):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_KEY_DOWN:
            if self.IsShown():self.onKeyDown(e.getEventArgs('eobj'))
        elif etype==esui.ETYPE_OPEN_SIM:
            self.Hide()
        return

    def drawMdl(self,mdl=None,refresh=False):
        ''' Draw model.
            * Para mdl: model tuple. None default for drawing current model;
            * Para refresh:if redraw. False default. Be True when mdl isnt None;'''
        if mdl is not None:
            self.mdl=mdl
            refresh=True
        self.canvas.drawMdl(self.mdl,refresh)
        self.stc_left.SetLabel('Model: '+str(self.mdl))
        self.stc_right.SetLabel('Count: '+str(len(ESC.ACP_MODELS[self.mdl])))
        return
    pass

class AcpCanvas(wx.ScrolledCanvas):
    def __init__(self,parent:MdlDiv,p,s):
        super().__init__(parent,pos=p,size=s)
        self.Parent:MdlDiv
        self.rx=0
        self.ry=0
        self.zoom_rate=1
        self.spos=[0,0]
        self.snap=100*self.zoom_rate

        # A4 size: 297x210mm, 120dpi,
        self.canvas_width=self.zoom_rate+2100
        self.canvas_height=self.zoom_rate+1500

        self.acp_adding=''  # AcpClass name;
        self.acp_pasting=list()
        self.list_clip=list()
        self.list_active=list()

        self.flag_moving=False
        self.flag_attaching=False
        # self.rect_selecting=False

        self.start_evtobj=self
        self.first_id=None
        self.first_port=None
        self.bitmap_bg=wx.Bitmap(self.canvas_width,self.canvas_height)

        self.SetBackgroundColour(esui.COLOR_BACK)
        self.SetVirtualSize(self.canvas_width,self.canvas_height)
        self.SetScrollRate(1,1)
        self.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_NEVER)

        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_UP,self.onRls)
        self.Bind(wx.EVT_MOTION,self.onMove)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onZoom)
        self.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhl)
        self.Bind(wx.EVT_MIDDLE_UP,self.onRlsWhl)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        return

    def drawMdl(self,mdl=None,refresh=False):
        if mdl is None:mdl=self.Parent.mdl
        if refresh:
            self.DestroyChildren()
            self.Scroll(0,0)
            self.rx=0
            self.ry=0
        self.list_active.clear()
        if mdl not in ESC.ACP_MODELS:return

        'todo: not redraw'
        self.DestroyChildren()
        for acp in ESC.ACP_MODELS[mdl]:
            AcpNode(self,acp)

        for acpnode in self.Children:
            acpnode.Refresh()

        self.Show()
        self.drawLink()
        return

    def drawLink(self):
        lines=list()
        snap=self.snap
        offx=-1*self.rx
        offy=-1*self.ry

        xdc=wx.ClientDC(self)
        dc=wx.BufferedDC(xdc,buffer=self.bitmap_bg)
        dc.Clear()
        dc.SetPen(wx.Pen(esui.COLOR_HOVER))
        for i in range(1,int(self.canvas_width/snap)):
            lines.append([snap*i+offx,offy,snap*i+offx,self.canvas_width*self.zoom_rate+offy])
            lines.append([offx,snap*i+offy,self.canvas_width*self.zoom_rate+offx,snap*i+offy])
        dc.DrawLineList(lines)

        dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=3))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(100*self.zoom_rate+offx,
            100*self.zoom_rate+offy,
            2100*self.zoom_rate,
            1500*self.zoom_rate)
        lines=list()
        io_points=list()
        for node in self.Children:
            node:AcpNode
            inport=node.acp.getPort(io='in')
            if len(inport)==0:continue
            for port in inport:
                # Input lines, inport->tar outport;
                if len(port.link)==0:continue
                for ctrl in node.Children:
                    # Inport position;
                    portid=getattr(ctrl,'portid',-1)
                    if port.pid==portid:
                        nx=ctrl.Position[0]
                        ny=ctrl.Position[1]
                        break
                ox=node.Position[0]+nx+2.5*yu*self.zoom_rate
                oy=node.Position[1]+ny+yu*self.zoom_rate

                tarid=port.link[0][0]
                tarpid=port.link[0][1]
                tarnode=self.getAcpNode(tarid)
                for ctrl in tarnode.Children:
                    portid=getattr(ctrl,'portid',-1)
                    if portid==tarpid:
                        tny=ctrl.Position[1]
                        break
                tx=tarnode.Position[0]
                ty=tarnode.Position[1]+tny+yu*self.zoom_rate
                io_points.append((ox,oy,tx,ty))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=1))
        for p in io_points:
            if p[0]>p[2]:cx=p[0]+100
            else:cx=(p[0]+p[2])/2
            cy=(p[1]+p[3])/2
            dc.DrawSpline([
                (p[0],      p[1]),
                (p[0]+4*yu, p[1]),
                (cx,        cy),
                (p[2]-4*yu, p[3]),
                (p[2],      p[3])])
            dc.DrawPolygon([
                (p[0],p[1]),
                (p[0]+yu,p[1]+0.5*yu),
                (p[0]+yu,p[1]-0.5*yu)])
            dc.DrawPolygon([
                (p[2]-yu,p[3]),
                (p[2],p[3]+0.5*yu),
                (p[2],p[3]-0.5*yu)])

        return

    def getAcpNode(self,acp):
        ''' Get Acpnode.
            * Para acp: Accept int/Acp;'''
        if isinstance(acp,int):acp=ESC.getAcp(acp,self.Parent.mdl)
        for node in self.Children:
            if isinstance(node,AcpNode) and node.acp==acp:return node
        return

    def addAcpNode(self,acpclass):
        self.spos=(0,0)
        self.acp_adding=acpclass
        return

    def rmAcpNodes(self):
        ''' Return Acps list of removed AcpNodes;'''
        rm_acp=ESC.clipAcps(self.list_active,self.Parent.mdl)
        for node in self.list_active:
            node.Destroy()
        esui.UMR.SIDE_DIV.clearDetail()
        self.Parent.drawMdl()
        return rm_acp

    def onKeyDown(self,e,operation=''):
        if e is not None:key=e.GetKeyCode()
        else:key=operation
        if (key==ord('C') and e.controlDown) or key=='Copy':
            self.list_clip=[copy.deepcopy(node.acp)
                for node in self.list_active]
        elif (key==ord('X') and e.controlDown) or key=='Cut':
            self.list_clip=self.rmAcpNodes()
        elif (key==ord('V') and e.controlDown) or key=='Paste':
            if len(self.list_clip)!=0:
                self.acp_pasting=self.list_clip
        return

    def onClk(self,e):

        self.start_evtobj=self
        mdl=esui.UMR.MDL_DIV.mdl
        self.spos=e.GetPosition()
        if self.acp_adding:
            acp=ESC.addAcp(self.acp_adding,mdl)
            ESC.setAcp(acp,mdl,acpo={
                'acp_name':'Acp_'+str(acp.getAcpo('acpid')),
                'position':[
                    self.spos[0]/self.zoom_rate+self.rx,
                    self.spos[1]/self.zoom_rate+self.ry]})
            self.acp_adding=''
            self.drawMdl()
        elif len(self.acp_pasting)!=0:
            'deco'
            p_f=[5000,5000]
            for acp in self.acp_pasting:
                p_f[0]=min(p_f[0],acp.position[0])
                p_f[1]=min(p_f[1],acp.position[1])

            acpid_table=dict()
            for acp in self.acp_pasting:
                acpid=acp.getAcpo('acpid')
                new_acp=ESC.addAcp(acp.getAcpo('AcpClass'),mdl)
                acpid_table[acpid]=new_acp.getAcpo('acpid')
                acp.AcpID=new_acp.AcpID
                p_t=acp.position
                acpx=self.spos[0]+self.rx+p_t[0]-p_f[0]
                acpy=self.spos[1]+self.ry+p_t[1]-p_f[1]
                acp.position=[acpx,acpy]

            for acp in self.acp_pasting:
                for ip,ip_tar in acp.inport.items():
                    if ip_tar is None:continue
                    if ip_tar[0] not in acpid_table:acp.inport[ip]=None
                    else:acp.inport[ip]=(acpid_table[ip_tar[0]],ip_tar[1])
                for op,op_tar_list in acp.outport.items():
                    tmp_list=list(op_tar_list)
                    for op_tar in op_tar_list:
                        tmp_list.remove(op_tar)
                        if op_tar[0] in acpid_table:
                            tmp_list.append((acpid_table[op_tar[0]],op_tar[1]))
                    acp.outport[op]=tmp_list
                ESC.setAcp(acp.AcpID,acp.__dict__,mdl)
            self.acp_pasting.clear()
            self.drawMdl()
        else:   # Empty click;
            self.list_active.clear()
            for node in self.Children:
                node.flag_active=False
                node.Refresh()
        return

    def onRls(self,e):
        eo=e.EventObject
        if eo==self:cpos=e.GetPosition()
        else:
            ep=e.GetPosition()
            cpos=(eo.Position[0]+ep[0],eo.Position[1]+ep[1])
        # Rect selecting;
        for node in self.Children:
            cx=node.Position[0] in Itv(cpos[0],self.spos[0])
            cy=node.Position[1] in Itv(cpos[1],self.spos[1])
            if cx and cy:
                self.list_active.append(node)
                node.flag_active=True
            elif node.flag_active:
                node.flag_active=False
            node.Refresh()
        self.drawLink()
        return

    def onMove(self,e):
        eo=e.EventObject
        if eo==self:cpos=e.GetPosition()
        else:
            ep=e.GetPosition()
            cpos=(eo.Position[0]+ep[0],eo.Position[1]+ep[1])
        dx=(cpos[0]-self.spos[0])
        dy=(cpos[1]-self.spos[1])
        if self.acp_adding!='' or len(self.acp_pasting)!=0:
            self.drawLink()
            dc=wx.ClientDC(self)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawRectangle(cpos[0],cpos[1],100,100)
            if len(self.acp_pasting)!=0:
                dc.DrawRectangle(cpos[0]+50,cpos[1]+50,100,100)
        elif e.middleIsDown:  # View panning;
            self.spos=cpos
            self.rx-=dx
            self.ry-=dy
            endx=self.canvas_width-self.Size.x/self.zoom_rate
            endy=self.canvas_height-self.Size.y/self.zoom_rate
            if endx<0:endx=0
            if endy<0:endy=0
            if self.rx<0:self.rx=0
            elif self.rx>endx:self.rx=endx
            if self.ry<0:self.ry=0
            elif self.ry>endy:self.ry=endy
            self.Scroll(self.rx,self.ry)
            self.drawLink()
        elif e.leftIsDown:  # Rect selecting;
            self.drawLink()
            dc=wx.ClientDC(self)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawRectangle(self.spos[0],self.spos[1],
                cpos[0]-self.spos[0],cpos[1]-self.spos[1])
        return

    def onZoom(self,e):
        ZS=1    # Zoom speed;
        t=np.sign(e.WheelRotation)
        if self.zoom_rate<0.5 and t<0:return
        if self.zoom_rate>1.5 and t>0:return
        self.zoom_rate+=t/10*ZS
        self.snap=100*self.zoom_rate
        self.drawMdl()
        self.SetVirtualSize(self.canvas_width*self.zoom_rate,self.canvas_width*self.zoom_rate)
        return

    def onClkWhl(self,e):
        eo=e.EventObject
        if eo==self:cpos=e.GetPosition()
        else:
            ep=e.GetPosition()
            cpos=(eo.Position[0]+ep[0],eo.Position[1]+ep[1])
        self.spos=cpos
        e.Skip()
        return

    def onRlsWhl(self,e):
        self.drawLink()
        return
    pass

class AcpNode(esui.Div):
    def __init__(self,parent:AcpCanvas,acp:ESC.Acp):
        self.zr=parent.zoom_rate
        self.yu=yu*self.zr
        self.Parent:AcpCanvas
        zyu=self.yu
        inport=acp.getPort(io='in')
        outport=acp.getPort(io='out')
        width=parent.snap
        height=5*zyu+3*zyu*max(len(inport),len(outport))
        height=(height//width+1)*width
        p=(acp.getAcpo('position')[0]*self.zr-parent.rx,
            acp.getAcpo('position')[1]*self.zr-parent.ry)
        super().__init__(parent,
            style={'p':p,'s':(width,height),'bgc':esui.COLOR_BACK,'border':esui.COLOR_FRONT},
            active={'border_width':5,'border':esui.COLOR_TEXT})

        self.acp=acp

        self.stc_name=esui.StaticText(self,
            (0.5*zyu,0.5*zyu),(2*zyu,2*zyu),acp.getAcpo('acp_name'),
            tsize=10*self.zr,align='left')
        acpclass=acp.getAcpo('AcpClass')
        self.stc_class=esui.StaticText(self,
            (0.5*zyu,3.5*zyu),(2*zyu,2*zyu),acpclass[acpclass.rfind('.'):],
            tsize=8*self.zr,align='left')

        i=2
        for port in inport:
            inbtn=esui.SltBtn(self,(width-2.5*zyu,0.5*zyu+i*3*zyu),
                (2*zyu,2*zyu),'<',tsize=8,tip=port.name)
            inbtn.portid=port.pid
            inbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1
        i=2
        for port in outport:
            outbtn=esui.SltBtn(self,(0.5*zyu,0.5*zyu+i*3*zyu),
                (2*zyu,2*zyu),'<',tsize=8,tip=port.name)
            outbtn.portid=port.pid
            outbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1

        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(esui.EBIND_LEFT_DCLK,self.onDClk)
        self.Bind(wx.EVT_LEFT_UP,self.onRls)
        self.Bind(wx.EVT_MOTION,self.onMove)
        self.Bind(wx.EVT_MIDDLE_DOWN,parent.onClkWhl)
        self.Bind(wx.EVT_MIDDLE_UP,parent.onRlsWhl)
        return

    def onClk(self,e):
        self.Parent.start_evtobj=self
        node_cpos=e.GetPosition()
        self.Parent.spos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        if not self.Parent.flag_moving or not self.isActive():
            # Single selecting;
            self.Parent.list_active=[self]
            for node in self.Parent.Children:
                if node!=self:node.setActive(active=False)
        e.Skip()
        return

    def onDClk(self,e):
        ddlg=DetailDialog(esui.UMR.ESMW,(25*xu,10*yu),(50*xu,80*yu),self.acp)
        ddlg.ShowModal()
        return

    def onClkIOBtn(self,e):
        cid=self.acp.getAcpo('acpid')
        cport=e.EventObject.portid

        if self.Parent.first_id is None:
            self.Parent.first_id=cid
            self.Parent.first_port=cport
        else:
            ESC.cntAcp(
                self.Parent.first_id,
                self.Parent.first_port,
                cid,cport,
                esui.UMR.MDL_DIV.mdl)
            self.Parent.first_id=None
            self.Parent.first_port=None
            self.Parent.drawLink()

        # e.Skip()
        return

    def onRls(self,e):
        if self.Parent.start_evtobj!=self:
            self.Parent.onRls(e)
            return
        zr=self.zr
        px=self.Position.x
        py=self.Position.y
        rx=self.Parent.rx
        ry=self.Parent.ry
        mx,my=px,py
        snap=self.Parent.snap
        if self.Parent.flag_moving:
            if self.Parent.flag_attaching:
                if (px+rx)*zr % int(snap)<20:
                    mx=round((px+rx)*zr/snap)*snap-rx*zr
                if (py+ry)*zr % int(snap)<20:
                    my=round((py+ry)*zr/snap)*snap-ry*zr
                self.Move(mx,my)
            for node in self.Parent.list_active:
                node.Refresh()
                p=[(node.Position.x)//zr+rx,(node.Position.y)//zr+ry]
                ESC.setAcp(node.acp,esui.UMR.MDL_DIV.mdl,position=p)
        self.Parent.drawLink()
        return

    def onMove(self,e):
        if self.Parent.start_evtobj!=self:
            self.Parent.onMove(e)
            return
        node_cpos=e.GetPosition()
        cpos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        dx=(cpos[0]-self.Parent.spos[0])
        dy=(cpos[1]-self.Parent.spos[1])
        if self.Parent.flag_moving and e.leftIsDown:
            self.Parent.spos=cpos
            for node in self.Parent.list_active:
                mx=dx+node.Position[0]
                my=dy+node.Position[1]
                node.Move(mx,my)
                self.Parent.drawLink()
        return
    pass

class AcpToolbar(esui.Div):
    def __init__(self,parent:MdlDiv,**argkw):
        super().__init__(parent,**argkw)
        self.Parent:MdlDiv
        self.canvas=self.Parent.canvas
        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Acp')
        self.move_btn=esui.SltBtn(self,(0,2*yu),(4*yu,4*yu),'Mv',option={'border':False})
        self.remove_btn=esui.Btn(self,(0,6*yu),(4*yu,4*yu),'Rm',option={'border':False})
        self.btn_zoom=esui.Btn(self,(0, 10*yu),(4*yu,4*yu),'Zm',option={'border':False})
        self.attach_btn=esui.SltBtn(self,(0,self.Size[1]-4*yu),(4*yu,4*yu),'Att',option={'border':False})

        self.move_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMove)
        self.remove_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkRemove)
        self.attach_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAttach)
        return

    def onClkRemove(self,e):
        self.canvas.rmAcpNodes()
        return

    def onClkMove(self,e):
        self.canvas.flag_moving=not self.canvas.flag_moving
        e.Skip()
        return

    def onClkAttach(self,e):
        self.canvas.flag_attaching=not self.canvas.flag_attaching
        e.Skip()
        return
    pass
