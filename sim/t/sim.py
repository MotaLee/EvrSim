# EvrSim simulation file;
# NOTICE: The big word comment must not be modified;
from core import ESC
import mod.AroCore
import mod.Dynamics
# Sim-in import;
pass

# SIM INDEX
SIM_NAME='t'
SIM_SETTING={'ACP_DEPTH':15}
MOD_INDEX=['AroCore','Dynamics']
AROCLASS_INDEX=[]
ACPCLASS_INDEX=[]
TOOL_INDEX=[]
MAP_INDEX=['init']
MODEL_INDEX=[]
# END

# SIM STREAM
ESC.initAro(mod.AroCore.Aro,{'AroName':'main'})
ESC.initAro(mod.Dynamics.MassPoint,{'AroName':'m1','parent':'main','mass':10,'position':[0,0,0]})
ESC.initAro(mod.Dynamics.MassPoint,{'AroName':'m2','parent':'main','mass':100,'position':[1,2,0]})
# END

# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
pass
