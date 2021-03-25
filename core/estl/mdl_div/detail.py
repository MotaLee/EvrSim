import wx
from core import ESC,esui
yu=esui.YU
class DetailDialog(esui.EsDialog):
    def __init__(self,parent,p,s,acp:ESC.Acp):
        super().__init__(parent,p,s,'Acp Detail: '+acp.getAcpo('acp_name'))
        self.acp=acp

        self.div_detail=esui.ScrollDiv(self,style={
            'p':(yu,6*yu),
            's':(self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            'border':esui.COLOR_HOVER})
        self.div_port=esui.ScrollDiv(self,style={
            'p':(self.Size.x/2+0.5*yu,6*yu),
            's':(self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            'border':esui.COLOR_HOVER})

        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.showDetail()
        return

    def onConfirm(self,e):
        set_dcit=dict()
        for ctrl in self.div_detail.Children:
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                v=ctrl.getValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif type(ctrl)==esui.SltBtn:
                v_eval=ctrl.GetValue()
            else:continue
            set_dcit[ctrl.Name]=v_eval
        ESC.setAcp(self.acp,esui.UMR.MDL_DIV.mdl,acpo=set_dcit)
        esui.UMR.MDL_DIV.drawMdl(refresh=True)
        self.EndModal(1)
        return

    def showDetail(self):
        DP=self.div_detail
        PP=self.div_port
        DP.delChildren()
        PP.delChildren()
        acp=self.acp
        acpattr=acp.getAcpAttr()
        esui.StaticText(DP,(yu,0),(8*yu,4*yu),'General:',align='left')
        i=1
        for name,attr in acpattr.items():
            attr:ESC.AcpAttr
            if not attr.flag_visible:continue
            esui.StaticText(DP,(yu,i*4*yu),(12*yu,4*yu),name+':',align='left')
            if attr.flag_fixed:stl=wx.TE_READONLY
            else:stl=0

            if attr.flag_long:
                esui.MultilineText(DP,hint=str(attr.value),cn=name,readonly=stl,
                    style={'p':(yu,(i+1)*4*yu),'s':(DP.Size[0]-2*yu,12*yu)})
                i+=3
            elif isinstance(attr.value,bool):
                esui.SltBtn(DP,(14*yu,(i*4+0.5)*yu),
                    (3*yu,3*yu),'√',cn=name,select=attr.value)
            else:
                esui.InputText(DP,hint=str(attr.value),cn=name,readonly=stl,
                    style={'p':(14*yu,(i*4+0.5)*yu),'s':(DP.Size[0]-15*yu,3.5*yu)})
            i+=1

        esui.StaticText(PP,(yu,yu),(8*yu,4*yu),'IO Ports:',align='left')
        btn_out=esui.Btn(PP,(PP.Size[0]-10*yu,yu),(4*yu,4*yu),'+Out')
        btn_in=esui.Btn(PP,(PP.Size[0]-5*yu,yu),(4*yu,4*yu),'+In')
        btn_out.Bind(wx.EVT_LEFT_DOWN,self.onClkAddOutBtn)
        btn_in.Bind(wx.EVT_LEFT_DOWN,self.onClkAddInBtn)
        if acp.fix_in.value:btn_in.Hide()
        if acp.fix_out.value:btn_out.Hide()
        i=1
        for pid,port in acp.port.value.items():
            if port.io=='in':
                esui.StaticText(PP,(yu,i*5*yu+yu),(10*yu,4*yu),port.name+':',align='left')
            else:
                esui.StaticText(PP,(yu,i*5*yu+yu),(10*yu,4*yu),port.name+':',align='left')
            btn_del=esui.Btn(PP,(PP.Size[0]-5*yu,i*5*yu+yu),(4*yu,4*yu),'×',cn=str(pid))
            btn_del.Bind(wx.EVT_LEFT_DOWN,self.onClkDelBtn)
            i+=1
        DP.updateMaxSize()
        PP.updateMaxSize()
        return

    def onClkAddInBtn(self,e):
        maxid=max([port.pid for port in self.acp.getPort()])+1
        self.acp.addPort(pid=maxid,io='in',name='New')
        self.showDetail()
        return

    def onClkAddOutBtn(self,e):
        'todo: add outport'
        return

    def onClkDelBtn(self,e):
        pid=int(e.EventObject.Name)
        self.acp.delPort(pid)
        self.showDetail()
        return
    pass
