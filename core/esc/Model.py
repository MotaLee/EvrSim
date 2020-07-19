from core import esc as ESC
def getModelPath(acpmodel):
    'Lv1: Get model path even not existed.'
    if acpmodel[0]==ESC.SIM_NAME:
        path='sim/'+acpmodel[0]+'/model/'+acpmodel[1]+'.py'
    else:
        path='mod/'+acpmodel[0]+'/model/'+acpmodel[1]+'.py'
    return path

def newModelFile(modelname):
    'Lv2: Create a new model in opened sim.'
    if ESC.SIM_FD is None:return ESC.bug('E: Sim not opened.')
    if modelname not in ESC.ACP_MAP:
        ESC.ACP_MAP[(ESC.SIM_NAME,modelname)]=list()
        ESC.ACPID_MAX[(ESC.SIM_NAME,modelname)]=0
    else:
        return ESC.bug('E: Model name already existed.')
    return

def updateModelFile(acpmodel=None):
    ''' Lv2: Update model files by ESC.ACP_MAP.

        Empty para acpmodel for all models;'''
    if ESC.SIM_FD is None:return ESC.bug('E: Sim not opened.')
    if acpmodel is None:
        models=list(ESC.ACP_MAP.keys())
    else: models=[acpmodel]

    for model in models:
        # Build index and key dict;
        acp_index=[]
        key_dict=dict()
        for acp in ESC.ACP_MAP[model]:
            acp_index.append(acp.AcpID)
            for k,v in acp.__dict__.items():
                if k not in key_dict.values():
                    key_dict[len(key_dict)+1]=k
        # Complete building;
        txt='ACP_INDEX='+acp_index.__str__()+'\n'
        txt+='KEY_DICT='+key_dict.__str__()+'\n'
        # Replace key;
        for acp in ESC.ACP_MAP[model]:
            temp_dict=dict(acp.__dict__)
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

def loadModelFile(acpmodel):
    ''' Lv2: Load model from file;'''
    if ESC.SIM_FD is None:return ESC.bug('E: Sim not opened.')
    path=ESC.getModelPath(acpmodel)
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
        ESC.initAcp(acp['AcpClass'],acp,acpmodel)
    return
