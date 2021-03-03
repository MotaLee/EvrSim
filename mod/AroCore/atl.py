import time
import wx
import _glm as glm
import numpy as np
from core import ESC,esui,esgl,esevt,estl
import mod
yu=esui.YU

# Other reliabilities;
# class ALibsTreePlc(esui.TreePlc):
#     def buildTree(self):
#         self.item_list=list()
#         for modname in ESC.MOD_TREE_DICT.keys():
#             aroci=eval('mod.'+modname+'.ARO_INDEX')
#             acpci=eval('mod.'+modname+'.ACP_INDEX')
#             ti=self.tree_item(modname,children=aroci+acpci)
#             self.item_list.append(ti)
#             for aitem in aroci+acpci:
#                 ti=self.tree_item(aitem,depth=1,parent=modname)
#                 self.item_list.append(ti)
#         self.drawTree()
#         return
#     pass
# Tool class defination;
class AroMenu(estl.CreateMenuTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,parent,p,s,label,items):
        super().__init__(name,parent,p,s,label,items)
        self.mod_name=self.Parent.Label
        self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.HidePopup()
        aroclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        aro=ESC.addAro(aroclass)
        ESC.setAro(aro.AroID,{'AroName':'New Aro'})
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        return
    pass

class AcpMenu(estl.CreateMenuTool):
    'Lv:3: Thrid tool class. Bind event;'
    def __init__(self,name,parent,p,s,label,items):
        super().__init__(name,parent,p,s,label,items)
        self.mod_name=self.Parent.Label
        self.pop_ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkPopup)
        return

    def onClkPopup(self,e):
        self.HidePopup()
        acpclass='mod.'+self.mod_name+'.'+self.items[self.popup.ipos]
        esui.IDX.MDL_DIV.addAcpNode(acpclass)
        return
    pass

class RunSimBtn(estl.ToggleTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        esevt.sendEvent(esevt.ETYPE_RUN_SIM,target=esui.IDX.ESMW)
        time_txt=estl.getToolByName('time_txt','AroCore')
        real_time=estl.getToolByName('real_time','AroCore')
        if time_txt is not None:
            if time_txt.timer.IsRunning():
                time_txt.timer.Stop()
            else:
                time_txt.timer.Start(int(1000*ESC.len_timestep))
        if real_time is not None:
            if real_time.timer.IsRunning():
                real_time.timer.Stop()
            else:
                real_time.start=time.time()
                real_time.timer.Start(int(1000*ESC.len_timestep))
        return
    pass

class ResetMapBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        time_txt=estl.getToolByName('time_txt','AroCore')
        real_time=estl.getToolByName('real_time','AroCore')

        if time_txt is not None:
            time_txt.clearTimer()
        if real_time is not None:
            real_time.clearTimer()
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_RESET_SIM)
        return
    pass

class SimTimeText(estl.TextTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.timestamp=0.0
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        return

    def onTimer(self,e):
        if ESC.CORE_STATUS.isStop():
            self.timer.Stop()
            estl.getToolByName('run_btn','AroCore').SetValue(False)
            return
        if self.timer.IsRunning():
            self.timestamp+=ESC.len_timestep*ESC.TIME_RATE
            m=int(self.timestamp/60)
            s=int(self.timestamp) % 60
            ms=int((self.timestamp-int(self.timestamp))*60)
            if m<10:m='0'+str(m)
            else: m=str(m)
            if s<10:s='0'+str(s)
            else: s=str(s)
            if ms<10:ms='0'+str(ms)
            else: ms=str(ms)
            self.SetLabel(m+':'+s+':'+ms)
            self.Refresh()
        return

    def clearTimer(self):
        self.timestamp=0
        self.SetLabel('00:00:00')
        self.Refresh()
        return
    pass

class RealTimeText(estl.TextTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.timestamp=0.0
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTimer,self.timer)
        self.start=0
        return

    def onTimer(self,e):
        if ESC.CORE_STATUS.isStop():
            self.timer.Stop()
            return
        if self.timer.IsRunning():
            self.timestamp=time.time()-self.start
            m=int(self.timestamp/60)
            s=int(self.timestamp) % 60
            ms=int((self.timestamp-int(self.timestamp))*60)
            if m<10:m='0'+str(m)
            else: m=str(m)
            if s<10:s='0'+str(s)
            else: s=str(s)
            if ms<10:ms='0'+str(ms)
            else: ms=str(ms)
            self.SetLabel(m+':'+s+':'+ms)
            self.Refresh()
        return

    def clearTimer(self):
        self.timestamp=0
        self.start=0
        self.SetLabel('00:00:00')
        self.Refresh()
        return
    pass

class ALibsBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)
        self.show_lib=False
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        if self.show_lib:return
        else:self.show_lib=True
        self.tab=esui.IDX.SIDE_DIV.getTab('ALibs')
        # self.tab.SetBackgroundColour(esui.COLOR_LBACK)
        tx=self.tab.Size.x
        ty=self.tab.Size.y
        self.tab.txt_alibs=esui.StaticText(self.tab,(yu,yu),(8*yu,4*yu),'ALibs:',align='left')
        self.tab.btn_add=esui.Btn(self.tab,(tx-5*yu,yu),(4*yu,4*yu),'+')
        self.tab.input_search=esui.InputText(self.tab,(yu,6*yu),(tx-11*yu,4*yu))
        self.tab.btn_search=esui.Btn(self.tab,(tx-9*yu,6*yu),(8*yu,4*yu),'Search')
        self.tab.tree=ALibsTreePlc(self.tab,(yu,11*yu),(tx-2*yu,50*yu))
        self.tab.tree.buildTree()
        self.tab.Show()
        self.tab.btn_add.Bind(wx.EVT_LEFT_DOWN,self.onClkAdd)
        return

    def onClkAdd(self,e):
        ti_list=self.tab.tree.getSelection()
        if len(ti_list)==0:return
        ti=ti_list[0]
        classname=ti.parent+'.'+ti.label
        try:aroci=eval('mod.'+ti.parent+'.ARO_INDEX')
        except BaseException:return
        if ti.Label in aroci:
            aro=ESC.addAro(classname)
            ESC.setAro(aro.AroID,{'AroName':'New Aro'})
            esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_UPDATE_MAP)
        else:esui.IDX.MDL_DIV.addAcpNode(classname)
        return
    pass

class WrkSpcBtn(estl.ButtonTool):
    def __init__(self,name,parent,p,s,label):
        super().__init__(name,parent,p,s,label)

        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def onClk(self,e):
        esui.toggleWorkspace()
        return
    pass
