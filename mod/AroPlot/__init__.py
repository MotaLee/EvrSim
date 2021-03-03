# libs;
import numpy as np
import wx
from core import ESC,esui,estl,esgl
# Mod-in import;
from .tdp import TdpGrid,TdpViewBall,TdpXyzAxis
from .atl import XyzAxisTool,GridTool,ViewBallTool,AuxDisTool,MainSwitch
from .canvas_plc import CanvasPlc
# MOD INDEX
MOD_NAME='AroPlot'
MOD_VER='0.0.4'
MOD_PERF={}
AROCLASS_INDEX=[]
ACP_INDEX=[]
MODEL_INDEX=[]

# Tool preset.
AP=esui.IDX.MAP_DIV
if AP is not None:
    xyz_axis=XyzAxisTool('xyz_axis')
    grid=GridTool('grid')
    view_ball=ViewBallTool('view_ball')
    aux_dis=AuxDisTool('aux_dis')
    # esgl.drawGL()

if esui.IDX.TOOL_DIV is not None:
    yu=esui.YU
    PT=esui.IDX.TOOL_DIV.getModTab('AroPlot')
    estl.TextTool('txt_title',PT,(yu,yu),(8*yu,4*yu),'AroPlot: '+MOD_VER)
    estl.TextTool('txt_main',PT,(yu,6*yu),(4*yu,4*yu),'All:')
    btn_main=MainSwitch('btn_main',PT,(6*yu,6.5*yu),(3*yu,3*yu))
