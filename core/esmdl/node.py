import wx
from core import ESC,esui
from .detail import DetailDialog
yu=esui.YU
xu=esui.XU

class AcpNode(esui.Plc):
    def __init__(self,parent,acp):
        super().__init__(parent,(2000,0),(100,100))
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.zr=self.Parent.zoom_rate
        self.yu=esui.YU*self.zr
        zr=self.zr
        yu=self.yu
        p=[acp.position[0]*zr-self.Parent.rx,acp.position[1]*zr-self.Parent.ry]
        width=self.Parent.snap
        height=3*yu*max(len(acp.inport),len(acp.outport))+5*yu
        height=(round(height//width)+1)*width
        self.SetSize(width,height)
        self.SetPosition(p)

        self.acp=acp
        self.on_clk=False

        i=2
        for k in acp.inport.keys():
            inbtn=esui.SltBtn(self,(width-2.5*yu,0.5*yu+i*3*yu),
                (2*yu,2*yu),'<',tsize=8,tip=acp.port[k])
            inbtn.portid=k
            inbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1
        i=2
        for k in acp.outport.keys():
            outbtn=esui.SltBtn(self,(0.5*yu,0.5*yu+i*3*yu),(2*yu,2*yu),'<',tsize=8,tip=acp.port[k])
            outbtn.portid=k
            outbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkIOBtn)
            i+=1

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        self.Bind(wx.EVT_LEFT_UP,self.onRls)
        self.Bind(wx.EVT_MOTION,self.onMove)
        self.Bind(wx.EVT_MIDDLE_DOWN,self.Parent.onClkWhl)
        self.Bind(wx.EVT_MIDDLE_UP,self.Parent.onRlsWhl)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.on_clk:
            dc.SetPen(wx.Pen(esui.COLOR_TEXT,width=5))
        else:
            dc.SetPen(wx.Pen(esui.COLOR_FRONT,width=1))
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        dc.SetTextForeground(esui.COLOR_TEXT)
        dc.SetFont(esui.ESFont(size=10*self.zr))
        dc.DrawText(self.acp.AcpName,0.5*self.yu,0.5*self.yu)

        acpclass=self.acp.AcpClass[self.acp.AcpClass.rfind('.'):]
        dc.SetFont(esui.ESFont(size=8*self.zr))
        dc.DrawText(acpclass,0.5*self.yu,3.5*self.yu)
        return

    def onClk(self,e):
        self.Parent.start_evtobj=self
        node_cpos=e.GetPosition()
        self.Parent.spos=[self.Position[0]+node_cpos[0],self.Position[1]+node_cpos[1]]
        if not self.Parent.acp_moving or not self.on_clk:
            # Single selecting;
            self.on_clk=True
            self.Parent.acpnode_selection=[self]
            for node in self.Parent.Children:
                if node!=self:
                    node.on_clk=False
                    node.Refresh()
        self.Refresh()
        e.Skip()
        return

    def onDClk(self,e):
        ddlg=DetailDialog(esui.WXMW,(25*xu,10*yu),(50*xu,80*yu),self.acp)
        ddlg.ShowModal()
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
        if self.Parent.acp_moving:
            if self.Parent.attaching:
                if (px+rx)*zr % int(snap)<20:
                    mx=round((px+rx)*zr/snap)*snap-rx*zr
                if (py+ry)*zr % int(snap)<20:
                    my=round((py+ry)*zr/snap)*snap-ry*zr
                self.Move(mx,my)
            for node in self.Parent.acpnode_selection:
                node.Refresh()
                p=[(node.Position.x)//zr+rx,(node.Position.y)//zr+ry]
                ESC.setAcp(node.acp.AcpID,{'position':p},esui.ACP_PLC.model_tuple)
        self.Parent.drawConnection()
        return

    def onMove(self,e):
        if self.Parent.start_evtobj!=self:
            self.Parent.onMove(e)
            return
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
