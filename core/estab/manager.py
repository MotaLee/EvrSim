import wx
from core import ESC,esui,esevt
yu=esui.YU
class ManagerTab(esui.ScrolledPlc):
    def __init__(self,parent,p,s,tablabel):
        super().__init__(parent,p,s)

        self.ori_s=s
        self.SetLabel(tablabel)

        self.box_sizer=wx.BoxSizer(wx.VERTICAL)
        self.map_block=MapBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,49*yu))
        self.model_block=ModelBlock(self,wx.DefaultPosition,(self.Size[0]-2*yu,49*yu))

        self.updateSizer()
        return

    def updateSizer(self):
        new_sizer=wx.BoxSizer(wx.VERTICAL)
        for child in self.Children:
            self.box_sizer.Detach(child)
            new_sizer.Add(child,0,wx.ALL | wx.FIXED_MINSIZE,border=yu)
        self.box_sizer=new_sizer
        self.SetSizerAndFit(self.box_sizer)

        self.updateVirtualSize()
        self.SetSize(self.ori_s)
        for child in self.Children:
            if not child.folded:
                child.SetSize(child.ori_s)
        return

    def onClkFold(self,e):
        block=e.EventObject.Parent
        if block.folded:
            e.EventObject.SetLabel('^')
            block.folded=False
            block.SetSize(self.Size[0],49*yu)
        else:
            e.EventObject.SetLabel('v')
            block.folded=True
            block.SetSize(self.Size[0],5*yu)
        self.updateSizer()
        return
    pass

class MapBlock(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,border={'bottom':esui.COLOR_ACTIVE})
        self.folded=False
        self.ori_s=s
        self.map_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),'Map:',align='left')
        self.btn_fold=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'^')

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
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        if e is not None:e.Skip()
        return
    pass

class ModelBlock(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,border={'bottom':esui.COLOR_ACTIVE})
        self.ori_s=s
        self.folded=False
        self.model_txt=esui.StaticText(self,(0,0),(8*yu,4*yu),'Model:',align='left')
        self.btn_fold=esui.Btn(self,(self.Size[0]-4*yu,0),(4*yu,4*yu),'^')
        self.enable_btn=esui.Btn(self,(self.Size[0]-9*yu,5*yu),(4*yu,4*yu),'Ena')
        self.del_btn=esui.Btn(self,(self.Size[0]-4*yu,5*yu),(4*yu,4*yu),'Del')
        self.model_tree=esui.ModelTreePlc(self,(0,10*yu),(self.Size[0],38*yu))
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
