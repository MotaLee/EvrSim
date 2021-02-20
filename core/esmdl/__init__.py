# Acp panel relavant;
import copy,interval,wx
import numpy as np
from core import ESC,esui,esevt
from .node import AcpNode
from .toolbar import AcpToolPlc
from .detail import DetailDialog
yu=esui.YU

class AcpPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Hide()

        self.model_tuple=tuple()
        self.toolpl=AcpToolPlc(self,(0,0),(4*yu,self.Size[1]))
        self.stc_left=esui.StaticText(self,(4*yu,0),(12*yu,2*yu),'',tsize=8,align='left')
        self.stc_right=esui.StaticText(self,(self.Size[0]-16*yu,0),(12*yu,2*yu),'',tsize=8,align='right')
        self.canvaspl=AcpCanvasPlc(self,(4*yu,2*yu),(self.Size[0]-4*yu,self.Size[1]-2*yu))
        CP=self.canvaspl
        self.acpnode_selection=CP.acpnode_selection
        self.drawAcp=CP.drawAcp
        self.drawConnection=CP.drawConnection
        self.addAcpNode=CP.addAcpNode
        self.onKeyDown=CP.onKeyDown

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_KEY_DOWN:
            if self.IsShown():self.onKeyDown(e.GetEventArgs(1))
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.Hide()
        return
    pass

class AcpCanvasPlc(wx.ScrolledCanvas):
    def __init__(self,parent,p,s):
        super().__init__(parent,pos=p,size=s)
        self.rx=0
        self.ry=0
        self.zoom_rate=1
        self.spos=[0,0]
        self.snap=10*esui.YU*self.zoom_rate
        self.canvas_width=20*esui.YU+1684
        self.canvas_height=20*esui.YU+1190

        self.acp_adding=''  # AcpClass name;
        self.acp_pasting=list()
        self.clip_list=list()
        self.acpnode_selection=list()

        self.acp_moving=False
        self.attaching=False
        # self.rect_selecting=False

        self.start_evtobj=self
        self.first_id=None
        self.first_port=None
        self.bg_bitmap=wx.Bitmap(self.canvas_width,self.canvas_height)

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
        return

    def drawAcp(self,mdl_tuple=None,refresh=False):
        'Empty para mdl_tuple to draw now model;'
        if mdl_tuple is not None:
            self.Parent.model_tuple=mdl_tuple
            self.Scroll(0,0)
            self.rx=0
            self.ry=0
            self.DestroyChildren()
        MT=self.Parent.model_tuple
        self.acpnode_selection=list()
        if MT not in ESC.ACP_MODELS:return

        drawed_list=list()
        # if refresh:self.DestroyChildren()
        self.DestroyChildren()
        # for node in self.Children:
        #     if node.acp not in ESC.ACP_MODELS[MT]:node.Destroy()
        #     else:drawed_list.append(node.acp)
        for acp in ESC.ACP_MODELS[MT]:
            # if acp not in drawed_list:
            AcpNode(self,acp)

        for node in self.Children:
            node.Refresh()

        self.Show()
        self.drawConnection()
        self.Parent.stc_left.SetLabel('Model: '+str(MT))
        self.Parent.stc_right.SetLabel('Count: '+str(len(ESC.ACP_MODELS[MT])))
        return

    def drawConnection(self):
        yu=esui.YU
        lines=list()
        snap=self.snap
        offx=-1*self.rx
        offy=-1*self.ry

        xdc=wx.ClientDC(self)
        dc=wx.BufferedDC(xdc,buffer=self.bg_bitmap)
        dc.Clear()
        dc.SetPen(wx.Pen(esui.COLOR_ACTIVE))
        for i in range(1,int(self.canvas_width/snap)):
            lines.append([snap*i+offx,offy,snap*i+offx,self.canvas_width*self.zoom_rate+offy])
            lines.append([offx,snap*i+offy,self.canvas_width*self.zoom_rate+offx,snap*i+offy])
        dc.DrawLineList(lines)

        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(10*yu*self.zoom_rate+offx,
            10*yu*self.zoom_rate+offy,
            1684*self.zoom_rate,
            1190*self.zoom_rate)
        lines=list()
        io_points=list()
        for node in self.Children:
            for ip,ip_tar in node.acp.inport.items():
                # Input lines, inport->tar outport;
                for Btn in node.Children:
                    # Inport position;
                    if type(Btn)==esui.SltBtn and Btn.portid==ip:
                        nx=Btn.Position[0]
                        ny=Btn.Position[1]
                        break
                ox=node.Position[0]+nx+2.5*yu*self.zoom_rate
                oy=node.Position[1]+ny+yu*self.zoom_rate

                tny=None
                if ip_tar is not None:
                    tarid=ip_tar[0]
                    tarport=ip_tar[1]
                else: continue
                newlist=list(self.Children)
                for tarnode in newlist:
                    for tarctrl in tarnode.Children:
                        if type(tarctrl)==esui.SltBtn:
                            if tarnode.acp.AcpID==tarid and tarctrl.portid==tarport:
                                tny=tarctrl.Position[1]
                                break
                    if tny:
                        tx=tarnode.Position[0]
                        ty=tarnode.Position[1]+tny+yu*self.zoom_rate
                        break
                io_points.append((ox,oy,tx,ty))
        # dc.DrawLineList(lines)
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

    def addAcpNode(self,acpclass):
        self.spos=(0,0)
        self.acp_adding=acpclass
        return

    def rmAcpNodes(self):
        ''' Return Acps list of removed AcpNodes;'''
        rmed_acp=list()
        for node in self.acpnode_selection:
            acp=ESC.delAcp(node.acp.AcpID,self.Parent.model_tuple,rmlink=False)
            rmed_acp.append(acp)
            node.Destroy()
        esui.SIDE_PLC.clearDetail()
        self.Parent.drawAcp()
        return rmed_acp

    def onKeyDown(self,e,operation=''):
        if e is not None:
            key=e.GetKeyCode()
        else:key=operation
        if (key==ord('C') and e.controlDown) or key=='Copy':
            self.clip_list=list()
            for node in self.acpnode_selection:
                self.clip_list.append(copy.deepcopy(node.acp))
        elif (key==ord('X') and e.controlDown) or key=='Cut':
            self.clip_list=self.rmAcpNodes()
        elif (key==ord('V') and e.controlDown) or key=='Paste':
            if len(self.clip_list)!=0:
                self.acp_pasting=self.clip_list
        return

    def onClk(self,e):
        self.start_evtobj=self
        MT=esui.ACP_PLC.model_tuple
        self.spos=e.GetPosition()
        if self.acp_adding:
            acp=ESC.addAcp(self.acp_adding,MT)
            ESC.setAcp(acp,
                {'AcpName':'Acp_'+str(acp.AcpID),'position':[
                    self.spos[0]/self.zoom_rate+self.rx,
                    self.spos[1]/self.zoom_rate+self.ry]},
                MT)
            self.acp_adding=''
            self.drawAcp()
        elif len(self.acp_pasting)!=0:
            p_f=[5000,5000]
            for acp in self.acp_pasting:
                p_f[0]=min(p_f[0],acp.position[0])
                p_f[1]=min(p_f[1],acp.position[1])

            acpid_table=dict()
            for acp in self.acp_pasting:
                new_acp=ESC.addAcp(acp.AcpClass,MT)
                acpid_table[acp.AcpID]=new_acp.AcpID
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
                ESC.setAcp(acp.AcpID,acp.__dict__,MT)
            self.acp_pasting=list()
            self.drawAcp()
        else:   # Empty click;
            self.acpnode_selection=list()
            for node in self.Children:
                node.on_clk=False
                node.Refresh(eraseBackground=False)
        return

    def onRls(self,e):
        eo=e.EventObject
        if eo==self:cpos=e.GetPosition()
        else:
            ep=e.GetPosition()
            cpos=(eo.Position[0]+ep[0],eo.Position[1]+ep[1])
        # Rect selecting;
        for node in self.Children:
            cx=node.Position[0] in interval.Interval(cpos[0],self.spos[0])
            cy=node.Position[1] in interval.Interval(cpos[1],self.spos[1])
            if cx and cy:
                self.acpnode_selection.append(node)
                node.on_clk=True
            elif node.on_clk:
                node.on_clk=False
            node.Refresh()
        self.drawConnection()
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
            self.drawConnection()
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
        elif e.leftIsDown:  # Rect selecting;
            self.drawConnection()
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
        self.snap=10*esui.YU*self.zoom_rate
        self.drawAcp(refresh=True)
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
        self.Parent.drawConnection()
        return
    pass
