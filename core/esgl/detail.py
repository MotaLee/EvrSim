import wx
from core import ESC,esui
yu=esui.YU
class DetailDialog(esui.EsDialog):
    def __init__(self,parent,p,s,aro):
        super().__init__(parent,p,s,'Aro Detail: '+aro.AroName)
        self.conbtn.Bind(wx.EVT_LEFT_UP,self.onConfirm)
        self.div_detail=esui.ScrollDiv(self,style={'p':(yu,6*yu),
            's':(self.Size.x/2-1.5*yu,self.Size.x-12*yu),
            'border':esui.COLOR_HOVER})
        # self.div_port=esui.ScrollDiv(self,style={
        #     'p':(self.Size.x/2+0.5*yu,6*yu),
        #     's':(self.Size.x/2-1.5*yu,self.Size[1]-12*yu),
        #     'border':esui.COLOR_HOVER})
        self.btn_move=esui.Btn(self,(self.Size.x-5*yu,yu),(yu,yu),'=',option={'border':False})
        if type(aro)==int:aro=ESC.getAcp(aro)
        self.aro=aro
        self.showDetail()
        return

    def onConfirm(self,e):
        set_dict=dict()
        for ctrl in self.div_detail.getChildren():
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                v=ctrl.getValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif type(ctrl)==esui.SltBtn:
                v_eval=ctrl.GetValue()
            elif type(ctrl)==esui.Btn and hasattr(ctrl,'value'):
                v_eval=ctrl.value
            else:continue
            set_dict[ctrl.Name]=v_eval
        ESC.setAro(self.aro.AroID,**set_dict)
        esui.UMR.MAP_DIV.readMap()
        self.EndModal(1)
        return

    def showDetail(self):
        DP=self.div_detail
        DP.delChildren()
        aro=self.aro

        esui.StaticText(DP,(yu,0),(8*yu,4*yu),'General:',align='left')
        i=1
        for k,v in aro.__dict__.items():
            if k in aro._flag['hide']:continue
            esui.StaticText(DP,(yu,i*4*yu),(12*yu,4*yu),k+':',align='left')
            if k not in aro._flag['lock']:stl=0
            else:stl=wx.TE_READONLY

            if k in aro._flag['long']:
                esui.MultilineText(DP,hint=str(v),cn=k,readonly=stl,
                    style={'p':(yu,(i+1)*4*yu),'s':(DP.Size[0]-2*yu,12*yu)})
                i+=3
            elif k in aro._flag['target']:
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
                esui.SltBtn(DP,(14*yu,(i*4+0.5)*yu),(3*yu,3*yu),'√',cn=k,select=v)
            else:
                esui.InputText(DP,hint=str(v),cn=k,readonly=stl,
                    style={'p':(14*yu,(i*4+0.5)*yu),'s':(DP.Size[0]-15*yu,3.5*yu)})
            i+=1

        DP.updateMaxSize()
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
