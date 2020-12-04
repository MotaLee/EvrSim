# -*- coding: UTF-8 -*-
# App variable;
EDITOR_VER='0.0.9'
ES_EDITOR_TITLE='EvrSimEditor'
# Outer libs;
import sys
import os
import wx
sys.path.append(os.getcwd())
# EvrSim libs;
from core import ESC
from core import esui
from core import esevt,esmdl,esgl,estool,estab
xu=esui.XU
yu=esui.YU
# Editor main window;
class EvrSimEditor(esui.EsWindow):
    def __init__(self):
        super().__init__(title=ES_EDITOR_TITLE)
        esui.WXMW=self
        esui.HEAD_PLC=esui.HeadPlc(self)
        esui.TOOL_PLC=estool.ToolPlc(self,(0,4*yu),(75*xu,21*yu))
        esui.CMD_PLC=esui.CmdPlc(self,(0,4*yu),(75*xu,21*yu))
        esui.ARO_PLC=esgl.AroGlc(self,(0,25*yu),(75*xu,75*yu))
        esui.ACP_PLC=esmdl.AcpPlc(self,(0,25*yu),(75*xu,75*yu))
        esui.SIDE_PLC=estab.SidePlc(self,(75*xu,4*yu),(25*xu,96*yu))
        self.wel_plc=WelPlc(self,(self.Size.x/2-360,self.Size.y/2-225),(720,450))

        self.Show()
        return
    pass

class WelPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.weltt=esui.TransText(self,(0,30*yu),(20*xu,4*yu),
            'EvrSim Editor')
        self.vertt=esui.TransText(self,(0,35*yu),(20*xu,4*yu),
            EDITOR_VER)
        img=wx.Image('res/img/splash.png',type=wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.bg=wx.StaticBitmap(self,bitmap=img)
        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_OPEN_SIM:
            self.Hide()
        elif etype==esevt.ETYPE_CLOSE_SIM:
            self.Show()
        return
    pass

# Main enterance;
wxmw=EvrSimEditor()
esui.WXAPP.MainLoop()
