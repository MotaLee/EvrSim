'''
## EvrSim Core

Communicate with memory and files.
'''

import os
# Built-in importion;
import mod
from .cls import EsTree,TreeNode,Aro,CoreStatus
from .aro import getAro,addAro,delAro,initAro,setAro,getAroByName,sortAro
# from .acp import Acp,PAcp,getAcp,addAcp,setAcp,delAcp,initAcp,cntAcp
from .acp import *
from .Map import newMapFile,loadMapFile,saveMapFile,renameMapFile,sortMap
from .mdl import newModelFile,loadModelFile,saveModelFile,getModelPath,renameModelFile
from .run import reqAcp,runCompiledSim,compileModel,RunProcess
from .sim import newSim,openSim,delSim,closeSim,setSim,saveSim,resetSim,SimTree
from .Mod import loadMod,getModAttr
# Attr;
ES_PATH=os.getcwd()
ES_APP=''
CORE_STATUS=CoreStatus()
SIM_NAME=''
SIM_TREE:SimTree=None
MOD_TREE_DICT=dict()
TIME_RATE=1
MODEL_ENABLE=list()
# Maps and models;
ARO_ORDER=list()
ARO_MAP=dict()
MAP_QUEUE=list()
MAP_ACTIVE=''
MAP_LIST=list()
ACP_MODELS=dict()     # {(modName,modelName):[acplist...]} | {'simInModelName':[...]}
STATIC_PREPARED=False
ACPS_PREPARED={'Providers':dict(),'Executors':dict(),'Iterators':dict()}
DATADICT=dict()
COMPILED_MODEL=None
RUN_PROCESS=RunProcess()
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
    global CORE_STATUS,SIM_NAME,SIM_TREE
    global MOD_TREE_DICT,TIME_RATE
    global MODEL_ENABLE,ARO_MAP,MAP_QUEUE,MAP_ACTIVE
    global ACP_MODELS,flag_realtime,flag_record,len_sim_queue
    global max_acp_depth,len_timestep,MAP_LIST,RUN_PROCESS
    CORE_STATUS=CoreStatus()
    SIM_NAME=''
    SIM_TREE=None
    MOD_TREE_DICT=dict()
    TIME_RATE=1
    MODEL_ENABLE=list()
    ARO_MAP=dict()
    MAP_QUEUE=list()
    MAP_ACTIVE=''
    MAP_LIST=list()
    ACP_MODELS=dict()
    flag_realtime=True
    flag_record=False
    len_sim_queue=1
    max_acp_depth=20
    len_timestep=1/30
    RUN_PROCESS=RunProcess()
    return

def info(string,level='[Info] ',record=False):
    string=level+string
    print(string)
    if record:pass
    return string

def err(errstr,record=False):
    'Report error.'
    info(errstr,level='[Err] ',record=record)
    raise BaseException(errstr)

def warn(warnstr,record=False):
    'Report warning.'
    info(warnstr,level='[Warn] ',record=record)
    return warnstr

def getFullMap():
    return ARO_MAP.values()

def isSimOpened():
    return SIM_NAME!=''

def setApp(app):
    global ES_APP
    ES_APP=app
    return
