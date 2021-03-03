import os,shutil
from core import esc as ESC
def newSim(simname,src='_Template'):
    'Lv1: Create new sim by copying para src dir without opening;'
    file_list=os.listdir('sim/')
    for f in file_list:
        if simname==f: return ESC.err('Sim existed.')
    tar_path='sim/'+simname+'/'
    src_path='sim/'+src+'/'
    shutil.copytree(src_path,tar_path)
    return

def delSim(simname):
    'Lv1: ;'
    if ESC.isSimOpened(): return ESC.err('Sim opened.')
    if simname in os.listdir('sim/'):
        shutil.rmtree('sim/'+simname)
    else: return ESC.err('Sim not found.')
    return

def openSim(simname):
    'Lv2: Open sim, and load mod and setting;'
    ESC.initESC()
    if ESC.isSimOpened(): return ESC.err('Sim already opened.')

    ESC.SIM_NAME=simname
    if simname in os.listdir('sim/'):
        shutil.copy('sim/'+simname+'/sim.py','sim/'+simname+'/_sim.py')
        SIM_FD=open('sim/'+simname+'/_sim.py','r+')
    else: return ESC.err('Sim not found.')

    # Read sim index;
    simtxt=SIM_FD.read()
    SIM_FD.close()
    _locals=dict()
    exec(simtxt,globals(),_locals)

    ESC.SIM_TREE=SimTree(_locals['SIM_TREE'])
    ESC.loadMod(ESC.SIM_TREE.node_mod.data)
    ESC.setSim(ESC.SIM_TREE.node_perf.data)
    ESC.MAP_LIST=ESC.SIM_TREE.node_map.data
    if ESC.MAP_ACTIVE=='':ESC.MAP_ACTIVE=ESC.MAP_LIST[0]
    ESC.loadMapFile(ESC.MAP_ACTIVE)
    for mdl in ESC.SIM_TREE.node_model.data:
        ESC.loadModelFile((ESC.SIM_NAME,mdl))

    return

def closeSim(save=False):
    'Lv2: Close current sim and load default setting;'
    if not ESC.isSimOpened(): return ESC.err('Sim not opened.')

    if save:ESC.saveSim()

    os.remove('sim/'+ESC.SIM_NAME+'/_sim.py')

    ESC.initESC()
    return

def setSim(setdict,usercall=True):
    ''' Lv1: Load setting.
        * Para usercall: True default.
        Wouldnt change simtree perf if not usercall;'''
    if not ESC.isSimOpened():return ESC.err('Sim not opened.')
    for k,v in setdict.items():
        if k not in ESC.SIM_TREE.node_perf.data or usercall:
            ESC.__dict__[k]=v
            if usercall:ESC.SIM_TREE.node_perf.data[k]=v
    return

def saveSim():
    'Save current sim;'
    if not ESC.isSimOpened():return ESC.err('Sim not opened.')
    ESC.saveModelFile()
    ESC.saveMapFile()
    treestr='SIM_TREE='+ESC.SIM_TREE.saveTree(savedata=True)
    SIM_FD=open('sim/'+ESC.SIM_NAME+'/_sim.py','r+')
    SIM_FD.seek(0,0)
    SIM_FD.truncate()
    SIM_FD.write(treestr)
    SIM_FD.flush()
    shutil.copy('sim/'+ESC.SIM_NAME+'/_sim.py','sim/'+ESC.SIM_NAME+'/sim.py')

    return

def resetSim():
    ESC.STATIC_PREPARED=False
    ESC.ACPS_PREPARED['Providers']=dict()
    ESC.loadMapFile()
    return

class SimTree(ESC.EsTree):
    def __init__(self,tree):
        super().__init__(tree=tree)
        self.node_perf=self.getNode('Perference')
        self.node_map=self.getNode('Map')
        self.node_model=self.getNode('Model')
        self.node_mod=self.getNode('Mod')
        return
    pass
