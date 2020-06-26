import wx
import numpy as np
from core import ESC
from core import esui
gmv=esui.gmv
# Panel container wx sub class;
class Plc(wx.Panel):
    '''Base container.

        Ctrl in Plc can only call other TopPlc;'''
    def __init__(self,parent,p,s,cn=''):
        wx.Panel.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            name=cn,
            style=wx.NO_BORDER)
        self.SetBackgroundColour(gmv.COLOR_Back)
        return
    pass

class ComPlc(Plc):
    def __init__(self,parent,p,s):
        Plc.__init__(self,parent,p,s)
        self.SetBackgroundColour('#333333')

        self.sidepl_agent=None

        yu=gmv.YU
        # xu=gmv.XU
        self.es_btn=esui.BorderlessBtn(self,(0,0),(4*yu,4*yu),'ES')
        self.sim_menu=esui.BorderlessMenuBtn(self,(4*yu+1,1),(8*yu-2,4*yu-2),
            'Sim',['New','Open','Save','Save as','Mods','Reset'])
        self.map_menu=esui.BorderlessMenuBtn(self,(12*yu+1,1),(8*yu-2,4*yu-2),
            'Map',['New','Delete','Rename','Save as','Snapshot','Manage'])
        self.mdl_menu=esui.BorderlessMenuBtn(self,(20*yu+1,1),(8*yu-2,4*yu-2),
            'Model',['New','Delete','Rename','Save as','Manage'])
        self.help_menu=esui.BorderlessMenuBtn(self,(28*yu+1,1),(8*yu-2,4*yu-2),
            'Help',['Help','About'])

        # self.comhead=esui.Stc(self,(75*xu,0),(4*xu,4*yu),'ES>>',tsize=1.5*yu)
        # self.comtxt=esui.Tcc(self,(79*xu,0),(21*xu-8*yu,4*yu),tsize=1.5*yu)
        self.com_btn=esui.BorderlessBtn(self,(self.Size[0]-8*yu,0),(4*yu,4*yu),'<<')
        self.ext_btn=esui.BorderlessBtn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'X')

        # self.comhead.Hide()
        # self.comtxt.Hide()
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.com_btn.Bind(wx.EVT_BUTTON,self.onClkCom)
        self.ext_btn.Bind(wx.EVT_BUTTON,self.onClkExt)
        self.sim_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkSim)
        self.mdl_menu.GetPopupControl().lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkModel)

        # comtxt.Bind(wx.EVT_TEXT_ENTER,wxmw.esWxCom)
        # histxt=esui.Tcc(wxmw,(0,4*yu),(75*xu,21*yu),
        # tsize=1.5*yu,exstl=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL)
        # est=subprocess.Popen('python est.py wx',
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.STDOUT,
        #     universal_newlines=True,encoding='utf-8')
        # histxt.Bind(wx.EVT_KEY_DOWN,wxmw.onhisHide)
        # histxt.Hide()
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#333333'))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)

        return

    def onClkSim(self,e):
        fc=self.sim_menu.GetPopupControl()
        if fc.ipos==0:
            DlgType=esui.NewDialog
        elif fc.ipos==1:
            DlgType=esui.OpenDialog

        if fc.ipos==2:
            if not ESC.SIM_NAME:return
            DlgType=None
            ESC.saveSim()
            self.sim_menu.HidePopup()
        elif fc.ipos==3:
            if not ESC.SIM_NAME:return
        elif fc.ipos==4:
            if not ESC.SIM_NAME:return
            # DlgType=esui.ModDialog
        if DlgType:
            xu=gmv.XU
            yu=gmv.YU
            wxmw=self.Parent
            wxmw.dlgw=DlgType(wxmw,(20*xu,20*yu),(60*xu,60*yu),fc.items[fc.ipos])
            wxmw.dlgw.ShowModal()
        return

    def onClkModel(self,e):
        if not ESC.SIM_NAME:return
        if self.sidepl_agent is None:
            self.sidepl_agent=self.Parent.FindWindowByName('sidepl')
        pc=self.mdl_menu.GetPopupControl()

        if pc.ipos==0:  # New;
            ESC.newModelFile('New model')
            self.sidepl_agent.loadModels([(ESC.SIM_NAME,'New model')])
            self.sidepl_agent.acp_btn.onClk(None)
            self.sidepl_agent.onClkAcpTabBtn(None)
        elif pc.ipos==1:    # Delete;
            pass
        elif pc.ipos==2:    # Rename;
            pass
        elif pc.ipos==3:    # Save as;
            pass
        elif pc.ipos==4:    # Manage;
            pass
        e.Skip()
        return

    def onClkCom(self,e):

        return

    def onClkExt(self,e):
        if ESC.SIM_FD is not None:ESC.closeSim()
        # est.kill()
        # wxapp.Destroy()
        exit()
        return

    pass

class SidePlc(Plc):

    def __init__(self,parent,p,s):
        Plc.__init__(self,parent,p,s,cn='sidepl')
        self.SetBackgroundColour('#333333')
        self.model_list=list()
        self.aropl_agent=self.Parent.FindWindowByName('aropl')
        self.acppl_agent=self.Parent.FindWindowByName('acppl')
        yu=gmv.YU
        self.aro_btn=esui.TabBtn(self,(1,0),(s[0]/3,4*yu),'Aro','Aro_btn')
        self.aro_tab=esui.AroSideTab(self,(0,4*yu),(s[0],92*yu),'Aro','Aro_tab')
        self.aro_btn.SetValue(True)

        self.arove_btn=esui.TabBtn(self,(1+s[0]/3,0),(s[0]/3,4*yu),'Arove','Arove_btn')
        self.arove_tab=esui.AroveSideTab(self,(0,4*yu),(s[0],92*yu),'Arove','Arove_tab')

        self.acp_btn=esui.TabBtn(self,(1+2*s[0]/3,0),(s[0]/3,4*yu),'Acp','Acp_btn')
        self.acp_tab=esui.AcpSideTab(self,(0,4*yu),(s[0],92*yu),'Acp','Acp_tab')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.aro_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAroTabBtn)
        self.aro_tab.arotree.Bind(wx.EVT_LEFT_DOWN,self.onClkAroList)
        self.aro_tab.arotree.Bind(wx.EVT_LEFT_DCLICK,self.onDClkAroList)
        self.arove_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAroveTabBtn)
        self.acp_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAcpTabBtn)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#333333'))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        return

    def loadMaps(self,maps):
        '''Load maps;'''
        self.maps=maps
        self.aro_tab.map_menu.setItems(maps)
        return

    def loadModels(self,models):
        for model in models:
            if model not in self.model_list:
                self.model_list.append(model)
        self.acp_tab.model_menu.setItems(self.model_list)
        self.acp_tab.model_menu.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.acp_tab.onClkAcpModel)
        self.acp_tab.model_menu.PopupControl.ipos=len(self.model_list)-1
        self.acp_tab.onClkAcpModel(None)
        return

    def updateAroList(self):
        tree=list()
        for aro in ESC.ARO_MAP:tree.append(aro.AroID)
        self.aro_tab.arotree.updateList(tree)
        return

    def showArove(self,aroid):
        self.onClkAroveTabBtn(None)
        self.arove_btn.onClk(None)
        self.arove_tab.showAroveDetail(aroid)
        return

    def showAcpDetail(self,acp):
        self.acp_tab.showAcpDetail(acp)
        return

    def onClkAcpTabBtn(self,e):
        self.aropl_agent.Hide()
        self.acppl_agent.Show()
        self.acppl_agent.drawConnection()
        if e is not None:e.Skip()
        return

    def onClkAroveTabBtn(self,e=None):
        self.aropl_agent.Show()
        self.acppl_agent.Hide()
        if e is not None:e.Skip()
        return

    def onClkAroTabBtn(self,e):
        self.aropl_agent.Show()
        self.acppl_agent.Hide()
        e.Skip()
        return

    def onClkAroList(self,e):
        ipos=e.EventObject.ipos
        aroid=e.EventObject.items[ipos]
        self.aropl_agent.highlightAroes([aroid])
        e.Skip()
        return

    def onDClkAroList(self,e):
        aroid=e.EventObject.items[e.EventObject.ipos]
        self.showArove(aroid)
        return

    pass

class ModPlc(Plc):
    def __init__(self,parent,p,s):
        Plc.__init__(self,parent,p,s,cn='modpl')
        self.SetBackgroundColour(gmv.COLOR_Back)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#333333'))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return

    def loadMod(self):
        'Build mod panel with ESC.MOD_LIST;'
        xu=gmv.XU
        yu=gmv.YU
        self.DestroyChildren()
        for i in range(0,len(ESC.MOD_LIST)):
            esui.TabBtn(self,(i*(6.25*xu+2),0),(6.25*xu,4*yu),
                tablabel=ESC.MOD_LIST[i],
                cn=ESC.MOD_LIST[i]+'btn')
            esui.ModTab(self,(0,4*yu),(75*xu,17*yu-2),
                tablabel=ESC.MOD_LIST[i],
                cn=ESC.MOD_LIST[i]+'tab')
        self.FindWindowByName('AroCorebtn').SetValue(True)
        self.FindWindowByName('AroCoretab').Show()
        return
    pass

# Acp panel relavant;
class AcpPlc(Plc):
    def __init__(self,parent,p,s):
        Plc.__init__(self,parent,p,s,'acppl')
        self.SetBackgroundColour('#333333')
        self.Hide()

        self.zoom_rate=1
        self.inner_size=2000
        self.acpmodel=''
        self.first_id=None
        self.first_port=None

        self.innerpl=Plc(self,(0,0),(self.inner_size,self.inner_size),'innerpl')
        # self.innerpl.Bind(wx.EVT_PAINT,self.onPaint)
        self.innerpl.Bind(wx.EVT_MOTION,self.onPan)
        self.innerpl.Bind(wx.EVT_MOUSEWHEEL,self.onZoom)
        self.innerpl.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhl)
        self.innerpl.Bind(wx.EVT_MIDDLE_UP,self.onRlsWhl)
        return

    def drawAcp(self,acpmodel=None):
        'Empty para acpmodel to draw now model;'
        if acpmodel is not None:
            self.acpmodel=acpmodel
        self.innerpl.DestroyChildren()
        if self.acpmodel not in ESC.ACP_MAP:
            return
        for acp in ESC.ACP_MAP[self.acpmodel]:
            # Draw Acp node;
            AcpNode(self.innerpl,acp,self.zoom_rate)

        for acp in self.innerpl.Children:
            acp.Refresh()

        self.drawConnection()
        return

    def drawConnection(self):
        snap=100*self.zoom_rate
        dc=wx.ClientDC(self.innerpl)
        dc.Clear()
        dc.SetPen(wx.Pen('#555555'))
        lines=list()
        snaplen=int(self.inner_size//snap)
        for i in range(1,snaplen):
            lines.append([snap*i,0,snap*i,self.innerpl.Size[1]])
            lines.append([0,snap*i,self.innerpl.Size[0],snap*i])
        dc.DrawLineList(lines)

        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        # xu=gmv.XU
        yu=gmv.YU
        lines=list()
        for node in self.innerpl.Children:
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
                newlist=list(self.innerpl.Children)
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

    def onPaint(self,e):
        dc=wx.PaintDC(self.innerpl)
        dc.SetPen(wx.Pen('#555555'))
        for i in range(1,self.inner_size//100):
            dc.DrawLine(100*i,0,100*i,self.innerpl.Size[1])
            dc.DrawLine(0,100*i,self.innerpl.Size[0],100*i)
        e.Skip()
        return

    def onPan(self,e):
        if e.middleIsDown:
            cpos=e.GetPosition()
            dx=(cpos[0]-self.spos[0])
            dy=(cpos[1]-self.spos[1])
            dx+=self.innerpl.Position[0]
            dy+=self.innerpl.Position[1]
            if dx>0:dx=0
            if dy>0:dy=0
            self.innerpl.Move(dx,dy)
            # self.drawConnection()
        e.Skip()
        return

    def onZoom(self,e):
        ZS=1    # Zoom speed;
        t=np.sign(e.WheelRotation)
        if self.zoom_rate<0.5 and t<0:return
        if self.zoom_rate>1.5 and t>0:return
        self.zoom_rate+=t/10*ZS
        self.drawAcp()
        return

    def onClkWhl(self,e):
        self.spos=e.GetPosition()
        e.Skip()
        return

    def onRlsWhl(self,e):
        self.drawConnection()
        return
    pass

class AcpNode(Plc):
    def __init__(self,parent,acp,zr=1):
        yu=gmv.YU*zr
        p=[acp.position[0]*zr,acp.position[1]*zr]
        width=200*zr
        height=3*yu*(1+max(len(acp.inport),len(acp.outport)))+5*yu
        Plc.__init__(self,parent,p,(width,height))

        acpclass=acp.AcpClass[acp.AcpClass.rfind('.'):]
        self.mvbtn=esui.BorderlessBtn(self,(width-4.5*yu,0.5*yu),(4*yu,4*yu),'=')
        self.rmbtn=esui.BorderlessBtn(self,(width-8.5*yu,0.5*yu),(4*yu,4*yu),'X')
        self.nametxt=esui.Stc(self,(0.5*yu,0.5*yu),(width-12*yu,4*yu),acp.AcpName,tsize=int(12*zr),align='left')
        self.classtxt=esui.Stc(self,(0.5*yu,4.5*yu),(12*yu,2*yu),acpclass,tsize=int(8*zr),align='left')

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

        self.acp=acp
        self.clk_mv=False
        self.dclk=False
        self.zr=zr
        self.host=self.Parent.Parent    # acppl.innerpl.self;
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_LEFT_DCLICK,self.onDClk)
        self.mvbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkMv)
        self.mvbtn.Bind(wx.EVT_LEFT_UP,self.onRlsMv)
        self.mvbtn.Bind(wx.EVT_MOTION,self.onMoveMv)
        self.rmbtn.Bind(wx.EVT_LEFT_DOWN,self.onClkRm)

        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        if self.dclk:
            dc.SetPen(wx.Pen(gmv.COLOR_Text,width=5))
        else:
            dc.SetPen(wx.Pen(gmv.COLOR_Front,width=1))
        dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        return

    def onClkMv(self,e):
        self.clk_mv=True
        self.spos=e.GetPosition()
        return

    def onRlsMv(self,e):
        self.clk_mv=False
        self.Refresh()
        p=[0,0]
        p[0]=self.Position[0]//self.zr
        p[1]=self.Position[1]//self.zr
        ESC.setAcp(self.acp.AcpID,{'position':p},self.host.acpmodel)
        self.host.drawConnection()
        return

    def onMoveMv(self,e):
        if self.clk_mv:
            cpos=e.GetPosition()
            dx=(cpos[0]-self.spos[0])
            dy=(cpos[1]-self.spos[1])
            dx+=self.Position[0]
            dy+=self.Position[1]
            self.Move(dx,dy)
        # e.Skip()

        return

    def onDClk(self,e):
        self.dclk=True
        for node in self.host.innerpl.Children:
            if node!=self:
                node.dclk=False
                node.Refresh()
        self.Refresh()
        wxmw=self.host.Parent
        sidepl=wxmw.FindWindowByName('sidepl')
        sidepl.showAcpDetail(self.acp)
        return

    def onClkIOBtn(self,e):
        cid=self.acp.AcpID
        cport=e.EventObject.portid

        if self.host.first_id is None:
            self.host.first_id=cid
            self.host.first_port=cport
        else:
            ESC.connectAcp(self.host.first_id,self.host.first_port,cid,cport,self.host.acpmodel)
            self.host.first_id=None
            self.host.first_port=None
            self.host.drawConnection()

        # e.Skip()
        return

    def onClkRm(self,e):
        ESC.delAcp(self.acp.AcpID,self.host.acpmodel)
        self.host.drawAcp()
        return
    pass
