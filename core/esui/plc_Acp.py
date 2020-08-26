# Acp panel relavant;
import copy
import interval
import wx
import numpy as np
from core import ESC
from core import esui
from core import esevt

class AcpPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Hide()
        yu=esui.YU

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
    pass

class AcpToolPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        yu=esui.YU
        # self.canvaspl=self.Parent.canvaspl
        self.head=esui.Btn(self,(0,0),(4*yu,2*yu),'Acp')
        self.move_btn=esui.BlSelectBtn(self,(0,2*yu),(4*yu,4*yu),'Mv')
        self.remove_btn=esui.BorderlessBtn(self,(0,6*yu),(4*yu,4*yu),'Rm')
        self.attach_btn=esui.BlSelectBtn(self,(0,self.Size[1]-4*yu),(4*yu,4*yu),'Att')

        self.move_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkMove)
        self.remove_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkRemove)
        self.attach_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAttach)
        # self.mv_btn.Bind(wx.EVT_LEFT_UP,self.onRlsMv)
        # self.mv_btn.Bind(wx.EVT_MOTION,self.onMoveMv)
        return

    def onClkRemove(self,e):
        self.Parent.canvaspl.rmAcpNodes()
        return

    def onClkMove(self,e):
        if self.Parent.canvaspl.acp_moving:
            self.Parent.canvaspl.acp_moving=False
        else:
            self.Parent.canvaspl.acp_moving=True
        e.Skip()
        return

    def onClkAttach(self,e):
        if self.Parent.canvaspl.attaching:
            self.Parent.canvaspl.attaching=False
        else:
            self.Parent.canvaspl.attaching=True
        e.Skip()
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
        self.canvas_size=200*esui.YU

        self.acp_adding=''
        self.acp_pasting=list()
        self.clip_list=list()
        self.acpnode_selection=list()

        self.acp_moving=False
        self.attaching=False
        self.rect_selecting=False

        self.first_id=None
        self.first_port=None
        self.bg_bitmap=wx.Bitmap(self.canvas_size,self.canvas_size)

        self.SetBackgroundColour(esui.COLOR_BACK)
        self.SetVirtualSize(self.canvas_size,self.canvas_size)
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
        if refresh:self.DestroyChildren()
        for node in self.Children:
            if node.acp not in ESC.ACP_MODELS[MT]:node.Destroy()
            else:drawed_list.append(node.acp)
        for acp in ESC.ACP_MODELS[MT]:
            if acp not in drawed_list:AcpNode(self,acp)

        for node in self.Children:
            node.Refresh()

        self.Show()
        self.drawConnection()
        self.Parent.stc_left.SetLabel('Model: '+str(MT))
        self.Parent.stc_right.SetLabel('Count: '+str(len(ESC.ACP_MODELS[MT])))
        # self.Parent.stc_left.Refresh()
        # self.Parent.stc_right.Refresh()
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
        dc.SetPen(wx.Pen(esui.COLOR_SECOND))
        for i in range(1,int(self.canvas_size/snap)):
            lines.append([snap*i+offx,offy,snap*i+offx,self.canvas_size*self.zoom_rate+offy])
            lines.append([offx,snap*i+offy,self.canvas_size*self.zoom_rate+offx,snap*i+offy])
        dc.DrawLineList(lines)

        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        lines=list()
        io_points=list()
        for node in self.Children:
            for ip,ip_tar in node.acp.inport.items():
                # Input lines, inport->tar outport;
                for Btn in node.Children:
                    # Inport position;
                    if type(Btn)==esui.SelectBtn and Btn.portid==ip:
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
                        if type(tarctrl)==esui.SelectBtn:
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
        # if len(self.Parent.model_tuple)!=0:
        #     dc.SetTextForeground(esui.COLOR_TEXT)
        #     dc.DrawText('Model: '+self.Parent.model_tuple[1],0,0)
        #     r_txt='Count: '+str(len(ESC.ACP_MODELS[self.Parent.model_tuple]))
        #     tsize=dc.GetTextExtent(r_txt)
        #     dc.DrawText(r_txt,self.Size[0]-tsize[0],0)
        return

    def addAcpNode(self,acpclass):
        self.spos=(0,0)
        self.acp_adding=acpclass
        return

    def rmAcpNodes(self):
        ''' Return Acps list of removed AcpNodes;'''
        rmed_acp=list()
        for node in self.acpnode_selection:
            acp=ESC.delAcp(node.acp.AcpID,self.Parent.model_tuple)
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
        MT=esui.ACP_PLC.model_tuple
        self.spos=e.GetPosition()
        if self.acp_adding:
            acp=ESC.addAcp(self.acp_adding,MT)
            ESC.setAcp(acp,
                {'AcpName':'Acp','position':[self.spos[0]+self.rx,self.spos[1]+self.ry]},
                MT)
            self.acp_adding=''
            self.drawAcp()
        elif len(self.acp_pasting)!=0:
            p_f=self.acp_pasting[0].position
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
        else:
            self.rect_selecting=True
            self.acpnode_selection=list()
            for node in self.Children:
                node.on_clk=False
                node.Refresh(eraseBackground=False)
        return

    def onRls(self,e):
        cpos=e.GetPosition()
        if self.acp_moving:
            pass
        else:   # Rect selecting;
            self.rect_selecting=False
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
        cpos=e.GetPosition()
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
            if self.rx<0:self.rx=0
            elif self.rx>200*self.canvas_size:self.rx=200*self.canvas_size
            if self.ry<0:self.ry=0
            elif self.ry>200*self.canvas_size:self.ry=200*self.canvas_size
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
        self.SetVirtualSize(self.canvas_size*self.zoom_rate,self.canvas_size*self.zoom_rate)
        return

    def onClkWhl(self,e):
        self.spos=e.GetPosition()
        e.Skip()
        return

    def onRlsWhl(self,e):
        self.Parent.drawConnection()
        return
    pass

class AcpNode(esui.Plc):
    def __init__(self,parent,acp):
        super().__init__(parent,(2000,0),(100,100))
        self.SetBackgroundColour(esui.COLOR_BACK)
        zr=self.Parent.zoom_rate
        yu=esui.YU*zr
        p=[(acp.position[0]-self.Parent.rx)*zr,(acp.position[1]-self.Parent.ry)*zr]
        width=10*esui.YU*zr
        height=3*yu*(1+max(len(acp.inport),len(acp.outport)))+5*yu
        self.SetSize(width,height)
        self.SetPosition(p)

        self.acp=acp
        self.clk_mv=False
        self.on_clk=False

        acpclass=acp.AcpClass[acp.AcpClass.rfind('.'):]
        self.mv_btn=esui.BorderlessBtn(self,(width-2.5*yu,0.5*yu),(2*yu,2*yu),'=')
        self.nametxt=esui.StaticText(self,(0.5*yu,0.5*yu),(width-2*yu,3*yu),acp.AcpName,tsize=int(10*zr),align='left')
        self.classtxt=esui.StaticText(self,(0.5*yu,3.5*yu),(width-2*yu,2*yu),acpclass,tsize=int(8*zr),align='left')
        i=2
        for k in acp.inport.keys():
            inbtn=esui.SelectBtn(self,(width-2.5*yu,0.5*yu+i*3*yu),(2*yu,2*yu),'<',tsize=8,tip=acp.port[k])
            inbtn.portid=k
            inbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1
        i=2
        for k in acp.outport.keys():
            outbtn=esui.SelectBtn(self,(0.5*yu,0.5*yu+i*3*yu),(2*yu,2*yu),'<',tsize=8,tip=acp.port[k])
            outbtn.portid=k
            outbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        self.Bind(wx.EVT_LEFT_UP,self.onRls)
        self.Bind(wx.EVT_MOTION,self.onMove)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.on_clk:
            dc.SetPen(wx.Pen(esui.COLOR_TEXT,width=5))
        else:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=1))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        return

    def onClk(self,e):
        self.on_clk=True
        node_cpos=e.GetPosition()
        self.Parent.spos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        if not e.controlDown:
            self.Parent.acpnode_selection=[self]

            for node in self.Parent.Children:
                if node!=self:
                    node.on_clk=False
                    node.Refresh()
        else:
            self.Parent.acpnode_selection.append(self)
        self.Refresh()
        e.Skip()
        return

    def onDClk(self,e):
        esui.SIDE_PLC.showDetail(self.acp,mode='Acp')
        return

    def onClkIOBtn(self,e):
        cid=self.acp.AcpID
        cport=e.EventObject.portid

        if self.Parent.first_id is None:
            self.Parent.first_id=cid
            self.Parent.first_port=cport
        else:
            ESC.connectAcp(self.Parent.first_id,self.Parent.first_port,cid,cport,esui.ACP_PLC.model_tuple)
            self.Parent.first_id=None
            self.Parent.first_port=None
            self.Parent.drawConnection()

        # e.Skip()
        return

    def onRls(self,e):
        zr=self.Parent.zoom_rate
        px=self.Position[0]
        py=self.Position[1]
        rx=self.Parent.rx
        ry=self.Parent.ry
        mx,my=px,py
        snap=self.Parent.snap
        if self.Parent.acp_moving:
            if self.Parent.attaching:
                if (px+rx)*zr % int(snap)<20:
                    mx=int(round((px+rx)*zr/snap)*snap)-rx
                if (py+ry)*zr % int(snap)<10:
                    my=int(round((py+ry)*zr/snap)*snap)-ry
                self.Move(mx,my)
            for node in self.Parent.acpnode_selection:
                node.Refresh()
                p=[(px+rx)//zr,(py+ry)//zr]
                ESC.setAcp(node.acp.AcpID,{'position':p},esui.ACP_PLC.model_tuple)
        self.Parent.drawConnection()
        return

    def onMove(self,e):
        node_cpos=e.GetPosition()
        cpos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        dx=(cpos[0]-self.Parent.spos[0])
        dy=(cpos[1]-self.Parent.spos[1])
        if self.Parent.acp_moving and e.leftIsDown:
            self.Parent.spos=cpos
            for node in self.Parent.acpnode_selection:
                mx=dx+node.Position[0]
                my=dy+node.Position[1]

                node.Move(mx,my)
        return
    pass
