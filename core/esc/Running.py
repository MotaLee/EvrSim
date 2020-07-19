from core import esc as ESC
import mod
def runSim(itorlist=['time']):
    'Lv1: Run Sim with iterators, time default;'
    if ESC.SIM_FD is None: return ESC.bug('E: Sim not opened.')
    if ESC.CORE_STAUS=='BUSY':return ESC.bug('E: Core busy.')
    ESC.CORE_STAUS='BUSY'

    # Collect providers and iterators;
    pvdrs=dict()
    itors=dict()
    for model,acplist in ESC.ACP_MAP.items():
        if model in ESC.MODEL_DISABLE:continue
        for acp in acplist:
            if isinstance(acp,mod.AroCore.AcpIterator) and acp.item in itorlist:
                if model not in itors:itors[model]=list()
                if acp not in itors[model]:itors[model].append(acp)
            elif isinstance(acp,mod.AroCore.AcpProvider):
                if model not in pvdrs:pvdrs[model]=list()
                pvdrs[model].append(acp)

    # Snapshot preparing;
    ESC.ARO_QUEUE.append(list(ESC.ARO_MAP))
    if len(ESC.ARO_QUEUE)>ESC.SIM_QUEUE_LEN:
        ESC.ARO_QUEUE=ESC.ARO_QUEUE[1:]

    if len(itors.values())==0:  # Static;
        travesalPvdrs(pvdrs)
        'todo: convergence check;'
        ESC.CORE_STAUS='STOP'
    elif len(itors.values())==1:    # Single dimension;
        itor=list(itors.values())[0][0]
        if ESC.SIM_REALTIME:
            itor.iterate()
            travesalPvdrs(pvdrs)
            if ESC.CORE_STAUS!='STOP':
                ESC.CORE_STAUS='READY'
        else:
            'todo: not realtime simulation;'
            while not itor.iterate():
                travesalPvdrs(pvdrs)
            ESC.CORE_STAUS='STOP'
    else:
        # Multi-dimension;
        'todo: multi-dimension simulation;'

    return

def travesalPvdrs(pvdrs):
    for model,pvdrlist in pvdrs.items():
        for pvdr in pvdrlist:
            data=reqAcp(pvdr,model)
            if ESC.CORE_STAUS=='STOP':
                return None,None
    return data

def reqAcp(acp,acpmodel,paradict={}):
    ''' Lv2: Request Acp.

        Para acp accepts str for Acpname,

        int for AcpID or Acp self;'''
    # Para check;
    if type(acp) is str:
        for anl in ESC.ACP_MAP[acpmodel]:
            if anl.AcpName==acp:
                acp=anl
                break
        if type(acp) is str:return ESC.bug('E: AcpName not existed.')
    elif type(acp) is int:
        acp=ESC.getAcp(acp,acpmodel)
        if type(acp) is str:return ESC.bug(acp)

    # Needed var;
    acproot=acp
    stack=list()
    stack.append(acproot)
    datadict=dict()
    datadict.update(paradict)
    if len(ESC.ARO_QUEUE)==0:ESC.ARO_QUEUE.append(list(ESC.ARO_MAP))

    # Main travesal;
    while len(stack)!=0:
        if len(stack)>ESC.ACP_DEPTH:return ESC.bug('E: Acp too deep.')
        acp=stack[-1]
        # Requesting check;
        datadict.update(acp.preProgress(datadict))
        # IOports check;
        out_ready=True
        for port in acp.outport.keys():
            if (acp.AcpID,port) not in datadict:
                out_ready=False
                break
        in_ready=True
        for vout in acp.inport.values():
            if vout not in datadict:
                in_ready=False
                stack.append(ESC.getAcp(vout[0],acpmodel))
                break
        # Checked;
        if out_ready and in_ready:
            # All ready, post progress;
            datadict.update(acp.postProgress(datadict))
            stack.pop()
        elif in_ready:
            # Inport all ready, calculate Acp;
            try:ret=acp.AcpProgress(datadict)
            except BaseException as e:
                ESC.bug('E: Acp progressing in'+acp.AcpName+' raised '+str(e))
                ESC.CORE_STAUS='STOP'
                return None,None
            datadict.update(ret)
        continue

    return datadict
