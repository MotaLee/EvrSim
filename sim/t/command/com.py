from core import ESC
import mod.AroCore
import mod.Dynamics
# SIM STREAM
ESC.initAro(mod.AroCore.Aro,{'AroName':'main'})
ESC.initAro(mod.Dynamics.MassPoint,{'AroName':'m1','parent':'main','mass':10,'position':[0,0,0]})
ESC.initAro(mod.Dynamics.MassPoint,{'AroName':'m2','parent':'main','mass':100,'position':[1,2,0]})
# END
