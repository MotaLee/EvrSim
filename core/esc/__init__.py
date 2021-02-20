'''
## EvrSim Core

Communicate with memory and files.
'''

import os,json
# Built-in importion;
import mod
from .cls import EsTree,TreeNode,Aro
from .aro import getAro,addAro,delAro,initAro,setAro,getAroByName,sortAro
from .Acp import getAcp,addAcp,setAcp,delAcp,initAcp,connectAcp
from .Map import newMapFile,loadMapFile,saveMapFile,renameMapFile,sortMap
from .Mdl import newModelFile,loadModelFile,updateModelFile,getModelPath,renameModelFile
from .Run import runSim,reqAcp,runCompiledSim,compileModel
from .Sim import newSim,openSim,delSim,closeSim,setSim,saveSim,resetSim,SimTree
from .Mod import loadMod,getModAttr
# Attr;
ES_PATH=os.getcwd()
ES_APP=''
CORE_STAUS='READY'     # ['READY','BUSY','STOP','STEP']
SIM_NAME=''
SIM_FD=None
SIM_TREE:SimTree=None
MOD_TREE_DICT=dict()
PERFERENCE=dict()
# Core modified;
TIME_RATE=1
MODEL_ENABLE=list()
# Maps and models;
ARO_ORDER=list()
ARO_MAP=dict()
MAP_QUEUE=list()
MAP_ACTIVE=''
MAP_LIST=list()

ACPID_MAX=dict()    # {(modName,modelName):acpid, ...}
ACP_MODELS=dict()     # {(modName,modelName):[acplist...]} | {'simInModelName':[...]}
STATIC_DICT=dict()      # {(modname,mdlname,acpid):datadict, ...}
STATIC_PREPARED=False
ACPS_PREPARED={'Providers':dict(),'Executors':dict(),'Iterators':dict()}
DATADICT=dict()
COMPILED_MODEL=None

# User changeable setting;
flag_realtime=True
flag_record=False
len_sim_queue=1
len_timestep=1/30     # Unit second, fps=30;
max_acp_depth=20
SETTING_DICT={
    'Simulate realtime':'flag_realtime',
    'Record data':'flag_record',
    'Queue length':'len_sim_queue',
    'Max Acp depth':'max_acp_depth',
    'Time step':'len_timestep'}


# Methods
def initESC():
    global CORE_STAUS,SIM_NAME,SIM_FD,SIM_TREE
    global MOD_TREE_DICT,PERFERENCE,TIME_RATE
    global MODEL_ENABLE,ARO_MAP,MAP_QUEUE,MAP_ACTIVE
    global ACPID_MAX,ACP_MODELS,flag_realtime,flag_record,len_sim_queue
    global max_acp_depth,len_timestep,MAP_LIST
    CORE_STAUS='READY'
    SIM_NAME=''
    SIM_FD=None
    SIM_TREE=None
    MOD_TREE_DICT=dict()
    PERFERENCE=dict()
    TIME_RATE=1
    MODEL_ENABLE=list()
    ARO_MAP=dict()
    MAP_QUEUE=list()
    MAP_ACTIVE=''
    MAP_LIST=list()
    ACPID_MAX=dict()
    ACP_MODELS=dict()
    flag_realtime=True
    flag_record=False
    len_sim_queue=1
    max_acp_depth=20
    len_timestep=1/30
    return

def info(string,level='[Info] ',record=False):
    string=level+string
    print(string)
    if record:pass
    return string

def err(errstr,record=False):
    'Lv0: Report error str;'
    info(errstr,level='[Err] ',record=record)
    raise BaseException(errstr)
    return errstr

def getFullMap():
    return ARO_MAP.values()

def isSimOpened():
    return SIM_NAME!=''
