'''
EvrSim Core class.

Communicate with memory and files;
'''
# Built-in importion;
import mod
from .Aro import getAro,addAro,delAro,initAro,setAro,getAroByName
from .Acp import getAcp,addAcp,setAcp,delAcp,initAcp,connectAcp
from .Map import newMapFile,loadMapFile,updateMapFile
from .Model import newModelFile,loadModelFile,updateModelFile,getModelPath
from .Running import runSim
from .Sim import newSim,openSim,delSim,closeSim,setSim,saveSim,resetSim

CORE_STAUS='READY'     # ['READY','BUSY','STOP','STEP']
SIM_NAME=''
SIM_FD=None
MOD_LIST=[]
USER_SETTING={}
# Core modified;
TIME_RATE=1
MODEL_DISABLE=[]
# Maps and models;
AROID_MAX=0
ARO_MAP=[]
ARO_QUEUE=[]
ARO_MAP_NAME=''
ARO_MAP_LIST=[]

ACPID_MAX={}
ACP_MAP={}     # {'modName.modelName':[acplist...]} | {'simInModelName':[...]}

# User changeable setting;
SIM_REALTIME=True
SIM_RECORD=False
SIM_QUEUE_LEN=1
ACP_DEPTH=20
TIME_STEP=1/30     # Unit second, fps=30Hz;
SETTING_DICT={
    'Simulate realtime':'SIM_REALTIME',
    'Record data':'SIM_RECORD',
    'Queue length':'SIM_QUEUE_LEN',
    'Max Acp depth':'ACP_DEPTH',
    'Time step':'TIME_STEP'}

# Methods
def initESC():
    global CORE_STAUS,SIM_NAME,SIM_FD,MOD_LIST,USER_SETTING,TIME_RATE
    global MODEL_DISABLE,AROID_MAX,ARO_MAP,ARO_QUEUE,ARO_MAP_NAME
    global ACPID_MAX,ACP_MAP,SIM_REALTIME,SIM_RECORD,SIM_QUEUE_LEN
    global ACP_DEPTH,TIME_STEP,ARO_MAP_LIST
    CORE_STAUS='READY'
    SIM_NAME=''
    SIM_FD=None
    MOD_LIST=[]
    USER_SETTING={}
    TIME_RATE=1
    MODEL_DISABLE=[]
    AROID_MAX=0
    ARO_MAP=[]
    ARO_QUEUE=[]
    ARO_MAP_NAME=''
    ARO_MAP_LIST=[]
    ACPID_MAX={}
    ACP_MAP={}
    SIM_REALTIME=True
    SIM_RECORD=False
    SIM_QUEUE_LEN=1
    ACP_DEPTH=20
    TIME_STEP=1/30
    return

def bug(bugstr,report=False):
    'Lv0: Report bug str;'
    if report:raise bugstr
    print(bugstr)
    return bugstr

def loadMod(modlist):
    ''' Lv1: Load Mod from MOD_LIST.

        Include models and setting;'''
    for m in modlist:
        if m not in MOD_LIST:
            MOD_LIST.append(m)
            exec('import mod.'+m)

        mod_setting=eval('mod.'+m+'.MOD_SETTING')
        setSim(mod_setting,usercall=False)

        model_index=eval('mod.'+m+'.MODEL_INDEX')
        for model in model_index:
            loadModelFile((m,model))
    return
