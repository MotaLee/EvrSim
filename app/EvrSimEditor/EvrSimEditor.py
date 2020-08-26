# -*- coding: UTF-8 -*-
# App variable;
ESWX_VER='0.0.5'
ES_EDITOR_TITLE='EvrSimEditor'
# Outer libs;
import sys
import os
import wx
sys.path.append(os.getcwd())
# EvrSim libs;
from core import ESC
from core import esui
from core import esevt
from core import esgl
from core import estool
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
        esui.ACP_PLC=esui.AcpPlc(self,(0,25*yu),(75*xu,75*yu))
        esui.SIDE_PLC=esui.SidePlc(self,(75*xu,4*yu),(25*xu,96*yu))
        self.wel_plc=WelPlc(self,(0,4*yu),(100*xu,96*yu))

        self.Show()
        return
    pass

class WelPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.weltt=esui.TransText(self,(0,15*yu),(100*xu,10*yu),
            'E v r S i m  E d i t o r',tsize=int(4*yu))
        self.vertt=esui.TransText(self,(0,25*yu),(100*xu,4*yu),
            ESWX_VER,tsize=int(2*yu))
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
