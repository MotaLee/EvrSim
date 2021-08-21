from core import ESC
import mod.AroCore
import mod.Dynamics
# SIM STREAM
ESC.addAro(mod.AroCore.Aro,{'AroName':'main'})
ESC.addAro(mod.Dynamics.MassPoint,{'AroName':'m1','parent':'main','mass':10,'position':[0,0,0]})
ESC.addAro(mod.Dynamics.MassPoint,{'AroName':'m2','parent':'main','mass':100,'position':[1,2,0]})
# END
