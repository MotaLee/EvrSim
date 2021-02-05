import os
import shutil
from core import esc as ESC
def newSim(simname,src='_Template'):
    'Lv1: Create new sim by copying para src dir without opening;'
    file_list=os.listdir('sim/')
    for f in file_list:
        if simname==f: return ESC.bug('Sim existed.')
    tar_path='sim/'+simname+'/'
    src_path='sim/'+src+'/'
    shutil.copytree(src_path,tar_path)
    return

def delSim(simname):
    'Lv1: ;'
    if ESC.SIM_FD is not None: return ESC.bug('Sim opened.')
    if simname in os.listdir('sim/'):
        shutil.rmtree('sim/'+simname)
    else: return ESC.bug('Sim not found.')
    return

def openSim(simname):
    'Lv2: Open sim, and load mod and setting;'
    ESC.initESC()
    if ESC.SIM_FD is not None: return ESC.bug('Sim already opened.')

    ESC.SIM_NAME=simname
    if simname in os.listdir('sim/'):
        shutil.copy('sim/'+simname+'/sim.py','sim/'+simname+'/_sim.py')
        ESC.SIM_FD=open('sim/'+simname+'/_sim.py','r+')
    else: return ESC.bug('Sim not found.')

    # Read sim index;
    simtxt=ESC.SIM_FD.read()
    _locals=dict()
    exec(simtxt,globals(),_locals)

    # Mod;
    ESC.loadMod(_locals['MOD_INDEX'])

    # Setting;
    ESC.setSim(_locals['USER_SETTING'])

    # Map;
    ESC.MAP_LIST=_locals['MAP_INDEX']
    ESC.ARO_MAP_NAME=ESC.MAP_LIST[0]
    ESC.loadMapFile(ESC.MAP_LIST[0])
    # Models;
    for model in _locals['MODEL_INDEX']:
        ESC.loadModelFile((ESC.SIM_NAME,model))
    return

def closeSim(save=False):
    'Lv2: Close current sim and load default setting;'
    if ESC.SIM_FD is None: return ESC.bug('Sim not opened.')

    if save:ESC.saveSim()

    ESC.SIM_FD.close()
    os.remove('sim/'+ESC.SIM_NAME+'/_sim.py')

    ESC.initESC()
    return

def setSim(setdict={},usercall=True):
    ''' Lv1: Load setting.

        Wouldnt change which in USER_SETTING.

        Empty setdict to reset all to default;'''
    if ESC.SIM_FD is None:return ESC.bug('Sim not opened.')
    if setdict=={}:
        ESC.SIM_REALTIME=True
        ESC.SIM_RECORD=False
        ESC.SIM_QUEUE_LEN=1
        ESC.ACP_DEPTH=20
        ESC.TIME_STEP=1/30
        ESC.USER_SETTING={}
    else:
        for k,v in setdict.items():
            if k not in ESC.USER_SETTING or usercall:
                ESC.__dict__[k]=v
                if usercall:ESC.USER_SETTING[k]=v
    return

def saveSim():
    'Save current sim;'
    if ESC.SIM_FD is None:return ESC.bug('Sim not opened.')
    ESC.updateModelFile()
    ESC.updateMapFile()

    simtxt='SIM_NAME="'+ESC.SIM_NAME+'"\n'
    simtxt+='USER_SETTING='+ESC.USER_SETTING.__str__()+'\n'
    simtxt+='MOD_INDEX='+ESC.MOD_LIST.__str__()+'\n'
    simtxt+='AROCLASS_INDEX=[]\n'
    simtxt+='ACPCLASS_INDEX=[]\n'
    simtxt+='TOOL_INDEX=[]\n'
    simtxt+='MAP_INDEX='+ESC.MAP_LIST.__str__()+'\n'
    model_index=[]
    for model in ESC.ACP_MODELS.keys():
        if model[0]==ESC.SIM_NAME:
            model_index.append(model[1])
    simtxt+='MODEL_INDEX='+model_index.__str__()+'\n'
    simtxt+='COM_INDEX=[""]\n'
    ESC.SIM_FD.seek(0,0)
    ESC.SIM_FD.truncate()
    ESC.SIM_FD.write(simtxt)
    ESC.SIM_FD.flush()
    shutil.copy('sim/'+ESC.SIM_NAME+'/_sim.py','sim/'+ESC.SIM_NAME+'/sim.py')

    return

def comSim():
    'todo: sim command'
    # ESC.ARO_MAP=[]
    # if ESC.SIM_FD is None:return ESC.bug('Sim not opened.')
    # ESC.SIM_FD.seek(0,0)
    # line=ESC.SIM_FD.readline()
    # while line!='# START\n':
    #     line=ESC.SIM_FD.readline()
    # while line!='# END\n':
    #     try:exec(line)
    #     except BaseException as e:print('Ex:',e)
    #     line=ESC.SIM_FD.readline()
    # ESC.SIM_FD.seek(0,0)
    return

def resetSim():
    ESC.STATIC_PREPARED=False
    ESC.ACPS_PREPARED['Providers']=dict()
    ESC.loadMapFile()
    return
