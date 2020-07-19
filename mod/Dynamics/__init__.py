# libs;
from core import ESC
from core import esui
# Mod-in import;
from mod.AroCore.tool import CreateAroTool,CreateAcpTool
from .adp import DpRigidGroup,DpMoment,DpAxisConstraint,DpGround
from .aro import MassPoint,RigidGroup,Moment,AxisConstraint,Ground
from .acp import InstanceCenter
from .tool import RGMenuTool,NewRGTool,DelRGTool,ConnectRGTool,RemoveFromRGTool
# MOD INDEX
MOD_NAME='Dynamics'
MOD_VER='0.0.2'
MOD_SETTING={}
ARO_INDEX=['MassPoint','Moment','Ground']
ACP_INDEX=['InstanceCenter']
TOOL_INDEX=['new_obj','new_acp','rg_menu','new_rg','del_rg','connect_rg','remove_rg']
MODEL_INDEX=['ug']

# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
yu=esui.YU
psx=esui.MOD_PLC.Size[0]
new_obj=CreateAroTool('new_Obj','New Obj',(yu,yu),(8*yu,4*yu),ARO_INDEX)
new_acp=CreateAcpTool('new_acp','New Acp',(yu,6*yu),(8*yu,4*yu),ACP_INDEX)

rg_menu=RGMenuTool('rg_menu','',(psx-18*yu,yu),(17*yu,4*yu))
new_rg=NewRGTool('new_rg','New RG',(psx-18*yu,6*yu),(8*yu,4*yu))
del_rg=DelRGTool('del_rg','Del RG',(psx-9*yu,6*yu),(8*yu,4*yu))
connect_rg=ConnectRGTool('connect_rg','Connect',(psx-18*yu,11*yu),(8*yu,4*yu))
remove_rg=RemoveFromRGTool('remove_rg','Remove',(psx-9*yu,11*yu),(8*yu,4*yu))

pass
