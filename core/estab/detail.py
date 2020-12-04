import wx
from core import ESC,esui,esevt,esgl
yu=esui.YU
class DetailTab(esui.Plc):
    def __init__(self,parent,p,s,tablabel):
        super().__init__(parent,p,s)

        self.ori_s=s
        self.aro=None
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.btn_con=esui.Btn(self,(self.Size[0]-10*yu,yu),(4*yu,4*yu),label='√')
        self.btn_can=esui.Btn(self,(self.Size[0]-5*yu,yu),(4*yu,4*yu),label='×')
        self.plc_detail=esui.ScrolledPlc(self,(0,6*yu),(self.Size[0],self.Size[1]-6*yu))
        self.btn_con.Bind(wx.EVT_LEFT_DOWN,self.onClkConfirm)
        return

    def onClkConfirm(self,e):
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
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        esui.HintText(self,(self.Size[0]-14*yu,yu),(8*yu,4*yu),txt='Updated!')
        return

    def showDetail(self,aro=None):
        DP=self.plc_detail
        DP.DestroyChildren()
        esui.SIDE_PLC.toggleTab('Detail')
        if aro is None:aro=esgl.ARO_SELECTION[0]
        elif type(aro)==int:aro=ESC.getAro(aro)
        self.aro=aro
        esui.StaticText(self,(yu,0),(8*yu,4*yu),aro.AroName+' Detail:',align='left')
        i=0
        for k,v in aro.__dict__.items():
            if k[0]=='_':continue
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

    def clearDetail(self):
        self.plc_detail.DestroyChildren()
        return

    def onChangeTarget(self,e):
        'todo: better picking'
        host=e.EventObject.host
        aro=esgl.ARO_SELECTION[0]
        host.value=aro.AroID
        host.SetLabel(aro.AroName)
        host.Refresh()
        return

    def onRemoveTarget(self,e):
        host=e.EventObject.host
        host.value=None
        host.SetLabel('')
        host.Refresh()
        return
    pass
