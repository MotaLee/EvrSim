# Acp panel relavant;
import interval
import wx
import numpy as np
from core import ESC
from core import esui

class AcpPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'acppl')
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Hide()
        yu=esui.YU

        self.acpmodel=''

        self.toolpl=AcpToolPlc(self,(0,0),(4*yu,self.Size[1]))

        self.canvaspl=AcpCanvasPlc(self,(4*yu,0),(self.Size[0]-4*yu,self.Size[1]))
        return

    def drawAcp(self,model=None):
        self.canvaspl.drawAcp(model)
        return

    def drawConnection(self):
        self.canvaspl.drawConnection()
        return
    pass

class AcpToolPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'toolpl')
        self.SetBackgroundColour(esui.COLOR_LBACK)
        yu=esui.YU
        # self.canvaspl=self.Parent.canvaspl
        self.head=esui.btn(self,(0,0),(4*yu,2*yu),'Acp')
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
        self.acp_moving=False
        self.attaching=False
        self.selecting=False
        self.spos=(0,0)
        self.zoom_rate=1
        self.snap=10*esui.YU*self.zoom_rate
        self.canvas_size=200*esui.YU
        self.first_id=None
        self.first_port=None
        self.acp_selection=[]
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

    def drawAcp(self,acpmodel=None):
        'Empty para acpmodel to draw now model;'
        if acpmodel is not None:
            self.Parent.acpmodel=acpmodel
        if len(self.Children)!=0:
            self.Hide()
            self.DestroyChildren()
        self.Scroll(0,0)
        self.acp_selection=list()
        if self.Parent.acpmodel not in ESC.ACP_MAP:
            return
        for acp in ESC.ACP_MAP[self.Parent.acpmodel]:
            # Draw Acp node;
            AcpNode(self,acp,self.zoom_rate)

        for node in self.Children:
            node.Refresh()

        self.Scroll(self.rx,self.ry)
        self.Show()
        self.drawConnection()
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
        for node in self.Children:
            for ip,ip_tar in node.acp.inport.items():
                # Input lines, inport->tar outport;
                for btn in node.Children:
                    # Inport position;
                    if type(btn)==esui.SelectBtn and btn.portid==ip:
                        nx=btn.Position[0]
                        ny=btn.Position[1]
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
                lines.append([ox,oy,tx,ty])
        dc.DrawLineList(lines)

        return

    def rmAcpNodes(self):
        for node in self.acp_selection:
            ESC.delAcp(node.acp.AcpID,self.Parent.acpmodel)
            node.Destroy()
        self.Parent.drawAcp()
        return

    def onClk(self,e):
        self.spos=e.GetPosition()
        if self.acp_moving:
            pass
        else:
            self.selecting=True
            self.acp_selection=list()
            for node in self.Children:
                node.on_clk=False
                node.Refresh(eraseBackground=False)
        return

    def onRls(self,e):
        cpos=e.GetPosition()
        if self.acp_moving:
            pass
            # self.acp_moving=False
            # for node in self.acp_selection:
            #     node.Refresh()
            #     p=[0,0]
            #     p[0]=node.Position[0]//self.zoom_rate
            #     p[1]=node.Position[1]//self.zoom_rate
            #     ESC.setAcp(node.acp.AcpID,{'position':p},self.Parent.acpmodel)
        else:   # Rect selecting;
            self.selecting=False
            for node in self.Children:
                cx=node.Position[0] in interval.Interval(cpos[0],self.spos[0])
                cy=node.Position[1] in interval.Interval(cpos[1],self.spos[1])
                if cx and cy:
                    self.acp_selection.append(node)
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
        if self.acp_moving and e.leftIsDown:
            pass
            # self.spos=cpos
            # # dc=wx.ClientDC(self)
            # # dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            # # dc.DrawCircle(cpos,5)
            # for node in self.acp_selection:
            #     mx=dx+node.Position[0]
            #     my=dy+node.Position[1]
            #     if self.attaching:
            #         if (mx+self.rx) % int(self.snap)<5:
            #             mx=int(round(mx/self.snap)*self.snap-self.rx)
            #         if (my+self.ry) % int(self.snap)<5:
            #             my=int(round(my/self.snap)*self.snap-self.ry)
            #     node.Move(mx,my)
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
        self.drawAcp()
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
    def __init__(self,parent,acp,zr=1):
        yu=esui.YU*zr
        p=[acp.position[0]*zr,acp.position[1]*zr]
        width=10*esui.YU*zr
        height=3*yu*(1+max(len(acp.inport),len(acp.outport)))+5*yu
        super().__init__(parent,p,(width,height))

        self.acp=acp
        self.clk_mv=False
        self.on_clk=False
        self.zr=zr

        acpclass=acp.AcpClass[acp.AcpClass.rfind('.'):]
        self.mv_btn=esui.BorderlessBtn(self,(width-2.5*yu,0.5*yu),(2*yu,2*yu),'=')
        self.nametxt=esui.Stc(self,(0.5*yu,0.5*yu),(width-2*yu,2*yu),acp.AcpName,tsize=int(10*zr),align='left')
        self.classtxt=esui.Stc(self,(0.5*yu,2.5*yu),(width-2*yu,2*yu),acpclass,tsize=int(8*zr),align='left')
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
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        return

    def onClk(self,e):
        self.on_clk=True
        node_cpos=e.GetPosition()
        self.Parent.spos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        if not e.controlDown:
            self.Parent.acp_selection=[self]

            for node in self.Parent.Children:
                if node!=self:
                    node.on_clk=False
                    node.Refresh()
        else:
            self.Parent.acp_selection.append(self)
        self.Refresh()
        e.Skip()
        return

    def onDClk(self,e):
        esui.SIDE_PLC.showAcpDetail(self.acp)
        return

    def onClkIOBtn(self,e):
        cid=self.acp.AcpID
        cport=e.EventObject.portid

        if self.Parent.first_id is None:
            self.Parent.first_id=cid
            self.Parent.first_port=cport
        else:
            ESC.connectAcp(self.Parent.first_id,self.Parent.first_port,cid,cport,esui.ACP_PLC.acpmodel)
            self.Parent.first_id=None
            self.Parent.first_port=None
            self.Parent.drawConnection()

        # e.Skip()
        return

    def onRls(self,e):
        # node_cpos=e.GetPosition()
        # cpos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        if self.Parent.acp_moving:
            # self.acp_moving=False
            for node in self.Parent.acp_selection:
                node.Refresh()
                p=[0,0]
                p[0]=node.Position[0]//self.Parent.zoom_rate
                p[1]=node.Position[1]//self.Parent.zoom_rate
                ESC.setAcp(node.acp.AcpID,{'position':p},esui.ACP_PLC.acpmodel)
        self.Parent.drawConnection()
        return

    def onMove(self,e):
        node_cpos=e.GetPosition()
        cpos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        dx=(cpos[0]-self.Parent.spos[0])
        dy=(cpos[1]-self.Parent.spos[1])
        if self.Parent.acp_moving and e.leftIsDown:
            self.Parent.spos=cpos
            for node in self.Parent.acp_selection:
                mx=dx+node.Position[0]
                my=dy+node.Position[1]
                if self.Parent.attaching:
                    if (mx+self.Parent.rx) % int(self.Parent.snap)<5:
                        mx=int(round(mx/self.Parent.snap)*self.Parent.snap-self.Parent.rx)
                    if (my+self.Parent.ry) % int(self.Parent.snap)<5:
                        my=int(round(my/self.Parent.snap)*self.Parent.snap-self.Parent.ry)
                node.Move(mx,my)
        return
    pass
