import os
from core import esc as ESC
import mod
def getModelPath(mdl):
    ''' Get model path even not existed.
    * Para mdl: model tuple like (sim,model);'''
    if mdl[0]==ESC.SIM_NAME:
        path='sim/'+mdl[0]+'/mdl/'+mdl[1]+'.py'
    else:
        path='mod/'+mdl[0]+'/mdl/'+mdl[1]+'.py'
    return path

def newModelFile(mdlname):
    'Lv2: Create a new model in opened sim.'
    if not ESC.isSimOpened():ESC.err('Sim not opened.')
    model_tuple=(ESC.SIM_NAME,mdlname)
    if model_tuple not in ESC.ACP_MODELS:
        ESC.ACP_MODELS[model_tuple]=list()
    else:ESC.err('Model name already existed.')
    return

def saveModelFile(mdl=None):
    ''' Update model files by ESC.ACP_MODELS.
    * Para mdl: None defa mdl tuple for all models;'''
    # if not ESC.isSimOpened():return ESC.err('Sim not opened.')
    if mdl is None:models=list(ESC.ACP_MODELS.keys())
    else: models=[mdl]

    for model in models:
        # Build index and key dict;
        acp_index=[acp.acpid.value for acp in ESC.ACP_MODELS[model]]
        key_dict=dict()
        acp:ESC.Acp
        txt='ACP_INDEX='+str(acp_index)+'\n'
        for acp in ESC.ACP_MODELS[model]:
            acpo=acp.getAcpo()
            for k,v in acpo.items():
                if k not in key_dict:
                    key_dict[k]=len(key_dict)+1
            for attr,num in key_dict.items():
                if attr in acpo:
                    acpo[num]=acpo[attr]
                    del acpo[attr]
            txt+='Acp_'+str(acp.acpid.value)+'='+str(acpo)+'\n'

        txt+='KEY_DICT='+str(key_dict)+'\n'
        path=ESC.getModelPath(model)
        with open(path,'w+') as model_fd:
            model_fd.truncate()
            model_fd.write(txt)
    return

def loadModelFile(mdl):
    ''' Load model from file;'''
    if not ESC.isSimOpened():ESC.err('Sim not opened.')
    if mdl not in ESC.ACP_MODELS:ESC.ACP_MODELS[mdl]=list()
    path=ESC.getModelPath(mdl)
    with open(path,'r') as model_fd:
        content=model_fd.read()
    _locals=dict(locals())
    exec(content,globals(),_locals)
    ACP_INDEX=_locals['ACP_INDEX']
    KEY_DICT=_locals['KEY_DICT']
    for acpid in ACP_INDEX:
        acpo=_locals['Acp_'+str(acpid)]
        for attr,idx in KEY_DICT.items():
            if idx in acpo:
                acpo[attr]=acpo[idx]
                del acpo[idx]
        ESC.loadAcp(mdl,**acpo)
    return

def renameModelFile(mdlname,newname):
    'Rename model in sim.'
    if not ESC.isSimOpened(): return ESC.err('Sim not opened.')
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
