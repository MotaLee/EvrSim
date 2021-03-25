# -*- coding: UTF-8 -*-
# App variable;
ES_EDITOR_TITLE='EvrSim Editor'
# Outer libs;
import wx
# EvrSim libs;
import EvrSim
from core import esui,esgl,estl
xu=esui.XU
yu=esui.YU
UMR=esui.UMR
# Editor main window;
class EvrSimEditor(esui.EsWindow):
    def __init__(self,**argkw):
        super().__init__(title=ES_EDITOR_TITLE)
        UMR.bindIndex(self,'ESMW')
        UMR.HEAD_DIV=estl.HeadDiv(self)
        UMR.TOOL_DIV=estl.ToolDiv(self,style={'p':(0,4*yu),'s':(75*xu,21*yu)})
        UMR.CMD_DIV=estl.CmdDiv(self,style={'p':(0,4*yu),'s':(75*xu,21*yu)})
        UMR.MAP_DIV=esgl.GLDiv(self,(0,25*yu),(75*xu,75*yu))
        estl.AroToolbar()
        UMR.MDL_DIV=estl.MdlDiv(self,style={'p':(0,25*yu),'s':(75*xu,75*yu)})
        UMR.SIDE_DIV=estl.SideDiv(self,style={'p':(75*xu,4*yu),'s':(25*xu,96*yu)})
        WelDiv(self,style={'p':(self.Size.x/2-360,self.Size.y/2-225),'s':(720,450)})
        self.Show()
        return
    pass

class WelDiv(esui.Div):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        img_splash=esui.UMR.getImg(path='res/img/splash.png')
        self.splash=wx.StaticBitmap(self,bitmap=img_splash)
        self.weltt=esui.TransText(self,label=ES_EDITOR_TITLE,style={'p':(0,30*yu),'s':(10*xu,4*yu)})
        self.vertt=esui.TransText(self,label=EvrSim.EDITOR_VER,style={'p':(10*yu,30*yu),'s':(10*xu,4*yu)})
        esui.TransText(self,label='EvrSim ver',style={'p':(0,35*yu),'s':(10*xu,4*yu)})
        esui.TransText(self,label=EvrSim.ES_VER,style={'p':(10*yu,35*yu),'s':(10*xu,4*yu)})

        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        return

    def onComEvt(self,e):
        etype=e.getEventArgs()
        if etype==esui.ETYPE_OPEN_SIM:
            self.Hide()
        elif etype==esui.ETYPE_CLOSE_SIM:
            self.Show()
        return
    pass
