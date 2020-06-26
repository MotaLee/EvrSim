# Parent lib;
import wx
from core import ESC
from core import esui
gmv=esui.gmv

# Tab btn wx sub class;
class TabBtn(wx.ToggleButton):
    '''Label of btn and its tab must be the same.
    btn.cn is label+btn, while tab.cn is label+tab;'''
    def __init__(self,parent,p,s,tablabel,cn=''):
        wx.ToggleButton.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            label=tablabel,
            name=cn,
            style=wx.NO_BORDER)
        self.on_ctrl=False
        self.SetBackgroundColour(gmv.COLOR_Back)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW,self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW,self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        self.SetValue(True)
        for ctrl in self.Parent.Children:
            if type(ctrl)==TabBtn and ctrl!=self:
                ctrl.SetValue(False)
            if isinstance(ctrl,wx.Panel):
                if ctrl.GetLabel()==self.GetLabel():
                    ctrl.Show()
                else: ctrl.Hide()
        return

    def onPaint(self,e):
        dc = wx.PaintDC(self)
        if self.GetValue(): pw=8
        else:pw=1
        dc.SetPen(wx.Pen(gmv.COLOR_Front,width=pw))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        dc.SetTextForeground(gmv.COLOR_Text)
        tsize=dc.GetTextExtent(self.GetLabel())
        dc.DrawText(self.GetLabel(),(self.Size[0]-tsize[0])/2,(self.Size[1]-tsize[1])/2)
        return

    def onEnter(self,e):
        self.on_ctrl=True
        self.SetBackgroundColour('#555555')
        return

    def onLeave(self,e):
        self.on_ctrl=False
        self.SetBackgroundColour(gmv.COLOR_Back)
        return
    pass

# Mod tab wx sub class;
class ModTab(wx.Panel):
    'Para tablabel is also mod name;'
    def __init__(self,parent,p,s,tablabel,cn=''):
        wx.Panel.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            name=cn,
            style=wx.NO_BORDER)
        self.Hide()
        self.SetLabel(tablabel)
        self.SetBackgroundColour(gmv.COLOR_Back)

        # Build tools;
        _locals=dict(locals())
        exec('from mod.'+tablabel+' import TOOL_INDEX as toollist',globals(),_locals)
        toollist=_locals['toollist']
        for tool in toollist:
            _locals=dict(locals())
            exec('from mod.'+tablabel+' import '+tool,globals(),_locals)
            toolctrl=_locals[tool]
            toolctrl.build(self)
        return
    pass

# Side tab wx sub class;
class SideTab(wx.Panel):
    'Tab container.Label is btn.cn+tab;'
    def __init__(self,parent,p,s,tablabel,cn=''):
        wx.Panel.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            name=cn,
            style=wx.NO_BORDER)
        self.Hide()
        self.SetLabel(tablabel)
        self.SetBackgroundColour('#333333')
        return
    pass

class AroSideTab(SideTab):
    def __init__(self,parent,p,s,tablabel,cn=''):
        SideTab.__init__(self,parent,p,s,tablabel,cn)
        yu=gmv.YU
        xu=gmv.XU
        self.map_menu=esui.MenuBtn(self,(yu,yu),(8*yu,4*yu),'Load Map',[])
        self.filterbtn=esui.MenuBtn(self,(25*xu-9*yu,yu),(8*yu,4*yu),'Filter',['None','AroSpace'])
        self.arotree=esui.ListBox(self,(yu,6*yu),(25*xu-2*yu,50*yu))
        self.Show()
        return
    pass

class AroveSideTab(SideTab):
    def __init__(self,parent,p,s,tablabel,cn=''):
        SideTab.__init__(self,parent,p,s,tablabel,cn)
        yu=gmv.YU
        # xu=gmv.XU
        self.updeate_btn=esui.btn(self,(self.Size[0]-9*yu,yu),(8*yu,4*yu),txt='Update')
        self.detail_plc=esui.Plc(self,(yu,6*yu),(self.Size[0]-2*yu,self.Size[1]/1.5))
        self.detail_plc.SetBackgroundColour('#333333')
        self.updeate_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        return

    def showAroveDetail(self,aroid):
        self.detail_plc.DestroyChildren()
        self.aro=ESC.getAro(aroid)
        DP=self.detail_plc
        yu=gmv.YU
        i=0
        for k,v in self.aro.__dict__.items():
            if k not in ['AroID','AroClass']:
                esui.Stc(DP,(0,i*4*yu),(12*yu,4*yu),k+':',align='left')
                esui.Tcc(DP,(12*yu,i*4*yu),(DP.Size[0]-12*yu,4*yu),hint=v.__str__(),cn=k)
                i+=1
        for ctrl in self.detail_plc.Children:
            ctrl.Refresh()
        return

    def onClkUpdate(self,e):
        arove_dcit=dict()
        for ctrl in self.detail_plc.Children:
            if type(ctrl) is esui.Tcc:
                v=ctrl.GetValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
                arove_dcit[ctrl.Name]=v_eval
        wxmw=self.Parent.Parent     # wxmw.Sidepl.self;
        aropl=wxmw.FindWindowByName('aropl')
        ESC.setArove(self.aro.AroID,arove_dcit)
        aropl.readMap()
        return
    pass

class AcpSideTab(SideTab):
    def __init__(self,parent,p,s,tablabel,cn=''):
        SideTab.__init__(self,parent,p,s,tablabel,cn)
        yu=gmv.YU

        self.model_name=esui.Stc(self,(yu,yu),(8*yu,4*yu),'Model:',align='left')
        self.model_enable_btn=esui.SelectBtn(self,(self.Size[0]-9*yu,yu),(8*yu,4*yu),'Enable',tsize=12)
        self.model_menu=esui.SelectMenuBtn(self,(yu,6*yu),(self.Size[0]-2*yu,4*yu),'Model',[])

        self.updeate_btn=esui.btn(self,(self.Size[0]-9*yu,11*yu),(8*yu,4*yu),txt='Update')
        self.detail_plc=esui.Plc(self,(yu,16*yu),(self.Size[0]-2*yu,self.Size[1]/1.5))

        self.detail_plc.SetBackgroundColour('#333333')
        self.updeate_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        self.model_enable_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
        return

    def showAcpDetail(self,acp):
        self.detail_plc.DestroyChildren()
        self.acp=acp
        DP=self.detail_plc
        yu=gmv.YU
        i=0
        banlist=['AcpID','AcpClass','inport','outport','position','fixIO','port']
        nbanlist=['AcpID','AcpClass','position','fixIO']
        for k,v in acp.__dict__.items():
            if not acp.fixIO: nl=nbanlist
            else:nl=banlist
            if k not in nl:
                esui.Stc(DP,(0,i*4*yu),(12*yu,4*yu),k+':',align='left')
                esui.Tcc(DP,(12*yu,i*4*yu),(DP.Size[0]-12*yu,4*yu),hint=v.__str__(),cn=k)
                i+=1
        'todo:port setting build;'

        for ctrl in self.detail_plc.Children:
            ctrl.Refresh()
        return

    def onClkUpdate(self,e):
        set_dcit=dict()
        for ctrl in self.detail_plc.Children:
            if type(ctrl) is esui.Tcc:
                v=ctrl.GetValue()
                try: v_eval=eval(v)
                except BaseException:v_eval=v
                set_dcit[ctrl.Name]=v_eval
        acppl=self.Parent.acppl_agent
        ESC.setAcp(self.acp.AcpID,set_dcit,acppl.acpmodel)
        acppl.drawAcp()
        return

    def onClkAcpModel(self,e):
        fc=self.model_menu.PopupControl
        acpmodel=fc.items[fc.ipos]
        self.model_menu.SetLabel(acpmodel[0]+'.'+acpmodel[1])
        self.model_enable_btn.SetValue(acpmodel not in ESC.MODEL_DISABLE)
        self.Parent.acppl_agent.drawAcp(acpmodel)
        if e is not None:e.Skip()
        return

    def onClkEnable(self,e):
        fc=self.model_menu.PopupControl
        acpmodel=fc.items[fc.ipos]
        enable_already=self.model_enable_btn.GetValue()
        disable_list=list(ESC.MODEL_DISABLE)
        if enable_already:
            disable_list.append(acpmodel)
        else:
            disable_list.remove(acpmodel)
        ESC.setSim({'MODEL_DISABLE':disable_list})
        e.Skip()
        return
    pass
