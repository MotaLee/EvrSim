# libs;
from core import ESC,esui
import mod.AroCore as AC
# Class import;
from .aro import MeshObject

# from .acp import Acp,AcpConst,AcpSelector,AcpProvider,AcpIterator,AcpExecutor
# from .acp import AcpVector3,AcpDepartor3,AcpNorm
# from .acp import AcpPMTD,AcpLimitor,AcpSum,AcpCross

from .adp import MeshObj
# from .atl import AroMenu,AcpMenu,RunSimBtn,SimTimeText,ResetMapBtn,ALibsBtn,RealTimeText
# from .setting import set_dict
# Mod index and global var;
MOD_NAME='Game'
MOD_VER='0.0.1'
MOD_PERF={}
ARO_INDEX=['MeshObject']
ACP_INDEX=[]
MODEL_INDEX=[]
TP=None
# Tool preset;
if esui.IDX.TOOL_DIV is not None:
    if not esui.IDX.hasIndex('MAP_DIV'):
        ESC.err('Leak of reliabilities.')
    TP=esui.IDX.TOOL_DIV.getTab(MOD_NAME)
if TP is not None:
    yu=esui.YU
    new_obj=AC.AroMenu('new_obj',TP,(yu,yu),(8*yu,4*yu),'New obj',ARO_INDEX)
    # new_acp=AcpMenu('new_acp',TP,(yu,6*yu),(8*yu,4*yu),'New Acp',ACP_INDEX)
    # run_btn=RunSimBtn('run_btn',TP,(10*yu,yu),(9*yu,9*yu),'▶')
    # time_txt=SimTimeText('time_txt',TP,(20*yu,6*yu),(8*yu,4*yu),'00:00:00')
    # real_time=RealTimeText('real_time',TP,(28*yu,6*yu),(8*yu,4*yu),'00:00:00')
    # rst_btn=ResetMapBtn('rst_btn',TP,(20*yu,yu),(4*yu,4*yu),'Rst')
    # alibs_btn=ALibsBtn('alibs_btn',TP,(25*yu,yu),(8*yu,4*yu),'ALibs..')
