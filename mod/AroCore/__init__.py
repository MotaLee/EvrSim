# libs;
from core import ESC,esui
# Class import;
Aro=ESC.Aro
from .aro import AroPoint,AroTree,AroSpace,AroGroup
from .aro import AroTargets,AroImage,AroField,AroLight
from .acp import Acp,AcpConst,AcpSelector,AcpProvider,AcpIterator,AcpExecutor
from .acp import AcpVector3,AcpDepartor3,AcpNorm
from .acp import AcpPMTD,AcpLimitor,AcpSum,AcpCross

from .adp import AdpPoint,AdpArrow,AdpImage,AdpPlane,AdpCube,AdpCS
from .atl import AroMenu,AcpMenu,RunSimBtn,SimTimeText
from .atl import ResetMapBtn,RealTimeText,WrkSpcBtn
# from .setting import set_dict
# Mod index and global var;
MOD_NAME='AroCore'
MOD_VER='0.0.10'
MOD_PERF={}
ARO_INDEX=['AroPoint']
ACP_INDEX=[
    'Acp','AcpConst','AcpSelector','AcpProvider','AcpIterator',
    'AcpVector3','AcpDepartor3','AcpNorm','AcpPMTD','AcpSum',
    'AcpCross','AcpLimitor']
MODEL_INDEX=[]

TP=None
# Tool preset;
if ESC.ES_APP!='EST':
    if esui.ARO_PLC is None: ESC.err('Leak of reliabilities.')
    TP=esui.TOOL_PLC.getTab('AroCore')
if TP is not None:
    yu=esui.YU
    new_aro=AroMenu('new_aro',TP,(yu,yu),(8*yu,4*yu),'New Aro',ARO_INDEX)
    new_acp=AcpMenu('new_acp',TP,(yu,6*yu),(8*yu,4*yu),'New Acp',ACP_INDEX)
    run_btn=RunSimBtn('run_btn',TP,(10*yu,yu),(9*yu,9*yu),'▶')
    time_txt=SimTimeText('time_txt',TP,(20*yu,6*yu),(8*yu,4*yu),'00:00:00')
    real_time=RealTimeText('real_time',TP,(28*yu,6*yu),(8*yu,4*yu),'00:00:00')
    rst_btn=ResetMapBtn('rst_btn',TP,(20*yu,yu),(4*yu,4*yu),'Rst')
    # alibs_btn=ALibsBtn('alibs_btn',TP,(25*yu,yu),(8*yu,4*yu),'ALibs..')
    btn_ws=WrkSpcBtn('btn_ws',TP,(34*yu,yu),(8*yu,4*yu),'Aro/Acp')
