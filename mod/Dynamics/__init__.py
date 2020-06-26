# libs;
from core import ESC
from core import esui
gmv=esui.gmv
# Mod-in import;
from .aroclass import MassPoint
from mod.AroCore.tool import CreateAroTool
# MOD INDEX
MOD_NAME='Dynamics'
MOD_VER='0.0.1'
MOD_SETTING={'MODEL_DISABLE':[('Dynamics','ug')]}
AROCLASS_INDEX=['MassPoint']
ACP_INDEX=[]
TOOL_INDEX=['new_aro']
MODEL_INDEX=['base','ug']

# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
yu=gmv.YU
new_aro=CreateAroTool('new_aro','New Aro',(yu,yu),(8*yu,4*yu),AROCLASS_INDEX)
pass
