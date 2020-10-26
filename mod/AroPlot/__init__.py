# libs;
import numpy as np
import wx
from core import ESC,esui,estool
# Mod-in import;
from .tdp import TdpGrid,TdpViewBall,TdpXyzAxis
from.tool import XyzAxisTool,GridTool,ViewBallTool,AuxDisTool
from .canvas_plc import CanvasPlc
# MOD INDEX
MOD_NAME='AroPlot'
MOD_VER='0.0.2'
MOD_SETTING={}
AROCLASS_INDEX=[]
ACP_INDEX=[]
TOOL_INDEX=[]
MODEL_INDEX=[]

# Tool preset.
# Variable of tool name need to add to TOOL_INDEX, otherwise unable to be indexed;
if esui.ARO_PLC is not None:
    xyz_axis=XyzAxisTool('xyz_axis')
    grid=GridTool('grid')
    view_ball=ViewBallTool('view_ball')
    aux_dis=AuxDisTool('aux_dis')
    esui.ARO_PLC.drawGL()
def onClkMain(e):
    xyz_axis.tdp.visible=not xyz_axis.tdp.visible
    grid.tdp.visible=not grid.tdp.visible
    view_ball.tdp.visible=not view_ball.tdp.visible
    esui.ARO_PLC.drawGL()
    return
if esui.TOOL_PLC is not None:
    yu=esui.YU
    PT=esui.TOOL_PLC.getModTab('AroPlot')
    estool.TextTool('txt_title',PT,(yu,yu),(8*yu,4*yu),'AroPlot: '+MOD_VER)
    estool.TextTool('txt_main',PT,(yu,6*yu),(4*yu,4*yu),'Aux:')
    btn_main=estool.ToggleTool('btn_main',PT,(6*yu,6.5*yu),(3*yu,3*yu),'',select=True)
    btn_main.Bind(wx.EVT_LEFT_DOWN,onClkMain)
