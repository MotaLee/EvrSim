# -*- coding: UTF-8 -*-
# App variable;
EDITOR_VER='0.0.13'
ES_EDITOR_TITLE='EvrSim Editor'
# Outer libs;
import wx
# EvrSim libs;
import EvrSim
from core import ESC,esui,esevt,esgl,estl
xu=esui.XU
yu=esui.YU
IDX=esui.IDX
# Editor main window;
class EvrSimEditor(esui.EsWindow):
    def __init__(self,**argkw):
        super().__init__(title=ES_EDITOR_TITLE)
        IDX.bindIndex(self,'ESMW')
        IDX.HEAD_DIV=esui.HeadPlc(self)
        IDX.TOOL_DIV=estl.ToolDiv(self,style={'p':(0,4*yu),'s':(75*xu,21*yu)})
        IDX.CMD_DIV=esui.CmdPlc(self,(0,4*yu),(75*xu,21*yu))
        IDX.MAP_DIV=esgl.AroGlc(self,(0,25*yu),(75*xu,75*yu))
        estl.AroToolbar()
        IDX.MDL_DIV=estl.MdlDiv(self,style={'p':(0,25*yu),'s':(75*xu,75*yu)})
        IDX.SIDE_DIV=estl.SideDiv(self,style={'p':(75*xu,4*yu),'s':(25*xu,96*yu)})
        self.wel_plc=WelPlc(self,(self.Size.x/2-360,self.Size.y/2-225),(720,450))
        self.Show()
        return
    pass

class WelPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        self.weltt=esui.TransText(self,(0,30*yu),(10*xu,4*yu),ES_EDITOR_TITLE)
        self.vertt=esui.TransText(self,(10*yu,30*yu),(10*xu,4*yu),EDITOR_VER)
        esui.TransText(self,(0,35*yu),(10*xu,4*yu),'EvrSim ver:')
        esui.TransText(self,(10*yu,35*yu),(10*xu,4*yu),EvrSim.ES_VER)
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
