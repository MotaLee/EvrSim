# libs;
from core import ESC,esui
# Class import;
from .aro import Aro,AroPoint,AroTree,AroSpace,AroGroup,AroTargets,AroImage
from .acp import Acp,AcpConst,AcpSelector,AcpProvider,AcpIterator,AcpExecutor
from .acp import AcpVector3,AcpDepartor3,AcpNorm
from .acp import AcpPMTD,AcpLimitor,AcpSum,AcpCross
from .adp import AdpPoint,AdpArrow,AdpImage
from.tool import AroMenu,AcpMenu,RunSimBtn,SimTimeText,ResetMapBtn,ALibsBtn,RealTimeText
from .arotoolbar import AroToolbarPlc
# from .setting import set_dict
# Mod index and global var;
MOD_NAME='AroCore'
MOD_VER='0.0.4'
MOD_SETTING={}
ARO_INDEX=['AroPoint']
ACP_INDEX=['Acp','AcpConst','AcpSelector','AcpProvider','AcpIterator',
    'AcpVector3','AcpDepartor3','AcpNorm','AcpPMTD','AcpSum','AcpCross','AcpLimitor']
TOOL_INDEX=['new_aro','new_acp','run_btn','time_txt','rst_btn','real_time']
MODEL_INDEX=[]
TP=None
# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
if ESC.ES_APP!='EST':
    if esui.ARO_PLC is None  or esui.TOOL_PLC is None:
        ESC.bug('E: Leak of reliabilities.')
        raise BaseException
    yu=esui.YU
    TP=esui.TOOL_PLC.getModTab('AroCore')
    esui.ARO_PLC.toolbar=AroToolbarPlc()
if TP is not None:
    new_aro=AroMenu('new_aro',TP,(yu,yu),(8*yu,4*yu),'New Aro',ARO_INDEX)
    new_acp=AcpMenu('new_acp',TP,(yu,6*yu),(8*yu,4*yu),'New Acp',ACP_INDEX)
    run_btn=RunSimBtn('run_btn',TP,(10*yu,yu),(9*yu,9*yu),'▶')
    time_txt=SimTimeText('time_txt',TP,(20*yu,6*yu),(8*yu,4*yu),'00:00:00')
    real_time=RealTimeText('real_time',TP,(28*yu,6*yu),(8*yu,4*yu),'00:00:00')
    rst_btn=ResetMapBtn('rst_btn',TP,(20*yu,yu),(4*yu,4*yu),'Rst')
    alibs_btn=ALibsBtn('alibs_btn',TP,(25*yu,yu),(8*yu,4*yu),'ALibs..')
