import wx
from core import ESC,esui,esevt
yu=esui.YU
class DetailDialog(esui.EsDialog):
    def __init__(self,parent,p,s,acp):
        super().__init__(parent,p,s,'Acp Detail: '+acp.AcpName)
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.plc_detail=esui.ScrolledPlc(self,(yu,6*yu),
            (self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            border={'all':esui.COLOR_ACTIVE})
        self.plc_port=esui.ScrolledPlc(self,(self.Size.x/2+0.5*yu,6*yu),
            (self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            border={'all':esui.COLOR_ACTIVE})
        if type(acp)==int:acp=ESC.getAcp(acp)
        self.acp=acp
        self.showDetail()
        return

    def onConfirm(self,e):
        set_dcit=dict()
        for ctrl in self.plc_detail.Children:
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                v=ctrl.GetValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif type(ctrl)==esui.SelectBtn:
                v_eval=ctrl.GetValue()
            else:continue
            set_dcit[ctrl.Name]=v_eval
        ESC.setAcp(self.acp.AcpID,set_dcit,esui.ACP_PLC.model_tuple)
        esui.ACP_PLC.drawAcp(refresh=True)
        self.EndModal(1)
        return

    def showDetail(self):
        DP=self.plc_detail
        PP=self.plc_port
        DP.DestroyChildren()
        PP.DestroyChildren()
        acp=self.acp

        esui.StaticText(DP,(yu,0),(8*yu,4*yu),'General:',align='left')
        i=1
        for k,v in acp.__dict__.items():
            if k in acp._acpo_flag['invisible']:continue
            esui.StaticText(DP,(yu,i*4*yu),(12*yu,4*yu),k+':',align='left')
            if k not in acp._acpo_flag['uneditable']:stl=0
            else:stl=wx.TE_READONLY

            if k in acp._acpo_flag['longdata']:
                esui.MultilineText(DP,(yu,(i+1)*4*yu),(DP.Size[0]-2*yu,12*yu),
                    hint=str(v),cn=k,exstl=stl)
                i+=3
            elif type(v)==bool:
                esui.SelectBtn(DP,(14*yu,(i*4+0.5)*yu),(3*yu,3*yu),'√',cn=k,select=v)
            else:
                esui.InputText(DP,(14*yu,(i*4+0.5)*yu),(DP.Size[0]-15*yu,3.5*yu),hint=str(v),cn=k,exstl=stl)
            i+=1

        esui.StaticText(PP,(yu,yu),(8*yu,4*yu),'IO Ports:',align='left')
        btn_out=esui.Btn(PP,(PP.Size[0]-10*yu,yu),(4*yu,4*yu),'+Out')
        btn_in=esui.Btn(PP,(PP.Size[0]-5*yu,yu),(4*yu,4*yu),'+In')
        btn_out.Bind(wx.EVT_LEFT_DOWN,self.onClkAddOutBtn)
        btn_in.Bind(wx.EVT_LEFT_DOWN,self.onClkAddInBtn)
        if acp.fixIO=='In':btn_in.Hide()
        elif acp.fixIO=='Out':btn_out.Hide()
        elif acp.fixIO=='Both':
            btn_in.Hide()
            btn_out.Hide()
        i=1
        for pid,pname in acp.port.items():
            if pid in acp.inport:
                esui.StaticText(PP,(yu,i*5*yu+yu),(10*yu,4*yu),pname+':',align='left')
            else:
                esui.StaticText(PP,(yu,i*5*yu+yu),(10*yu,4*yu),pname+':',align='left')
            btn_del=esui.Btn(PP,(PP.Size[0]-5*yu,i*5*yu+yu),(4*yu,4*yu),'×',cn=str(pid))
            btn_del.Bind(wx.EVT_LEFT_DOWN,self.onClkDelBtn)
            i+=1
        DP.updateVirtualSize()
        PP.updateVirtualSize()
        return

    def onClkAddInBtn(self,e):
        inport=dict(self.acp.inport)
        port=dict(self.acp.port)
        maxid=max(inport.keys())+1
        inport.update({maxid:None})
        port.update({maxid:'in P'})
        ESC.setAcp(self.acp,{'inport':inport,'port':port},esui.ACP_PLC.model_tuple)
        self.showDetail()
        return

    def onClkAddOutBtn(self,e):
        'todo: add outport'
        return

    def onClkDelBtn(self,e):
        pid=int(e.EventObject.Name)
        port=dict(self.acp.port)
        del port[pid]
        if pid in self.acp.inport:
            IO='inport'
            newdict=dict(self.acp.inport)
            if newdict[pid] is not None:
                ESC.connectAcp(self.acp.AcpID,pid,
                    newdict[pid][0],newdict[pid][1],
                    esui.ACP_PLC.model_tuple)
        else:
            IO='outport'
            newdict=dict(self.acp.outport)
            if len(newdict[pid])!=0:
                for tpl in newdict[pid]:
                    ESC.connectAcp(self.acp.AcpID,pid,
                        tpl[0],tpl[1],
                        esui.ACP_PLC.model_tuple)
        del newdict[pid]
        ESC.setAcp(self.acp,{IO:newdict,'port':port},esui.ACP_PLC.model_tuple)
        self.showDetail()
        return
    pass
