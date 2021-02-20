import wx
from core import ESC,esui,esevt,esgl
yu=esui.YU
class DetailDiv(esui.Div):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.aro=None

        self.btn_con=esui.Btn(self,(self.Size[0]-10*yu,yu),(4*yu,4*yu),txt='√')
        self.btn_can=esui.Btn(self,(self.Size[0]-5*yu,yu),(4*yu,4*yu),txt='×')
        self.div_detail=esui.ScrollDiv(self,style={
            'p':(0,6*yu),
            's':(self.Size[0],self.Size[1]-6*yu),
            'bgc':esui.COLOR_LBACK})
        self.btn_con.Bind(wx.EVT_LEFT_DOWN,self.onClkConfirm)
        self.btn_can.Bind(wx.EVT_LEFT_DOWN,self.onClkCancel)
        return

    def onClkConfirm(self,e):
        arove=dict()
        for ctrl in self.div_detail.getChildren():
            if isinstance(ctrl,(esui.InputText,esui.MultilineText)):
                v=ctrl.GetValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
            elif type(ctrl)==esui.SltBtn:
                v_eval=ctrl.GetValue()
            elif type(ctrl)==esui.Btn and hasattr(ctrl,'value'):
                v_eval=ctrl.value
            else:continue
            arove[ctrl.Name]=v_eval
        ESC.setAro(self.aro.AroID,arove)
        # esui.ARO_PLC.readMap()
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        esui.HintText(self,(self.Size[0]-14*yu,yu),(8*yu,4*yu),txt='Updated!')
        return

    def onClkCancel(self,e):
        esui.SIDE_PLC.hideTab('Detail')
        esui.SIDE_PLC.toggleTab('Manager')
        return

    def showDetail(self,aro=None):
        DP=self.div_detail
        DP.delChildren()
        esui.SIDE_PLC.toggleTab('Detail')
        if aro is None:aro=esgl.ARO_SELECTION[0]
        elif isinstance(aro,int):aro=ESC.getAro(aro)
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
                esui.SltBtn(DP,(14*yu,(i*4+0.5)*yu),(3*yu,3*yu),'√',cn=k,select=v)
            else:
                esui.InputText(DP,(14*yu,(i*4+0.5)*yu),
                    (DP.Size[0]-15*yu,3.5*yu),hint=str(v),cn=k,exstl=stl)
            i+=1
        DP.updateMaxSize()
        return

    def clearDetail(self):
        self.div_detail.delChildren()
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
