import time
from core import esc as ESC
import mod
def runSim(itoritems=['time']):
    # s=time.time()
    'Lv1: Run Sim with iterators, time default;'
    if ESC.SIM_FD is None: return ESC.bug('E: Sim not opened.')
    if ESC.CORE_STAUS=='BUSY':return ESC.bug('E: Core busy.')
    ESC.CORE_STAUS='BUSY'

    # Collect providers and iterators;
    if len(ESC.ACPS_PREPARED['Providers'])==0:
        for model,acplist in ESC.ACP_MODELS.items():
            if model in ESC.MODEL_DISABLE:continue
            for acp in acplist:
                if isinstance(acp,mod.AroCore.AcpIterator) and acp.item in itoritems:
                    if acp.item not in ESC.ACPS_PREPARED['Iterators']:
                        ESC.ACPS_PREPARED['Iterators'][acp.item]=list()
                    if acp not in ESC.ACPS_PREPARED['Iterators'][acp.item]:
                        ESC.ACPS_PREPARED['Iterators'][acp.item].append(acp)
                elif isinstance(acp,mod.AroCore.AcpProvider):
                    if model not in ESC.ACPS_PREPARED['Providers']:ESC.ACPS_PREPARED['Providers'][model]=list()
                    ESC.ACPS_PREPARED['Providers'][model].append(acp)
                elif isinstance(acp,mod.AroCore.AcpExecutor):
                    if model not in ESC.ACPS_PREPARED['Executors']:ESC.ACPS_PREPARED['Executors'][model]=list()
                    ESC.ACPS_PREPARED['Executors'][model].append(acp)
    itors=ESC.ACPS_PREPARED['Iterators']
    pvdrs=ESC.ACPS_PREPARED['Providers']
    excrs=ESC.ACPS_PREPARED['Executors']

    # Snapshot preparing;
    ESC.MAP_QUEUE.append(list(ESC.ARO_MAP))
    if len(ESC.MAP_QUEUE)>ESC.SIM_QUEUE_LEN:
        ESC.MAP_QUEUE=ESC.MAP_QUEUE[1:]

    # Static;
    if not ESC.STATIC_PREPARED:
        travesalAcps(pvdrs,static=True)
        ESC.STATIC_PREPARED=True
    if len(itors.keys())==0:
        ESC.CORE_STAUS='STOP'
        ESC.bug('I: Static running done.')
    elif len(itors.keys())==1:
        # Single dimension;
        if ESC.SIM_REALTIME:
            for itor in list(itors.values())[0]:
                itor.iterate()
            travesalAcps(pvdrs)
            travesalAcps(excrs)
            if ESC.CORE_STAUS!='STOP':
                ESC.CORE_STAUS='READY'
        else:
            'todo: not realtime simulation;'
            while not itor.iterate():
                travesalAcps(pvdrs)
                travesalAcps(excrs)
            ESC.CORE_STAUS='STOP'
    else:
        # Multi-dimension;
        'todo: multi-dimension simulation;'
    # print(s-time.time())

    return

def travesalAcps(acps,static=False):
    for model,acplist in acps.items():
        for acp in acplist:
            if (static and acp.static) or not acp.static:
                reqAcp(acp,model)
                if ESC.CORE_STAUS=='STOP':
                    return
    return

def reqAcp(acp,acpmodel,paradict={}):
    ''' Lv2: Request Acp.

        Para acp accepts str for Acpname,

        int for AcpID or Acp self;'''
    # Para check;
    # if type(acp) is str:
    #     for anl in ESC.ACP_MODELS[acpmodel]:
    #         if anl.AcpName==acp:
    #             acp=anl
    #             break
    #     if type(acp) is str:return ESC.bug('E: AcpName not existed.')
    # elif type(acp) is int:
    #     acp=ESC.getAcp(acp,acpmodel)
    #     if type(acp) is str:return ESC.bug(acp)

    # Needed var;
    acproot=acp
    stack=list()
    stack.append(acproot)
    datadict=dict()
    datadict.update(paradict)
    if len(ESC.MAP_QUEUE)==0:ESC.MAP_QUEUE.append(list(ESC.ARO_MAP))

    # Main travesal;
    while len(stack)!=0:
        if len(stack)>ESC.ACP_DEPTH:return ESC.bug('E: Acp too deep.')
        acp=stack[-1]
        if acp.static and (acpmodel[0],acpmodel[1],acp.AcpID) in ESC.STATIC_DICT:
            datadict.update(ESC.STATIC_DICT[acpmodel+(acp.AcpID)])
            stack.pop()
            continue

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
            try:ret=acp.postProgress(datadict)
            except BaseException as e:
                ESC.bug('E: Post progressing in '+acp.AcpName+' '+str(e))
                ESC.CORE_STAUS='STOP'
                return None,None
            datadict.update(ret)
            stack.pop()
        elif in_ready:
            # Inport all ready, calculate Acp;
            try:ret=acp.AcpProgress(datadict)
            except BaseException as e:
                ESC.bug('E: Acp progressing in '+acp.AcpName+' '+str(e))
                ESC.CORE_STAUS='STOP'
                return None,None
            datadict.update(ret)
            if acp.static:
                ESC.STATIC_DICT[(acpmodel[0],acpmodel[1],acp.AcpID)]=ret
        continue

    return datadict
