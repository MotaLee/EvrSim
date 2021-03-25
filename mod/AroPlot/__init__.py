from core import esui
yu=esui.YU
# Mod-in import;
from .atl import XyzAxisTool,GridTool,ViewBallTool,DisplaySwitch
from .tdp import *
from .canvas_div import CanvasDiv
# MOD INDEX
MOD_NAME='AroPlot'
MOD_VER='0.0.5'
MOD_PERF={}
ARO_INDEX=[]
ACP_INDEX=[]
MODEL_INDEX=[]

# Tool preset.
if esui.UMR.hasIndex('MAP_DIV'):
    xyz_axis=XyzAxisTool()
    grid=GridTool()
    view_ball=ViewBallTool()
    # aux=AuxTool('aux',MOD_NAME)

if esui.UMR.hasIndex('TOOL_DIV'):
    PT=esui.UMR.TOOL_DIV.getModTab('AroPlot')
    ph=PT.Size.y
    txt_display=esui.DivText(PT,label='Display',
        style={'p':(yu,ph-3*yu),'s':(11*yu,2*yu)})
    btn_all=DisplaySwitch(PT,'btn_all',MOD_NAME,
        label='All',select=True,
        style={'p':(yu,yu),'s':(11*yu,3*yu)})
    btn_xyz=DisplaySwitch(PT,'btn_xyz',MOD_NAME,
        label='Xyz',select=True,
        style={'p':(yu,5*yu),'s':(3*yu,3*yu)})
    btn_grid=DisplaySwitch(PT,'btn_grid',MOD_NAME,
        label='Grd',select=True,
        style={'p':(5*yu,5*yu),'s':(3*yu,3*yu)})
    btn_vb=DisplaySwitch(PT,'btn_vb',MOD_NAME,
        label='VB',select=True,
        style={'p':(9*yu,5*yu),'s':(3*yu,3*yu)})
    btn_track=DisplaySwitch(PT,'btn_track',MOD_NAME,
        label='Trc',select=True,
        style={'p':(yu,9*yu),'s':(3*yu,3*yu)})
    btn_vec=DisplaySwitch(PT,'btn_vec',MOD_NAME,
        label='Vec',select=False,
        style={'p':(5*yu,9*yu),'s':(3*yu,3*yu)})
    btn_lcs=DisplaySwitch(PT,'btn_lcs',MOD_NAME,
        label='Vec',select=False,
        style={'p':(9*yu,9*yu),'s':(3*yu,3*yu)})
