# -*- coding: UTF-8 -*-
import wx
from core import ESC
from core import esui
from core import esevt

class SidePlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.Hide()

        self.map_list=list()
        self.model_list=list()
        self.tab_list=['Manager','Detail']

        yu=esui.YU
        tab_pos=(2,8*yu)
        tab_size=(s[0],88*yu)
        self.workspace_btn=esui.Btn(self,(1,0),(4*yu,4*yu),'<->',tip='Toggle Aro/Acp')
        self.manager_btn=esui.TabBtn(self,(1,4*yu),(8*yu,4*yu),'Manager')
        self.manager_tab=ManagerTab(self,tab_pos,tab_size,'Manager')

        self.detail_btn=esui.TabBtn(self,(8*yu,4*yu),(8*yu,4*yu),'Detail')
        self.detail_tab=DetailTab(self,tab_pos,tab_size,'Detail')

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)

        self.workspace_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkWorkspace)

        self.updateAroTree=self.manager_tab.map_block.map_tree.buildTree
        self.showDetail=self.detail_tab.showDetail
        self.clearDetail=self.detail_tab.clearDetail
        self.Hide()
        return

    def loadMaps(self,maps=None):
        '''Load maps;'''
        if maps is None:
            maps=list(ESC.MAP_LIST)
        self.map_list=maps
        self.manager_tab.map_block.map_menu.setItems(maps)
        self.manager_tab.map_block.onClkMapMenu(None)
        self.toggleTab('Manager')
        return

    def loadModels(self,models=None):
        if models is None:
            models=list(ESC.ACP_MODELS.keys())
        for model in models:
            if model not in self.model_list:
                self.model_list.append(model)
        self.manager_tab.model_block.model_tree.buildTree()
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_UPDATE_MAP:
            self.updateAroTree()
        elif etype==esevt.ETYPE_RESET_SIM:
            self.updateAroTree()
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.loadMaps()
            self.loadModels()
            self.Show()
        return

    def onClkWorkspace(self,e=None,call=None):
        status=esui.ARO_PLC.IsShown()
        if status or call=='ACP_PLC':
            esui.ARO_PLC.Hide()
            esui.ACP_PLC.Show()
            esui.ACP_PLC.drawConnection()
        elif not status or call=='ARO_PLC':
            esui.ARO_PLC.Show()
            esui.ACP_PLC.Hide()
        if e is not None and call is None:e.Skip()
        return

    def toggleTab(self,tablabel='Manager'):
        for ctrl in self.Children:
            if type(ctrl)==esui.TabBtn and tablabel==ctrl.Label:
                ctrl.onClk(None)
        return

    def getTab(self,tablabel):
        for ctrl in self.Children:
            if ctrl.GetLabel()==tablabel and isinstance(ctrl,esui.Plc):
                return ctrl
        i=len(self.tab_list)
        yu=esui.YU
        btn=esui.TabBtn(self,(8*yu*i,4*yu),(8*yu,4*yu),tablabel)
        tab=esui.ScrolledPlc(self,(0,8*yu),(self.Size.x,self.Size.y-8*yu),tablabel)
        self.tab_list.append(tablabel)
        btn.onClk(None)
        return tab

    def delTab(self,tablabel):
        for ctrl in self.Children:
            if ctrl.GetLabel()==tablabel:
                ctrl.DestroyLater()
        return
    pass

class ManagerTab(esui.ScrolledPlc):
    def __init__(self,parent,p,s,tablabel):
        super().__init__(parent,p,s)
        yu=esui.YU

        self.ori_s=s
        self.SetLabel(tablabel)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.box_sizer=wx.BoxSizer(wx.VERTICAL)
        self.map_block=MapBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,48*yu))
        self.model_block=ModelBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,48*yu))

        self.updateSizer()
        return

    def updateSizer(self):
        new_sizer=wx.BoxSizer(wx.VERTICAL)
        for child in self.Children:
            self.box_sizer.Detach(child)
            new_sizer.Add(child,0,wx.ALL | wx.FIXED_MINSIZE,border=esui.YU)
        self.box_sizer=new_sizer
        self.SetSizerAndFit(self.box_sizer)

        self.updateVirtualSize()
        self.SetSize(self.ori_s)
        return

    def onClkFold(self,e):
        block=e.EventObject.Parent
        if block.folded:
            block.folded=False
            block.SetSize(self.Size[0],48*esui.YU)
        else:
            block.folded=True
            block.SetSize(self.Size[0],4*esui.YU)
        self.updateSizer()
        return
    pass

class MapBlock(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        yu=esui.YU
        self.folded=False

        self.map_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),'Map:',align='left')
        self.btn_fold=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'v')

        self.map_menu=esui.SelectMenuBtn(self,(0,5*yu),(24*yu,4*yu),'',[])
        self.btn_add_space=esui.Btn(self,(self.Size[0]-14*yu,5*yu),(4*yu,4*yu),'Spc')
        self.btn_add_group=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Grp')
        self.btn_filter=esui.MenuBtn(self,
            (self.Size[0]-4*yu,5*yu),(4*yu,4*yu),
            'Flr',['None','Space','Group'])

        self.map_tree=esui.MapTreePlc(self,(0,10*yu),(self.Size[0],38*yu))

        self.btn_fold.Bind(wx.EVT_LEFT_DOWN,self.Parent.onClkFold)
        self.map_menu.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMapMenu)
        return

    def onClkMapMenu(self,e):
        fc=self.map_menu.PopupControl
        aromap=fc.items[fc.ipos]
        self.map_menu.SetLabel(aromap)
        self.map_menu.Refresh()
        ESC.loadMapFile(aromap)
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,esevt.ETYPE_UPDATE_MAP)
        if e is not None:e.Skip()
        return
    pass

class ModelBlock(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        yu=esui.YU
        self.folded=False
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.model_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),'Model:',align='left')
        self.btn_fold=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'v')
        self.enable_btn=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Ena')
        self.del_btn=esui.Btn(self,(self.Size[0]-4*yu,5*yu),(4*yu,4*yu),'Del')
        self.model_tree=esui.ModelTreePlc(self,(0,10*yu),(self.Size[0],38*yu))
        # self.del_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        self.enable_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
        self.btn_fold.Bind(wx.EVT_LEFT_DOWN,self.Parent.onClkFold)
        return

    def onClkEnable(self,e):
        acpmodel=None
        for ti_plc in self.model_tree.Children:
            item=ti_plc.item
            if item.is_selected and item.depth!=0:
                acpmodel=(item.parent,item.label)
                enable_already=item.ena
                item.ena= not item.ena
                break
        if acpmodel is None:return
        disable_list=list(ESC.MODEL_DISABLE)
        if enable_already:
            disable_list.append(acpmodel)
        else:
            disable_list.remove(acpmodel)
        ESC.setSim({'MODEL_DISABLE':disable_list})
        self.model_tree.drawTree()
        e.Skip()
        return

    pass

class ModBlock(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        yu=esui.YU
        self.folded=False
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.model_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),'Model:',align='left')
        self.btn_fold=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'v')
        self.enable_btn=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Ena')
        self.del_btn=esui.Btn(self,(self.Size[0]-4*yu,5*yu),(4*yu,4*yu),'Del')
        self.model_tree=esui.ModelTreePlc(self,(0,10*yu),(self.Size[0],38*yu))
        # self.del_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkUpdate)
        self.enable_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
        self.btn_fold.Bind(wx.EVT_LEFT_DOWN,self.Parent.onClkFold)
        return
    pass

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
        self.confirm_btn=esui.Btn(self,(self.Size[0]-5*yu,yu),(4*yu,4*yu),txt='√')
        self.detail_plc=esui.ScrolledPlc(self,(0,6*yu),(self.Size[0],self.Size[1]-6*yu))
        self.detail_plc.SetBackgroundColour(esui.COLOR_LBACK)
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
        yu=esui.YU
        esui.HintText(self,(self.Size[0]-14*yu,yu),(8*yu,4*yu),txt='Updated!')
        return

    def showDetail(self,aobj=None,mode='Aro'):
        yu=esui.YU
        DP=self.detail_plc
        DP.Hide()
        DP.DestroyChildren()
        self.mode=mode
        esui.SIDE_PLC.toggleTab('Detail')
        if mode=='Aro':
            if aobj is None:aro=esui.ARO_PLC.aro_selection[0]
            elif type(aobj)==int:aro=ESC.getAro(aobj)
            else: aro=aobj
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
        elif mode=='Acp':
            'todo:get acp by acpid'
            if type(aobj)==int:acp=ESC.getAcp(aobj)
            else:acp=aobj
            self.aobj=acp
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
                    esui.SelectBtn(DP,(14*yu,(i*4+0.5)*yu),(3*yu,3*yu),cn=k,select=v)
                else:
                    esui.InputText(DP,(14*yu,(i*4+0.5)*yu),(DP.Size[0]-15*yu,3.5*yu),hint=str(v),cn=k,exstl=stl)
                i+=1
            esui.StaticText(DP,(yu,i*4*yu),(8*yu,4*yu),'IO Ports:',align='left')
            self.add_in_btn=esui.Btn(DP,(DP.Size[0]-9*yu,(i*4+0.5)*yu),(3*yu,3*yu),'+I')
            self.add_out_btn=esui.Btn(DP,(DP.Size[0]-5*yu,(i*4+0.5)*yu),(3*yu,3*yu),'+O')
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
                    esui.StaticText(DP,(3*yu,i*4*yu),(10*yu,4*yu),'>>'+pname+':',align='left')
                else:
                    # last_ctrl=
                    esui.StaticText(DP,(3*yu,i*4*yu),(10*yu,4*yu),'<<'+pname+':',align='left')
                esui.Btn(DP,(DP.Size[0]-5*yu,i*4*yu+yu),(2*yu,2*yu),'×')
                i+=1
            DP.updateVirtualSize()
        for ctrl in self.detail_plc.Children:
            ctrl.Refresh()
        DP.Show()
        return

    def clearDetail(self):
        self.detail_plc.DestroyChildren()
        return

    def onClkAddInBtn(self,e):
        inport=dict(self.aobj.inport)
        port=dict(self.aobj.port)
        maxid=max(inport.keys())+1
        inport.update({maxid:None})
        port.update({maxid:'in P'})
        ESC.setAcp(self.aobj,{'inport':inport,'port':port},esui.ACP_PLC.model_tuple)
        self.showDetail(self.aobj,mode='Acp')
        return

    def onClkAddOutBtn(self,e):
        'todo: add outport'
        return
    pass
