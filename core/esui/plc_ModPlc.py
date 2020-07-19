import wx
import mod
from core import ESC
from core import esui
from core import esevt
class ModPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,cn='modpl')
        self.SetBackgroundColour(esui.COLOR_BACK)
        self.tool_dict=dict()
        self.reg_evt_tool_list=list()
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_LBACK))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.esEVT_LOAD_MOD:
            self.loadMod()
        else:
            for tool in self.reg_evt_tool_list:
                esevt.sendEvent(etype,target=tool.ctrl)
        return

    def loadMod(self):
        'Build mod panel with ESC.MOD_LIST;'
        xu=esui.XU
        yu=esui.YU
        self.DestroyChildren()
        for i in range(0,len(ESC.MOD_LIST)):
            esui.TabBtn(self,(i*(6.25*xu+2),0),(6.25*xu,4*yu),
                tablabel=ESC.MOD_LIST[i],
                cn=ESC.MOD_LIST[i]+'btn')
            ModTab(self,(0,4*yu),(75*xu,17*yu-2),
                modlabel=ESC.MOD_LIST[i],
                cn=ESC.MOD_LIST[i]+'tab')
        self.FindWindowByName('AroCorebtn').SetValue(True)
        self.FindWindowByName('AroCoretab').Show()
        return

    def regToolEvent(self,tool):
        if tool not in self.reg_evt_tool_list:
            self.reg_evt_tool_list.append(tool)
        else:
            self.reg_evt_tool_list.remove(tool)
        return
    pass

class ModTab(esui.ScrolledPlc):
    def __init__(self,parent,p,s,modlabel,cn=''):
        super().__init__(parent,p,s,cn,axis='X')
        self.Hide()
        self.SetLabel(modlabel)
        self.SetBackgroundColour(esui.COLOR_BACK)

        # Build tools;
        # self.DestroyChildren()
        TOOL_INDEX=eval('mod.'+modlabel+'.TOOL_INDEX')
        for toolname in TOOL_INDEX:
            tool=eval('mod.'+modlabel+'.'+toolname)
            if tool.host=='MOD_PLC':
                tool.build(self)
        return
    pass
