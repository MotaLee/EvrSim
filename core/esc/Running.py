import time
from core import esc as ESC
import mod

def runSim(itoritems=None):
    'Lv1: Run Sim with iterators, time default;'
    # s=time.time()
    # if ESC.SIM_FD is None: return ESC.bug('Sim not opened.')
    if ESC.CORE_STAUS=='BUSY':return ESC.bug('Core busy.')
    ESC.CORE_STAUS='BUSY'

    if ESC.COMPILED_MODEL is not None:
        runCompiledSim()
        return

    # Collect providers and iterators;
    if len(ESC.ACPS_PREPARED['Providers'])==0:
        CollectAcps(itoritems)
    itors=ESC.ACPS_PREPARED['Iterators']
    pvdrs=ESC.ACPS_PREPARED['Providers']
    excrs=ESC.ACPS_PREPARED['Executors']

    # Snapshot preparing;
    ESC.MAP_QUEUE.append(dict(ESC.ARO_MAP))
    ESC.MAP_QUEUE=ESC.MAP_QUEUE[0:ESC.SIM_QUEUE_LEN]

    if ESC.CORE_STAUS!='BUSY':return
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

def CollectAcps(itoritems=None):
    if itoritems is None:itoritems=['time']
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
    return

def travesalAcps(acps,static=False):
    global datadict
    for model,acplist in acps.items():
        ESC.DATADICT=dict()
        acplen=len(acplist)
        for i in range(0,acplen):
            if (static and acplist[i].static) or not acplist[i].static:
                reqAcp(acplist[i],model)
                if ESC.CORE_STAUS=='STOP':
                    return
    return

def reqAcp(acp,acpmodel):
    ''' Lv2: Request Acp.'''
    # Needed var;
    datadict=ESC.DATADICT
    stack=list()
    track=list()
    stack.append(acp)
    if len(ESC.MAP_QUEUE)==0:
        ESC.MAP_QUEUE.append(dict(ESC.ARO_MAP))

    # Main travesal;
    while len(stack)!=0:
        if len(stack)>ESC.ACP_DEPTH:return ESC.bug('Acp too deep.')
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
                ESC.bug('Post progressing in '+acp.AcpName+' '+str(e))
                ESC.CORE_STAUS='STOP'
                return None,None
            datadict.update(ret)
            stack.pop()
            track.append(acp)
        elif in_ready:
            # Inport all ready, calculate Acp;
            try:ret=acp.AcpProgress(datadict)
            except BaseException as e:
                ESC.bug('Acp progressing in '+acp.AcpName+' '+str(e))
                ESC.CORE_STAUS='STOP'
                return None,None
            datadict.update(ret)
            if acp.static:
                ESC.STATIC_DICT[(acpmodel[0],acpmodel[1],acp.AcpID)]=ret
        continue

    return datadict,track

def runCompiledSim():
    # s=time.time()
    if ESC.COMPILED_MODEL is None:
        compileModel()
    set_dict=dict()
    for ii in ESC.COMPILED_MODEL['ITOR']:
        ii.iterate()

    for oi in ESC.COMPILED_MODEL['OUTPUT']:
        aroid=oi[0]
        datadict={'REQ':[aroid]}
        arove=ESC.COMPILED_MODEL['AROVE_INDEX'][oi[1]]
        for acp in ESC.COMPILED_MODEL['TRACK_INDEX'][oi[2]]:
            if isinstance(acp,mod.AroCore.AcpProvider):
                out=datadict[acp.inport[1]][aroid]
                if len(out[0])==1:out=out[0][0]
                else:out=out[0]
            elif isinstance(acp,mod.AroCore.AcpSelector):
                reslist=ESC.COMPILED_MODEL['INPUT'][(id(acp),aroid)]
                resdata=list()
                for resid in reslist:
                    data=getattr(ESC.getAro(resid),acp.item)
                    if not isinstance(data,list):data=[data]
                    resdata.append(data)
                if len(resdata)==0:resdata=[acp.default]
                datadict.update({(acp.AcpID,1):{aroid:resdata}})
            else:
                ret=acp.AcpProgress(datadict)
                datadict.update(ret)
        if aroid not in set_dict:set_dict[aroid]=dict()
        set_dict[aroid].update({arove:out})

    for aroid,arove in set_dict.items():
        ESC.setAro(aroid,arove)
    for ei in ESC.COMPILED_MODEL['EXCR']:
        ei.postProgress({})
    if ESC.CORE_STAUS!='STOP':
        ESC.CORE_STAUS='READY'
    # print(time.time()-s)
    return

def compileModel(mdl=None):
    CollectAcps()
    pvdrs=ESC.ACPS_PREPARED['Providers']
    excrs=ESC.ACPS_PREPARED['Executors']
    itors=ESC.ACPS_PREPARED['Iterators']

    INPUT=dict()
    OUTPUT=list()
    EXCR=list()
    ITOR=list()
    AROVE_INDEX=list()
    TRACK_INDEX=list()

    for model,pvdrlist in pvdrs.items():
        for pvdr in pvdrlist:
            ESC.DATADICT=dict()
            datadict,track=ESC.reqAcp(pvdr,model)
            reqlist=datadict['REQ']
            if pvdr.item in AROVE_INDEX:
                api=AROVE_INDEX.index(pvdr.item)
            else:
                AROVE_INDEX.append(pvdr.item)
                api=len(AROVE_INDEX)-1
            if track in TRACK_INDEX:
                ati=TRACK_INDEX.index(track)
            else:
                TRACK_INDEX.append(track)
                ati=len(TRACK_INDEX)-1
            for aroid in reqlist:
                OUTPUT.append([aroid,api,ati])
                for acp in track:
                    if isinstance(acp,mod.AroCore.AcpSelector):
                        resdict=datadict[(acp.AcpID,'RES')]
                        INPUT.update({(id(acp),aroid):resdict[aroid]})
    for model,excrlist in excrs.items():
        for _excr in excrlist:
            EXCR.append(_excr)
    for model,itorlist in itors.items():
        for _itor in itorlist:
            ITOR.append(_itor)
    ESC.COMPILED_MODEL={'INPUT':INPUT,
        'OUTPUT':OUTPUT,
        'EXCR':EXCR,
        'ITOR':ITOR,
        'AROVE_INDEX':AROVE_INDEX,
        'TRACK_INDEX':TRACK_INDEX}

    ESC.resetSim()
    return
