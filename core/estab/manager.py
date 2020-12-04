import wx
from core import ESC,esui,esevt
yu=esui.YU
class ManagerTab(esui.ScrolledPlc):
    def __init__(self,parent,p,s,tablabel):
        super().__init__(parent,p,s)
        self.ori_s=s
        self.SetLabel(tablabel)

        self.sim_block=SimBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,49*yu))
        self.map_block=MapBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,49*yu))
        self.model_block=ModelBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,49*yu))

        self.updateSizer()
        return

    def updateSizer(self):
        total_height=0
        for child in self.Children:
            child.SetPosition((yu,yu+total_height))
            total_height+=child.Size.y
        self.updateVirtualSize()
        self.SetSize(self.ori_s)
        return

    pass

class MngrBlock(esui.Plc):
    def __init__(self,parent,p,s,name):
        super().__init__(parent,p,s,border={'bottom':esui.COLOR_ACTIVE})
        self.folded=False
        self.ori_s=s
        self.map_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),name+':',align='left')
        self.btn_fold=esui.Btn(self,(self.Parent.Size[0]-6*yu,0),(4*yu,4*yu),'^')
        self.btn_fold.Bind(wx.EVT_LEFT_DOWN,self.onClkFold)
        return

    def onClkFold(self,e):
        if self.folded:
            self.btn_fold.SetLabel('^')
            self.folded=False
            self.SetSize(self.Parent.Size[0],49*yu)
        else:
            self.btn_fold.SetLabel('v')
            self.folded=True
            self.SetSize(self.Size[0],5*yu)
        self.Parent.updateSizer()
        return
    pass

class SimBlock(MngrBlock):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'Sim')
        self.sim_tree=esui.SimTreePlc(self,(0,5*yu),(self.Size[0],38*yu))
        # self.folded=True
        self.onClkFold(None)
        return
    pass

class MapBlock(MngrBlock):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'map')
        self.map_menu=esui.SelectMenuBtn(self,(0,5*yu),(24*yu,4*yu),'',[])
        self.btn_add_space=esui.Btn(self,(self.Size[0]-14*yu,5*yu),(4*yu,4*yu),'Spc')
        self.btn_add_group=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Grp')
        self.btn_filter=esui.MenuBtn(self,
            (self.Size[0]-4*yu,5*yu),(4*yu,4*yu),
            'Flr',['None','Space','Group'])

        self.map_tree=esui.MapTreePlc(self,(0,10*yu),(self.Size[0],38*yu))
        self.map_menu.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkMapMenu)
        return

    def onClkMapMenu(self,e):
        fc=self.map_menu.PopupControl
        aromap=fc.items[fc.ipos]
        self.map_menu.SetLabel(aromap)
        self.map_menu.Refresh()
        ESC.loadMapFile(aromap)
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        if e is not None:e.Skip()
        return
    pass

class ModelBlock(MngrBlock):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'Model')
        self.enable_btn=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Ena')
        self.del_btn=esui.Btn(self,(self.Size[0]-4*yu,5*yu),(4*yu,4*yu),'Del')
        self.model_tree=esui.ModelTreePlc(self,(0,10*yu),(self.Size[0],38*yu))
        self.enable_btn.Bind(wx.EVT_LEFT_DOWN,self.onClkEnable)
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
        self.model_tree.DestroyChildren()
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
