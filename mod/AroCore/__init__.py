# libs;
from core import ESC
from core import esui
# Class import;
from .aroclass import Aro,AroSpace
from .acpclass import Acp,AcpSelector,AcpProvider,AcpBuffer,AcpIterator
from .acpclass import AcpVector3,AcpDepartor3,AcpPMTD
from.tool import CreateAroTool,CreateAcpTool,RunSimTool,TimeTextTool,ResetMapTool
# from .setting import set_dict
# Mod index and global var;
MOD_NAME='AroCore'
MOD_VER='0.0.2'
MOD_SETTING={}
AROCLASS_INDEX=['Aro','AroSpace']
ACPCLASS_INDEX=['Acp','AcpSelector','AcpProvider','AcpIterator','AcpVector3','AcpDepartor3','AcpPMTD']
TOOL_INDEX=['new_aro','new_acp','run_btn','time_txt','rst_btn']
MODEL_INDEX=[]
# Tool preset;
# Tool variable name need to add to TOOL_INDEX in __init__.py;
xu=esui.gmv.XU
yu=esui.gmv.YU
new_aro=CreateAroTool('new_aro','New Aro',(yu,yu),(8*yu,4*yu),AROCLASS_INDEX)
new_acp=CreateAcpTool('new_acp','New Acp',(yu,6*yu),(8*yu,4*yu),ACPCLASS_INDEX)
run_btn=RunSimTool('run_btn','>',(10*yu,yu),(9*yu,9*yu),tip='Run Sim.')
time_txt=TimeTextTool('time_txt','00:00:00',(20*yu,6*yu),(8*yu,4*yu))
rst_btn=ResetMapTool('rst_btn','Rst',(20*yu,yu),(4*yu,4*yu))
