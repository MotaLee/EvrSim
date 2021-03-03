# libs;
from core import ESC,esui
# Mod-in import;
from .octree import OcTree
from mod.AroCore.atl import AroMenu,AcpMenu
from .adp import DpRigidGroup,DpMoment,DpConstraint,DpGround
from .aro import MassPoint,RigidGroup,Moment,ForceField,RigidBody
from .aro import Constraint,Ground,PointForce,PlaneGnd,MassCube
from .atl import RGMenu,NewRGBtn,DelRGBtn,ConnectRGBtn,RemoveFromRGBtn,DynamicsTool
from .acp import IPE
from .bullet import BulletEngine
# MOD INDEX
MOD_NAME='Dynamics'
MOD_VER='0.0.6'
MOD_PERF={}
ARO_INDEX=['MassPoint','PointForce','Moment','Ground','Constraint','PlaneGnd','MassCube','ForceField']
ACP_INDEX=['IPE','CPE','BulletEngine']
MODEL_INDEX=['ug','PM1','PM2','PM3']
TP=None

# Tool preset;
if esui.IDX.hasIndex('TOOL_DIV'):
    if not esui.IDX.hasIndex('MAP_DIV'):raise ESC.err('Leak of reliabilities.')

    yu=esui.YU
    TP=esui.IDX.TOOL_DIV.getModTab('Dynamics')
    psx=esui.IDX.TOOL_DIV.Size[0]
    dynamic_tool=DynamicsTool('dynamic_tool',TP,(yu,yu),(8*yu,4*yu),'Dynamics')
    new_obj=AroMenu('new_Obj',TP,(yu,6*yu),(8*yu,4*yu),'New Obj',ARO_INDEX)
    new_acp=AcpMenu('new_acp',TP,(yu,11*yu),(8*yu,4*yu),'New Acp',ACP_INDEX)

    rg_menu=RGMenu('rg_menu',TP,(psx-18*yu,yu),(17*yu,4*yu),'')
    new_rg=NewRGBtn('new_rg',TP,(psx-18*yu,6*yu),(8*yu,4*yu),'New RG')
    del_rg=DelRGBtn('del_rg',TP,(psx-9*yu,6*yu),(8*yu,4*yu),'Del RG')
    connect_rg=ConnectRGBtn('connect_rg',TP,(psx-18*yu,11*yu),(8*yu,4*yu),'Connect')
    remove_rg=RemoveFromRGBtn('remove_rg',TP,(psx-9*yu,11*yu),(8*yu,4*yu),'Remove')
