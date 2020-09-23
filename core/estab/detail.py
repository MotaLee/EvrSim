import wx
from core import ESC,esui,esevt
yu=esui.YU
class DetailTab(esui.Plc):
    def __init__(self,parent,p,s,tablabel):
        super().__init__(parent,p,s)
        yu=esui.YU

        self.ori_s=s
        self.aobj=None
        self.mode='Aro'     # Or 'Acp';
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.detail_txt=esui.StaticText(self,(yu,yu),(8*yu,4*yu),'Detail:',align='left')
        self.confirm_btn=esui.Btn(self,(self.Size[0]-5*yu,yu),(4*yu,4*yu),label='√')
        self.detail_plc=esui.ScrolledPlc(self,(0,6*yu),(self.Size[0],self.Size[1]-6*yu))
        self.confirm_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkConfirm)
        return

    def onClkConfirm(self,e):
        if self.mode=='Aro':
            arove_dcit=dict()
            for ctrl in self.detail_plc.Children:
                if ctrl.HasExtraStyle(wx.TE_READONLY):continue
                if type(ctrl) is esui.InputText or type(ctrl)==esui.MultilineText:
                    v=ctrl.GetValue()
                    try: v_eval=eval(v)
                    except BaseException:v_eval=v
                    arove_dcit[ctrl.Name]=v_eval
            ESC.setAro(self.aobj.AroID,arove_dcit)
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        elif self.mode=='Acp':
            set_dcit=dict()
            for ctrl in self.detail_plc.Children:
                if type(ctrl)==esui.InputText or type(ctrl)==esui.MultilineText:
                    v=ctrl.GetValue()
                    try: v_eval=eval(v)
                    except BaseException:v_eval=v
                elif type(ctrl)==esui.SelectBtn:
                    v_eval=ctrl.GetValue()
                else:continue
                set_dcit[ctrl.Name]=v_eval
            ESC.setAcp(self.aobj.AcpID,set_dcit,esui.ACP_PLC.model_tuple)
            esui.ACP_PLC.drawAcp(refresh=True)
        # esui.SIDE_PLC.toggleTab('Manager')
        esui.HintText(self,(self.Size[0]-14*yu,yu),(8*yu,4*yu),txt='Updated!')
        return

    def showDetail(self,aobj=None,mode='Aro'):
        DP=self.detail_plc
        DP.DestroyChildren()
        self.mode=mode
        esui.SIDE_PLC.toggleTab('Detail')
        if mode=='Aro':self.showAroDetail(aobj)
        elif mode=='Acp':self.showAcpDetail(aobj)
        DP.updateVirtualSize()

        return

    def showAroDetail(self,aro):
        DP=self.detail_plc
        if aro is None:aro=esui.ARO_PLC.aro_selection[0]
        elif type(aro)==int:aro=ESC.getAro(aro)
        self.aobj=aro
        i=0
        for k,v in aro.__dict__.items():
            if k in aro._Arove_flag['invisible']:continue
            esui.StaticText(DP,(yu,i*4*yu),(12*yu,4*yu),k+':',align='left')
            if k not in aro._Arove_flag['uneditable']:stl=0
            else:stl=wx.TE_READONLY
            if k in aro._Arove_flag['longdata']:
                esui.MultilineText(DP,(yu,(i+1)*4*yu),(DP.Size[0]-2*yu,12*yu),
                    hint=str(v),cn=k,exstl=stl)
                i+=3
            elif type(v)==bool:
                esui.SelectBtn(DP,(14*yu,(i*4+1)*yu),(2*yu,2*yu),'√',cn=k,select=v)
            else:
                esui.InputText(DP,(14*yu,(i*4+0.5)*yu),(DP.Size[0]-15*yu,3.5*yu),hint=str(v),cn=k,exstl=stl)
            i+=1
        return

    def clearDetail(self):
        self.detail_plc.DestroyChildren()
        return

    pass
