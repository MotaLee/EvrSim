# libs;
from core import ESC
# Mod-in import;
from .aro import MassPoint,BodyCombo,Moment,ForceField,RigidBody,ComboNode
from .aro import Constraint,Ground,PointForce,MassCube,RefPoint,Beam2D
from .adp import *
from .bullet import BulletEngine
# MOD INDEX
MOD_NAME='Dynamics'
MOD_VER='0.0.7'
MOD_PERF={}
ARO_INDEX=[
    'MassPoint','PointForce','Moment','Ground',
    'Constraint','MassCube','ForceField','BodyCombo',
    'RefPoint','Beam2D']
ACP_INDEX=['BulletEngine']
MODEL_INDEX=['DyBase','ug']

ESC.enableModel((MOD_NAME,'DyBase'))
from EvrSim import ESAPP
if ESAPP=='Editor':
    from core import esui
    from mod.AroCore.atl import AroMenu,AcpMenu
    from .atl import MenuBC,BtnBC,DynamicsTool
    yu=esui.YU
    if esui.UMR.hasIndex('TOOL_DIV'):
        TP=esui.UMR.TOOL_DIV.getModTab('Dynamics')
        ph=TP.Size.y

        txt_dynamic=DynamicsTool(TP,label='Dynamics',
            style={'p':(yu,ph-3*yu),'s':(8*yu,3*yu)})
        menu_obj=AroMenu(TP,'menu_obj',MOD_NAME,
            items=ARO_INDEX,label='New Obj',
            style={'p':(yu,yu),'s':(8*yu,3*yu)})
        menu_acp=AcpMenu(TP,'menu_acp',MOD_NAME,
            items=ACP_INDEX,label='New Acp',
            style={'p':(yu,5*yu),'s':(8*yu,3*yu)})

        txt_bc=esui.DivText(TP,label='Body Combo',
            style={'p':(11*yu,ph-3*yu),'s':(13*yu,3*yu)})
        menu_bc=MenuBC(TP,
            style={'p':(11*yu,yu),'s':(13*yu,3*yu)})
        bc_apd=BtnBC(TP,label='Append',
            style={'p':(11*yu,5*yu),'s':(6*yu,3*yu)})
        bc_rmv=BtnBC(TP,label='Remove',
            style={'p':(18*yu,5*yu),'s':(6*yu,3*yu)})
        bc_cnt=BtnBC(TP,label='Connect',
            style={'p':(11*yu,9*yu),'s':(6*yu,3*yu)})
        bc_=BtnBC(TP,label='Todo',
            style={'p':(18*yu,9*yu),'s':(6*yu,3*yu)})
