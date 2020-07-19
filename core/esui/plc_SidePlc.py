# -*- coding: UTF-8 -*-
import wx
from core import ESC
from core import esui
from core import esevt
# from mod.AroCore import AroSpace,AroGroup
class SidePlc(esui.Plc):

    def __init__(self,parent,p,s):
        esui.Plc.__init__(self,parent,p,s,cn='sidepl')
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.Hide()

        self.map_list=list()
        self.model_list=list()
        self.tab_list=['Aro','Arove','Acp']
        self.now_tab=''

        yu=esui.YU
        self.aro_btn=esui.TabBtn(self,(1,0),(s[0]/3,4*yu),'Aro','Aro_btn')
        self.aro_tab=AroTab(self,(2,4*yu),(s[0],92*yu),'Aro','Aro_tab')

        self.arove_btn=esui.TabBtn(self,(1+s[0]/3,0),(s[0]/3,4*yu),'Arove','Arove_btn')
        self.arove_tab=AroveTab(self,(2,4*yu),(s[0],92*yu),'Arove','Arove_tab')

        self.acp_btn=esui.TabBtn(self,(1+2*s[0]/3,0),(s[0]/3,4*yu),'Acp','Acp_btn')
        self.acp_tab=AcpTab(self,(2,4*yu),(s[0],92*yu),'Acp','Acp_tab')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)

        self.aro_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAroTabBtn)
        self.arove_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAroveTabBtn)
        self.acp_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAcpTabBtn)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetPen(wx.Pen(esui.COLOR_BLACK,width=2))
        dc.DrawLine(0,0,0,self.Size.y)
        return

    def loadMaps(self,maps):
        '''Load maps;'''
        self.map_list=maps
        self.aro_tab.map_menu.setItems(maps)
        self.aro_btn.onClk(None)
        self.onClkAroTabBtn(None)
        self.aro_tab.onClkMapMenu(None)
        return

    def loadModels(self,models):
        for model in models:
            if model not in self.model_list:
                self.model_list.append(model)
        self.acp_tab.model_menu.setItems(self.model_list)
        self.acp_tab.onClkModelMenu(None)
        return

    def showArove(self,aroid=None):
        self.onClkAroveTabBtn(None)
        self.arove_btn.onClk(None)
        if aroid is None:aroid=esui.ARO_PLC.aro_selection[0].AroID
        self.arove_tab.showAroveDetail(aroid)
        return

    def showAcpDetail(self,acp):
        self.acp_tab.showAcpDetail(acp)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.esEVT_UPDATE_MAP:
            self.updateAroTree()
        elif etype==esevt.esEVT_RESET_SIM:
            # self.onClkAroTabBtn(None)
            self.updateAroTree()
        return

    def onClkAcpTabBtn(self,e):
        self.now_tab='Acp'
        esui.ARO_PLC.Hide()
        esui.ACP_PLC.Show()
        esui.ACP_PLC.drawConnection()
        if e is not None:e.Skip()
        return
    def onClkAroveTabBtn(self,e=None):
        self.now_tab='Arove'
        esui.ARO_PLC.Show()
        esui.ACP_PLC.Hide()
        if e is not None:e.Skip()
        return
    def onClkAroTabBtn(self,e):
        self.now_tab='Aro'
        esui.ARO_PLC.Show()
        esui.ACP_PLC.Hide()
        if e is not None:e.Skip()
        return

    def updateAroTree(self):
        self.aro_tab.arotree.buildTree()
        return

    pass

class AroTab(esui.Plc):
    def __init__(self,parent,p,s,tablabel,cn):
        super().__init__(parent,p,s,cn)
        yu=esui.YU
        xu=esui.XU
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.map_txt=esui.Stc(self,(yu,yu),(8*yu,4*yu),'Map:',align='left')
        self.map_menu=esui.SelectMenuBtn(self,(8*yu,yu),(self.Size[0]-10*yu,4*yu),'',[])
        self.btn_add_space=esui.btn(self,(25*xu-15*yu,6*yu),(4*yu,4*yu),'+S')
        self.btn_add_group=esui.btn(self,(25*xu-10*yu,6*yu),(4*yu,4*yu),'+G')
        self.btn_filter=esui.MenuBtn(self,(25*xu-5*yu,6*yu),(4*yu,4*yu),'Flr',['None','Space','Group'])
        # self.arotree=esui.ListBox(self,(yu,11*yu),(self.Size[0]-2*yu,50*yu))
        self.arotree=esui.AroTreePlc(self,(yu,11*yu),(self.Size[0]-2*yu,50*yu))

        self.map_menu.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMapMenu)
        return

    def onClkMapMenu(self,e):
        fc=self.map_menu.PopupControl
        aromap=fc.items[fc.ipos]
        self.map_menu.SetLabel(aromap)
        self.map_menu.Refresh()
        ESC.loadMapFile(aromap)
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_UPDATE_MAP)
        if e is not None:e.Skip()
        return
    pass

class AroveTab(esui.Plc):
    def __init__(self,parent,p,s,tablabel,cn):
        super().__init__(parent,p,s,cn)
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.hidden_list=[]
        # self.hidden_list=['AroID','AroClass','parent','children']
        yu=esui.YU
        self.updeate_btn=esui.btn(self,(self.Size[0]-9*yu,yu),(8*yu,4*yu),txt='Update')
        self.detail_plc=esui.Plc(self,(yu,6*yu),(self.Size[0]-2*yu,self.Size[1]/1.5))
        self.detail_plc.SetBackgroundColour(esui.COLOR_LBACK)
        self.updeate_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        return

    def showAroveDetail(self,aroid):
        self.detail_plc.DestroyChildren()
        self.aro=ESC.getAro(aroid)
        DP=self.detail_plc
        yu=esui.YU
        i=0
        'todo: better arove detail;'
        for k,v in self.aro.__dict__.items():
            if k not in self.hidden_list:
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
        ESC.setAro(self.aro.AroID,arove_dcit)
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_UPDATE_MAP)
        return
    pass

class AcpTab(esui.Plc):
    def __init__(self,parent,p,s,tablabel,cn):
        super().__init__(parent,p,s,cn)
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.hidden_list=['AcpID','AcpClass','inport','outport','position','fixIO','port']
        self.acp=None
        self.add_in_btn=None
        self.add_out_btn=None

        yu=esui.YU
        self.model_name=esui.Stc(self,(yu,yu),(8*yu,4*yu),'Model:',align='left')
        self.enable_btn=esui.SelectBtn(self,(self.Size[0]-18*yu,yu),(8*yu,4*yu),'Enable')
        self.updeate_btn=esui.btn(self,(self.Size[0]-9*yu,yu),(8*yu,4*yu),'Update')
        self.model_menu=esui.SelectMenuBtn(self,(yu,6*yu),(self.Size[0]-2*yu,4*yu),'Model',[])
        self.detail_plc=esui.ScrolledPlc(self,(yu,11*yu),(self.Size[0]-2*yu,self.Size[1]/1.5))

        self.updeate_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        self.enable_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
        self.model_menu.PopupControl.lctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkModelMenu)
        return

    def showAcpDetail(self,acp):
        self.detail_plc.DestroyChildren()
        self.acp=acp
        DP=self.detail_plc
        yu=esui.YU

        esui.Stc(DP,(yu,0),(8*yu,4*yu),'General:',align='left')
        i=1
        for k,v in acp.__dict__.items():
            if k not in self.hidden_list:
                # last_ctrl=
                esui.Stc(DP,(2*yu,i*4*yu),(10*yu,4*yu),k+':',align='left')
                esui.Tcc(DP,(12*yu,i*4*yu),(DP.Size[0]-13*yu,4*yu),hint=v.__str__(),cn=k)
                i+=1

        esui.Stc(DP,(yu,i*4*yu),(8*yu,4*yu),'IO Ports:',align='left')
        self.add_in_btn=esui.btn(DP,(DP.Size[0]-8*yu,i*4*yu+0.5*yu),(3*yu,3*yu),'+I')
        self.add_out_btn=esui.btn(DP,(DP.Size[0]-4*yu,i*4*yu+0.5*yu),(3*yu,3*yu),'+O')
        self.add_in_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAddInBtn)
        self.add_out_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkAddOutBtn)
        if acp.fixIO=='In':
            self.add_in_btn.Hide()
        elif acp.fixIO=='Out':
            self.add_out_btn.Hide()
        elif acp.fixIO=='Both':
            self.add_in_btn.Hide()
            self.add_out_btn.Hide()

        i+=1
        for pid,pname in acp.port.items():
            if pid in acp.inport:
                # last_ctrl=
                esui.Stc(DP,(2*yu,i*4*yu),(10*yu,4*yu),'>>'+pname+':',align='left')
            else:
                # last_ctrl=
                esui.Stc(DP,(2*yu,i*4*yu),(10*yu,4*yu),'<<'+pname+':',align='left')
            esui.btn(DP,(DP.Size[0]-4*yu,i*4*yu+yu),(2*yu,2*yu),'x')
            i+=1
        DP.updateVirtualSize()
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
        ESC.setAcp(self.acp.AcpID,set_dcit,esui.ACP_PLC.acpmodel)
        esui.ACP_PLC.drawAcp()
        return

    def onClkModelMenu(self,e):
        fc=self.model_menu.PopupControl
        acpmodel=fc.items[fc.ipos]
        self.model_menu.SetLabel(acpmodel[0]+'.'+acpmodel[1])
        self.enable_btn.SetValue(acpmodel not in ESC.MODEL_DISABLE)
        esui.ACP_PLC.drawAcp(acpmodel)
        if e is not None:e.Skip()
        return

    def onClkEnable(self,e):
        fc=self.model_menu.PopupControl
        acpmodel=fc.items[fc.ipos]
        enable_already=self.enable_btn.GetValue()
        disable_list=list(ESC.MODEL_DISABLE)
        if enable_already:
            disable_list.append(acpmodel)
        else:
            disable_list.remove(acpmodel)
        ESC.setSim({'MODEL_DISABLE':disable_list})
        e.Skip()
        return

    def onClkAddInBtn(self,e):
        inport=dict(self.acp.inport)
        port=dict(self.acp.port)
        maxid=max(inport.keys())+1
        inport.update({maxid:None})
        port.update({maxid:'in P'})
        ESC.setAcp(self.acp,{'inport':inport,'port':port},esui.ACP_PLC.acpmodel)
        self.showAcpDetail(self.acp)
        return

    def onClkAddOutBtn(self,e):
        'todo: add outport'
        return
    pass
