import wx
import mod
from core import ESC
from core import esui
from core import esevt
class ToolPlc(esui.Plc):
    def __init__(self,parent,p,s,single=''):
        super().__init__(parent,p,s)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.tab_list=list()
        self.tool_list=list()
        self.single_mode=single
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Hide()
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        bg=self.GetBackgroundColour()
        dc.SetBrush(wx.Brush(bg))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_OPEN_CMD:
            self.Hide()
        elif etype==esevt.ETYPE_CLOSE_CMD:
            self.Show()
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.Show()
        # else:
        for tool in self.tool_list:
            esevt.sendEvent(etype,target=tool)
        return

    def regToolEvent(self,tool):
        if tool not in self.tool_list:
            self.tool_list.append(tool)
            tool.SetExtraStyle(wx.WS_EX_BLOCK_EVENTS)
        else:
            self.tool_list.remove(tool)
        return

    def getModTab(self,modname):
        ''' Get the tab generated by Tool panel'''
        tab=self.FindWindowByName(modname+'Tab')
        if tab is None:
            self.tab_list.append(modname)
            i=len(self.tab_list)-1
            yu=esui.YU
            xu=esui.XU
            if self.single_mode=='':
                btn=esui.TabBtn(self,(i*8*yu,0),(8*yu,4*yu),tablabel=modname,cn=modname+'Btn')
                tab=ModTab(self,(0,4*yu),(self.Size.x,17*yu-2),label=modname,cn=modname+'Tab')
                btn.onClk(None)
            elif modname==self.single_mode:tab=self
        return tab
    pass

class ModTab(esui.ScrolledPlc):
    def __init__(self,parent,p,s,label,cn=''):
        super().__init__(parent,p,s,cn=cn,axis='X')
        self.Hide()
        self.SetLabel(label)
        self.SetBackgroundColour(esui.COLOR_BACK)
    pass
