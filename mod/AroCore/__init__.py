# libs;
from core import ESC
from core import esui
# Class import;
from .aro import Aro,AroPoint,AroTree,AroSpace,AroGroup,AroTarget
from .acp import Acp,AcpConst,AcpSelector,AcpProvider,AcpIterator
from .acp import AcpVector3,AcpDepartor3,AcpNorm
from .acp import AcpPMTD,AcpBuffer,AcpSum,AcpCross
from .adp import AdpPoint
from .tdp import TdpGrid,TdpViewBall,TdpXyzAxis
from.tool import XyzAxisTool,GridTool,ViewBallTool
from.tool import CreateAroTool,CreateAcpTool,RunSimTool,SimTimeText,ResetMapTool
# from .setting import set_dict
# Mod index and global var;
MOD_NAME='AroCore'
MOD_VER='0.0.3'
MOD_SETTING={}
ARO_INDEX=['AroPoint']
ACP_INDEX=['Acp','AcpConst','AcpSelector','AcpProvider','AcpIterator',
    'AcpVector3','AcpDepartor3','AcpNorm','AcpPMTD','AcpSum','AcpCross']
TOOL_INDEX=['new_aro','new_acp','run_btn','time_txt','rst_btn',
    'xyz_axis','grid','view_ball']
MODEL_INDEX=[]

# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
xu=esui.XU
yu=esui.YU
new_aro=CreateAroTool('new_aro','New Aro',(yu,yu),(8*yu,4*yu),ARO_INDEX)
new_acp=CreateAcpTool('new_acp','New Acp',(yu,6*yu),(8*yu,4*yu),ACP_INDEX)
run_btn=RunSimTool('run_btn','>',(10*yu,yu),(9*yu,9*yu),tip='Run Sim.')
time_txt=SimTimeText('time_txt','00:00:00',(20*yu,6*yu),(8*yu,4*yu))
rst_btn=ResetMapTool('rst_btn','Rst',(20*yu,yu),(4*yu,4*yu))
xyz_axis=XyzAxisTool('xyz_axis')
grid=GridTool('grid')
view_ball=ViewBallTool('view_ball')
