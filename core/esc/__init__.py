''' EvrSim Core class.

    Communicate with memory and files;'''
import os
# Built-in importion;
import mod
from .Aro import getAro,addAro,delAro,initAro,setAro,getAroByName,sortAro
from .Acp import getAcp,addAcp,setAcp,delAcp,initAcp,connectAcp
from .Map import newMapFile,loadMapFile,updateMapFile,renameMapFile,sortAroMap
from .Model import newModelFile,loadModelFile,updateModelFile,getModelPath,renameModelFile
from .Running import runSim,reqAcp,runCompiledSim,compileModel
from .Sim import newSim,openSim,delSim,closeSim,setSim,saveSim,resetSim

ES_PATH=os.getcwd()
ES_APP=''
CORE_STAUS='READY'     # ['READY','BUSY','STOP','STEP']
SIM_NAME=''
SIM_FD=None
MOD_LIST=list()
USER_SETTING=dict()
# Core modified;
TIME_RATE=1
MODEL_DISABLE=list()
# Maps and models;
ARO_ORDER=list()
ARO_MAP=dict()
MAP_QUEUE=list()
ARO_MAP_NAME=''
MAP_LIST=list()

ACPID_MAX=dict()    # {(modName,modelName):acpid, ...}
ACP_MODELS=dict()     # {(modName,modelName):[acplist...]} | {'simInModelName':[...]}
STATIC_DICT=dict()      # {(modname,mdlname,acpid):datadict, ...}
STATIC_PREPARED=False
ACPS_PREPARED={'Providers':dict(),'Executors':dict(),'Iterators':dict()}
DATADICT=dict()
COMPILED_MODEL=None

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
    global MODEL_DISABLE,ARO_MAP,MAP_QUEUE,ARO_MAP_NAME
    global ACPID_MAX,ACP_MODELS,SIM_REALTIME,SIM_RECORD,SIM_QUEUE_LEN
    global ACP_DEPTH,TIME_STEP,MAP_LIST
    CORE_STAUS='READY'
    SIM_NAME=''
    SIM_FD=None
    MOD_LIST=list()
    USER_SETTING=dict()
    TIME_RATE=1
    MODEL_DISABLE=list()
    ARO_MAP=list()
    MAP_QUEUE=list()
    ARO_MAP_NAME=''
    MAP_LIST=list()
    ACPID_MAX=dict()
    ACP_MODELS=dict()
    SIM_REALTIME=True
    SIM_RECORD=False
    SIM_QUEUE_LEN=1
    ACP_DEPTH=20
    TIME_STEP=1/30
    return

def info(string,level='[Info] ',record=False):
    string=level+string
    print(string)
    if record:pass
    return string

def bug(bugstr,record=False):
    'Lv0: Report bug str;'
    info(bugstr,level='[Bug] ',record=record)
    return bugstr

def loadMod(modlist,unload=False):
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
    if unload:
        for m in MOD_LIST:
            'todo: unload mods'
    return

# EsTree;
class EsTree(object):
    def __init__(self,node=None):
        self.tree=dict()
        self.parent_links=dict()
        self.children_links=dict()
        self.max_id=-1
        self.root=None
        self.node_class=TreeNode
        if node is not None:
            self.appendNode(node,None)
        return

    def getNode(self,nid=-1,label=''):
        if nid!=-1:return self.tree[nid]
        if label!='':
            for node in self.tree.values():
                if node.label==label:return node
        return None

    def initNode(self,cls=None,**argkw):
        if cls is None:cls=self.node_class
        node=cls(argkw)
        return node

    def appendNode(self,node,parent):
        ''' Para parent: Accept int/TreeNode.'''
        self.max_id+=1
        node.nid=self.max_id
        if parent is not None:
            if isinstance(parent,int):
                parent=self.getNode(nid=parent)
            if parent is None:bug('E: Parent node not found.')
            self.parent_links[node.nid]=parent.nid
            self.children_links[parent.nid].append(node.nid)
            node.parent=parent
            parent.children.append(node)
        else:
            self.parent_links[node.nid]=None
            self.root=node
        self.tree[node.nid]=node
        return

    def delNode(self,node):
        if isinstance(node,int):
            node=self.getNode(nid=node)
        pnid=self.parent_links[node.nid]
        if pnid is not None:
            self.tree[pnid].children.remove(node)
            self.children_links[pnid].remove(node.nid)
        else:self.__init__(None)
        subtree=self.travsalTree(node,lambda e: None)
        for nid in subtree:
            del self.tree[nid]
            del self.parent_links[nid]
            del self.children_links[nid]
        return

    def travsalTree(self,start=None,method=None):
        if start is None: start=self.root
        if method is None:method=self.visitNode
        stack=[start]
        visited=list()
        track=list()
        while(len(stack)!=0):
            node=stack[-1]
            if node.nid in visited:
                stack.pop()
                track.append(node.nid)
                continue
            children_ready=True
            for child in self.children_links[node.nid]:
                if child not in visited:
                    stack.append(self.tree[child])
                    children_ready=False
                    break
            if children_ready:
                visited.append(node.nid)
                method(node)

        return track

    def visitNode(self,node):
        ''' Overrided.'''
        return
    pass

class TreeNode(object):
    def __init__(self,**argkw):
        self.nid=0
        self.label=argkw.get('label','Node')
        self.children=list()
        self.parent=None
        return
    pass
