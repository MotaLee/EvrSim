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
from core import estl
import mod

esui.COLOR_BACK='#ffffff'
esui.COLOR_LBACK='#eeeeee'
esui.COLOR_TEXT='#000000'
esui.COLOR_FRONT='#66ccff'
esui.COLOR_ACTIVE='#666699'

class PlotPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        yu=esui.YU
        self.btn_sleeve=esui.TabBtn(self,(0,0),(8*yu,4*yu),'滑套')
        self.btn_pistol=esui.TabBtn(self,(8*yu,0),(8*yu,4*yu),'活塞')
        from mod.AroPlot import CanvasPlc
        self.canvas=CanvasPlc(self,(yu,4*yu),(self.Size.x-2*yu,self.Size.y-14*yu))
        self.canvas.initCanvas(title='仿真数据追踪',xlabel='T/s',ylabel='Displacement/mm')
        self.canvas.drawCanvas()

        esui.StaticText(self,(yu,self.Size.y-10*yu),(8*yu,4*yu),'显示选项：',align='left')

        self.btn_x=esui.SltBtn(self,(yu,self.Size.y-5*yu),(4*yu,4*yu),'√',select=True)
        self.txt_x=esui.StaticText(self,(5*yu,self.Size.y-5*yu),(8*yu,4*yu),'位移')

        self.btn_v=esui.SltBtn(self,(13*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
        self.txt_v=esui.StaticText(self,(17*yu,self.Size.y-5*yu),(8*yu,4*yu),'速度')

        self.btn_a=esui.SltBtn(self,(26*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
        self.txt_a=esui.StaticText(self,(30*yu,self.Size.y-5*yu),(8*yu,4*yu),'加速度')

        self.btn_pip=esui.SltBtn(self,(39*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
        self.txt_pip=esui.StaticText(self,(43*yu,self.Size.y-5*yu),(8*yu,4*yu),'管压')
        self.Bind(esevt.EVT_COMMON_EVENT,self.onPPComEvt)
        return

    def onPPComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_SIM_CIRCLED:
            x=ESC.getAroByName('toe_sleeve').position[0]
            t=ESC.getAcp(6,('STS','sts')).current
            self.canvas.appendPoints({'x':[(t,x)]})
        return
    pass

# Editor main window;
class EvrSimSTS(esui.EsWindow):
    def __init__(self):
        super().__init__(title=STS_TITLE)
        esui.IDX.bindIndex(self,'ESMW')
        xu=esui.XU
        yu=esui.YU
        esui.IDX.HEAD_DIV=esui.HeadBar(self,title=STS_TITLE)
        esui.IDX.TOOL_DIV=estl.ToolDiv(self,style={'p':(0,4*yu),'s':(self.Size.x,11*yu)})
        esui.IDX.MAP_DIV=esgl.AroGlc(self,(0,15*yu),(50*xu,85*yu),backgroundColor=(.5,.5,.5,1))
        self.PLOT_PLC=PlotPlc(self,(50*xu,15*yu),(50*xu,85*yu))
        esui.IDX.MAP_DIV.Show()
        self.Show()
        return
    pass

# Main enterance;
ESMW=EvrSimSTS()
esevt.sendEvent(esevt.ETYPE_COMEVT,[esevt.ETYPE_OPEN_SIM,'STS'])
ESC.loadMapFile('init')
esui.IDX.MAP_DIV.readMap()
esui.IDX.TOOL_DIV.toggleSingleMode('STS')
# esui.IDX.MAP_DIV.toolbar.Hide()
esgl.projMode(False)
esgl.lookAt([0,0,5],[0,0,0])
