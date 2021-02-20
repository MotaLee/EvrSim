import os
from core import esc as ESC
import mod
def getModelPath(mdl_tuple):
    'Lv1: Get model path even not existed.'
    if mdl_tuple[0]==ESC.SIM_NAME:
        path='sim/'+mdl_tuple[0]+'/model/'+mdl_tuple[1]+'.py'
    else:
        path='mod/'+mdl_tuple[0]+'/model/'+mdl_tuple[1]+'.py'
    return path

def newModelFile(mdlname):
    'Lv2: Create a new model in opened sim.'
    if ESC.SIM_FD is None:return ESC.err('Sim not opened.')
    model_tuple=(ESC.SIM_NAME,mdlname)
    if model_tuple not in ESC.ACP_MODELS:
        ESC.ACP_MODELS[model_tuple]=list()
        ESC.ACPID_MAX[model_tuple]=0
    else:
        return ESC.err('Model name already existed.')
    return

def updateModelFile(mdl_tuple=None):
    ''' Lv2: Update model files by ESC.ACP_MAP.

        Empty para mdl_tuple for all models;'''
    if ESC.SIM_FD is None:return ESC.err('Sim not opened.')
    if mdl_tuple is None:
        models=list(ESC.ACP_MODELS.keys())
    else: models=[mdl_tuple]

    for model in models:
        # Build index and key dict;
        acp_index=[]
        key_dict=dict()
        for acp in ESC.ACP_MODELS[model]:
            acp_index.append(acp.AcpID)
            for k,v in acp.__dict__.items():
                if k[0]=='_':continue
                if k not in key_dict.values():
                    key_dict[len(key_dict)+1]=k
        # Complete building;
        txt='ACP_INDEX='+acp_index.__str__()+'\n'
        txt+='KEY_DICT='+key_dict.__str__()+'\n'
        # Replace key;
        temp_dict=dict()
        for acp in ESC.ACP_MODELS[model]:
            for k,v in acp.__dict__.items():
                if k[0]!='_':temp_dict[k]=v
            for k,v in key_dict.items():
                if v in temp_dict:
                    temp=temp_dict[v]
                    del temp_dict[v]
                    temp_dict[k]=temp
            txt+='Acp_'+str(acp.AcpID)+'='+temp_dict.__str__()+'\n'

        path=ESC.getModelPath(model)
        with open(path,'w+') as model_fd:
            model_fd.truncate()
            model_fd.write(txt)
    return

def loadModelFile(mdl_tuple):
    ''' Lv2: Load model from file;'''
    if ESC.SIM_FD is None:return ESC.err('Sim not opened.')
    if mdl_tuple not in ESC.ACP_MODELS:
        ESC.ACP_MODELS[mdl_tuple]=list()
        ESC.ACPID_MAX[mdl_tuple]=0
    path=ESC.getModelPath(mdl_tuple)
    with open(path,'r') as model_fd:
        content=model_fd.read()
    _locals=dict(locals())
    exec(content,globals(),_locals)
    ACP_INDEX=_locals['ACP_INDEX']
    KEY_DICT=_locals['KEY_DICT']
    for acpid in ACP_INDEX:
        acp=_locals['Acp_'+str(acpid)]
        for k,v in KEY_DICT.items():
            if k in acp:
                temp=acp[k]
                del acp[k]
                acp[v]=temp
        ESC.initAcp(acp['AcpClass'],acp,mdl_tuple)
    return

def renameModelFile(mdlname,newname):
    'Rename model in sim.'
    if ESC.SIM_FD is None: return ESC.err('Sim not opened.')
    ESC.saveSim()
    mdl_tuple=(ESC.SIM_NAME,mdlname)
    new_tuple=(ESC.SIM_NAME,newname)
    if mdl_tuple in ESC.MODEL_ENABLE:
        list_enable=list(ESC.MODEL_ENABLE)
        list_enable.append(new_tuple)
        list_enable.remove(mdl_tuple)
        ESC.setSim({'MODEL_ENABLE':list_enable})
    tmp_value=ESC.ACP_MODELS[mdl_tuple]
    ESC.ACP_MODELS[new_tuple]=tmp_value
    del ESC.ACP_MODELS[mdl_tuple]
    os.rename('sim/'+ESC.SIM_NAME+'/model/'+mdlname+'.py','sim/'+ESC.SIM_NAME+'/model/'+newname+'.py')
    ESC.saveSim()
    return
