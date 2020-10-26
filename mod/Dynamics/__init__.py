# libs;
from core import ESC
from core import esui
# Mod-in import;
from mod.AroCore.tool import AroMenu,AcpMenu
from .adp import DpRigidGroup,DpMoment,DpConstraint,DpGround
from .aro import MassPoint,RigidGroup,Moment,Constraint,Ground,PointForce
from .tool import RGMenu,NewRGBtn,DelRGBtn,ConnectRGBtn,RemoveFromRGBtn
from .acp import IPE
# MOD INDEX
MOD_NAME='Dynamics'
MOD_VER='0.0.3'
MOD_SETTING={}
ARO_INDEX=['MassPoint','PointForce','Moment','Ground','Constraint']
ACP_INDEX=[]
TOOL_INDEX=['new_obj','new_acp','rg_menu','new_rg','del_rg','connect_rg','remove_rg']
MODEL_INDEX=['ug']
TP=None

# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
if ESC.ES_APP!='EST':
    if esui.ARO_PLC is None or esui.ACP_PLC is None or esui.TOOL_PLC is None:
        raise ESC.bug('E: Leak of reliabilities.')

    yu=esui.YU
    TP=esui.TOOL_PLC.getModTab('Dynamics')
    psx=esui.TOOL_PLC.Size[0]
    new_obj=AroMenu('new_Obj',TP,(yu,yu),(8*yu,4*yu),'New Obj',ARO_INDEX)
    new_acp=AcpMenu('new_acp',TP,(yu,6*yu),(8*yu,4*yu),'New Acp',ACP_INDEX)

    rg_menu=RGMenu('rg_menu',TP,(psx-18*yu,yu),(17*yu,4*yu),'')
    new_rg=NewRGBtn('new_rg',TP,(psx-18*yu,6*yu),(8*yu,4*yu),'New RG')
    del_rg=DelRGBtn('del_rg',TP,(psx-9*yu,6*yu),(8*yu,4*yu),'Del RG')
    connect_rg=ConnectRGBtn('connect_rg',TP,(psx-18*yu,11*yu),(8*yu,4*yu),'Connect')
    remove_rg=RemoveFromRGBtn('remove_rg',TP,(psx-9*yu,11*yu),(8*yu,4*yu),'Remove')

pass
