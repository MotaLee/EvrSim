# -*- coding: UTF-8 -*-
# App variable;
STS_VER='0.0.1'
STS_TITLE='智能趾端滑套仿真系统'
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
import mod
from mod.AroPlot import FigurePlc


esui.COLOR_BACK='#ffffff'
esui.COLOR_LBACK='#eeeeee'
esui.COLOR_TEXT='#000000'
esui.COLOR_FRONT='#66ccff'
esui.COLOR_SECOND='#666699'
# Editor main window;
class EvrSimSTS(esui.EsWindow):
    def __init__(self):
        super().__init__(title=STS_TITLE)
        xu=esui.XU
        yu=esui.YU
        esui.WXMW=self
        esui.HEAD_PLC=esui.HeadBar(self,title=STS_TITLE)
        esui.TOOL_PLC=estool.ToolPlc(self,(0,4*yu),(self.Size.x,11*yu),single='STS')
        esui.ARO_PLC=esgl.AroGlc(self,(0,15*yu),(50*xu,85*yu),backgroundColor=(.5,.5,.5,1))
        self.PLOT_PLC=esui.Plc(self,(50*xu,15*yu),(50*xu,85*yu))
        self.plotPlcInit()
        self.PLOT_PLC.Bind(esevt.EVT_COMMON_EVENT,self.onPPComEvt)
        esui.ARO_PLC.Show()
        self.Show()
        return

    def plotPlcInit(self):
        PP=self.PLOT_PLC
        yu=esui.YU
        PP.btn_sleeve=esui.TabBtn(PP,(0,0),(8*yu,4*yu),'滑套')
        PP.btn_pistol=esui.TabBtn(PP,(8*yu,0),(8*yu,4*yu),'活塞')

        PP.figure=FigurePlc(PP,(yu,4*yu),(PP.Size.x-2*yu,PP.Size.y-14*yu),
            title='仿真数据追踪',xlabel='T/s',ylabel='Displacement/mm')

        esui.StaticText(PP,(yu,PP.Size.y-10*yu),(8*yu,4*yu),'显示选项：',align='left')

        PP.btn_x=esui.SelectBtn(PP,(yu,PP.Size.y-5*yu),(4*yu,4*yu),'√',select=True)
        PP.txt_x=esui.StaticText(PP,(5*yu,PP.Size.y-5*yu),(8*yu,4*yu),'位移')

        PP.btn_v=esui.SelectBtn(PP,(13*yu,PP.Size.y-5*yu),(4*yu,4*yu),'√')
        PP.txt_v=esui.StaticText(PP,(17*yu,PP.Size.y-5*yu),(8*yu,4*yu),'速度')

        PP.btn_a=esui.SelectBtn(PP,(26*yu,PP.Size.y-5*yu),(4*yu,4*yu),'√')
        PP.txt_a=esui.StaticText(PP,(30*yu,PP.Size.y-5*yu),(8*yu,4*yu),'加速度')

        PP.btn_pip=esui.SelectBtn(PP,(39*yu,PP.Size.y-5*yu),(4*yu,4*yu),'√')
        PP.txt_pip=esui.StaticText(PP,(43*yu,PP.Size.y-5*yu),(8*yu,4*yu),'管压')
        return

    def onPPComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_SIM_CIRCLED:
            x=ESC.getAroByName('toe_sleeve').position[0]
            t=ESC.getAcp(6,('STS','sts')).current
            self.PLOT_PLC.figure.appendPoints({'x':[(t,x)]})
        return
    pass

# Main enterance;
wxmw=EvrSimSTS()
esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,[esevt.ETYPE_OPEN_SIM,'STS'])
ESC.loadMapFile('init')
esui.ARO_PLC.readMap()
esui.ARO_PLC.toolbar.Hide()
esgl.projMode(False)
esgl.lookAt([0,0,5],[0,0,0])
esui.WXAPP.MainLoop()
