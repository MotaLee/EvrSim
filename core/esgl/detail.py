import wx
from core import ESC,esui,esevt
yu=esui.YU
class DetailDialog(esui.EsDialog):
    def __init__(self,parent,p,s,aro):
        super().__init__(parent,p,s,'Aro Detail: '+aro.AroName)
        self.conbtn.Bind(wx.EVT_LEFT_UP,self.onConfirm)
        self.plc_detail=esui.ScrolledPlc(self,(yu,6*yu),
            (self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            border={'all':esui.COLOR_ACTIVE})
        self.plc_port=esui.ScrolledPlc(self,(self.Size.x/2+0.5*yu,6*yu),
            (self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
            border={'all':esui.COLOR_ACTIVE})
        self.btn_move=esui.BorderlessBtn(self,(self.Size.x-5*yu,yu),(yu,yu),'=')
        if type(aro)==int:aro=ESC.getAcp(aro)
        self.aro=aro
        self.showDetail()
        return

    def onConfirm(self,e):
        set_dict=dict()
        for ctrl in self.plc_detail.Children:
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                v=ctrl.GetValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif type(ctrl)==esui.SelectBtn:
                v_eval=ctrl.GetValue()
            elif type(ctrl)==esui.Btn and hasattr(ctrl,'value'):
                v_eval=ctrl.value
            else:continue
            set_dict[ctrl.Name]=v_eval
        ESC.setAro(self.aro.AroID,set_dict)
        esui.ARO_PLC.readMap()
        self.EndModal(1)
        return

    def showDetail(self):
        DP=self.plc_detail
        DP.DestroyChildren()
        aro=self.aro

        esui.StaticText(DP,(yu,0),(8*yu,4*yu),'General:',align='left')
        i=1
        for k,v in aro.__dict__.items():
            if k in aro._Arove_flag['invisible']:continue
            esui.StaticText(DP,(yu,i*4*yu),(12*yu,4*yu),k+':',align='left')
            if k not in aro._Arove_flag['uneditable']:stl=0
            else:stl=wx.TE_READONLY

            if k in aro._Arove_flag['longdata']:
                esui.MultilineText(DP,(yu,(i+1)*4*yu),(DP.Size[0]-2*yu,12*yu),
                    hint=str(v),cn=k,exstl=stl)
                i+=3
            elif k in aro._Arove_flag['target']:
                if isinstance(v,list):v=v[0]
                tar=ESC.getAro(v)
                tb1=esui.Btn(DP,(14*yu,(i*4+0.5)*yu),(DP.Size.x-22*yu,3*yu),tar.AroName,cn=k)
                tb1.value=v
                tb2=esui.Btn(DP,(DP.Size.x-7.5*yu,(i*4+0.5)*yu),(3*yu,3*yu),'⇵',cn=k)
                tb3=esui.Btn(DP,(DP.Size.x-4*yu,(i*4+0.5)*yu),(3*yu,3*yu),'×',cn=k)
                tb2.host=tb1
                tb3.host=tb1
                tb2.Bind(wx.EVT_LEFT_DOWN,self.onChangeTarget)
                tb3.Bind(wx.EVT_LEFT_DOWN,self.onRemoveTarget)
            elif type(v)==bool:
                esui.SelectBtn(DP,(14*yu,(i*4+0.5)*yu),(3*yu,3*yu),'√',cn=k,select=v)
            else:
                esui.InputText(DP,(14*yu,(i*4+0.5)*yu),
                    (DP.Size[0]-15*yu,3.5*yu),hint=str(v),cn=k,exstl=stl)
            i+=1

        DP.updateVirtualSize()
        return

    def onChangeTarget(self,e):
        'todo'
        return

    def onRemoveTarget(self,e):
        host=e.EventObject.host
        host.value=None
        host.SetLabel('')
        return
    pass
