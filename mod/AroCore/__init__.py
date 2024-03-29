from .aro import AroPoint
from .aro import AroImage,AroField,AroLight
from .acp import VAcp
from .adp import *

# from .setting import set_dict
# Mod index and global var;
MOD_NAME='AroCore'
MOD_VER='0.0.11'
MOD_PERF={}
ARO_INDEX=['AroPoint']
ACP_INDEX=[
    'Acp','AcpConst','AcpSetter','AcpGetter','AcpIterator',
    'AcpVector3','AcpDepartor3','AcpNorm','AcpEval','AcpSum','AcpMean',
    'AcpCross','AcpLimitor']
MODEL_INDEX=[]

from EvrSim import ESAPP
if ESAPP=='Editor':
    from core import ESC,esui
    from .atl import AroMenu,AcpMenu,RunSimBtn,SimTimeText,EnablePresetBtn
    from .atl import ResetMapBtn,RealTimeText,WrkSpcBtn
    yu=esui.YU
    if esui.UMR.hasIndex('TOOL_DIV'):
        if not esui.UMR.hasIndex('MAP_DIV'):
            ESC.err('Leak of reliabilities.')

        TP=esui.UMR.TOOL_DIV.getModTab('AroCore')
        menu_aro=AroMenu(TP,'menu_aro',MOD_NAME,items=ARO_INDEX,label='New Aro',
            style={'p':(yu,yu),'s':(8*yu,4*yu)})
        menu_acp=AcpMenu(TP,'menu_acp',MOD_NAME,items=ACP_INDEX,label='Core Acp',
            style={'p':(yu,6*yu),'s':(8*yu,4*yu)})
        btn_run=RunSimBtn(TP,label='▶',
            style={'p':(10*yu,yu),'s':(9*yu,9*yu),'text_size':3*yu})
        btn_pre=EnablePresetBtn(TP,label='Preset',
            style={'p':(25*yu,yu),'s':(4*yu,4*yu),'text_size':yu})
        txt_time=SimTimeText(TP,label='00:00:00',
            style={'p':(20*yu,6*yu),'s':(8*yu,4*yu)})
        txt_real=RealTimeText(TP,label='00:00:00',
            style={'p':(28*yu,6*yu),'s':(8*yu,4*yu)})
        btn_rst=ResetMapBtn(TP,'btn_run',MOD_NAME,label='Rst',
            style={'p':(20*yu,yu),'s':(4*yu,4*yu)})
        # alibs_btn=ALibsBtn('alibs_btn',TP,(25*yu,yu),(8*yu,4*yu),'ALibs..')
        btn_ws=WrkSpcBtn(TP,'btn_ws',MOD_NAME,label='Aro/Acp',
            style={'p':(34*yu,yu),'s':(8*yu,4*yu)})
        # mcv=ModComVar(globals())
