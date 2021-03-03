import multiprocessing as mp
from multiprocessing.queues import Queue
from multiprocessing.managers import BaseManager

from core import esc as ESC
import mod

def CollectAcps(itoritems=None):
    if itoritems is None:itoritems=['time']
    for model,acplist in ESC.ACP_MODELS.items():
        if model not in ESC.MODEL_ENABLE:continue
        for acp in acplist:
            if isinstance(acp,ESC.AcpIterator) and acp.getAcpo('item') in itoritems:
                if acp.item not in ESC.ACPS_PREPARED['Iterators']:
                    ESC.ACPS_PREPARED['Iterators'][acp.item]=list()
                if acp not in ESC.ACPS_PREPARED['Iterators'][acp.item]:
                    ESC.ACPS_PREPARED['Iterators'][acp.item].append(acp)
            elif isinstance(acp,ESC.AcpProvider):
                if model not in ESC.ACPS_PREPARED['Providers']:ESC.ACPS_PREPARED['Providers'][model]=list()
                ESC.ACPS_PREPARED['Providers'][model].append(acp)
            elif isinstance(acp,ESC.AcpExecutor):
                if model not in ESC.ACPS_PREPARED['Executors']:ESC.ACPS_PREPARED['Executors'][model]=list()
                ESC.ACPS_PREPARED['Executors'][model].append(acp)
    return

def reqAcp(acp:ESC.Acp,mdl):
    ''' Request Acp.'''
    # Needed var;
    datadict=ESC.DATADICT
    stack=list()
    track=list()
    stack.append(acp)
    if len(ESC.MAP_QUEUE)==0:
        ESC.MAP_QUEUE.append(dict(ESC.ARO_MAP))

    # Main travesal;
    while len(stack)!=0:
        # if len(stack)>ESC.max_acp_depth:ESC.err('Acp too deep.')
        acp=stack[-1]
        acpid=acp.getAcpo('acpid')
        # Requesting check;
        if hasattr(acp,'preProgress'):acp.preProgress()
        # IOports check;
        out_ready=True
        for port in acp.getPort(io='out'):
            if (acpid,port.pid) not in datadict:
                out_ready=False
                break
        in_ready=True
        for port in acp.getPort(io='in'):

            if port.link[0] not in datadict:
                in_ready=False
                stack.append(ESC.getAcp(port.link[0][0],mdl))
                break
        # Checked;
        if out_ready and in_ready:
            # All ready, post progress;
            try:
                if hasattr(acp,'postProgress'):
                    acp.postProgress()
            except BaseException as e:
                ESC.CORE_STATUS.setStop()
                ESC.err('Post progressing in '+acp.acp_namee+' '+str(e))
            stack.pop()
            track.append(acp)
        elif in_ready:
            # Inport all ready, calculate Acp;
            try:
                if hasattr(acp,'AcpProgress'):
                    acp.AcpProgress()
            except BaseException as e:
                ESC.CORE_STATUS.setStop()
                ESC.err('Acp progressing in '+acp.getAcpo('acp_name')+' '+str(e))
        continue

    return track

def runCompiledSim():
    # s=time.time()
    if ESC.COMPILED_MODEL is None:compileModel()
    set_dict=dict()
    for ii in ESC.COMPILED_MODEL['ITOR']:
        ii:ESC.AcpIterator
        ii.iterate()

    for oi in ESC.COMPILED_MODEL['OUTPUT']:
        aroid=oi[0]
        ESC.DATADICT={'REQ':[aroid]}
        arove=ESC.COMPILED_MODEL['AROVE_INDEX'][oi[1]]
        for acp in ESC.COMPILED_MODEL['TRACK_INDEX'][oi[2]]:
            if isinstance(acp,ESC.AcpProvider):
                out=ESC.DATADICT[acp.port.value[1].link[0]][aroid]
                if len(out[0])==1:out=out[0][0]
                else:out=out[0]
            elif isinstance(acp,ESC.AcpSelector):
                reslist=ESC.COMPILED_MODEL['INPUT'][(id(acp),aroid)]
                resdata=list()
                for resid in reslist:
                    data=getattr(ESC.getAro(resid),acp.getAcpo('item'))
                    if not isinstance(data,list):data=[data]
                    resdata.append(data)
                if len(resdata)==0:resdata=[acp.getAcpo('default')]
                ESC.DATADICT.update({(acp.getAcpo('acpid'),1):{aroid:resdata}})
            else:
                if hasattr(acp,'AcpProgress'):acp.AcpProgress()
        if aroid not in set_dict:set_dict[aroid]=dict()
        set_dict[aroid].update({arove:out})

    for aroid,arove in set_dict.items():
        ESC.setAro(aroid,arove)
    for ei in ESC.COMPILED_MODEL['EXCR']:
        ei:ESC.AcpExecutor
        ei.execute()
    if not ESC.CORE_STATUS.isStop():
        ESC.CORE_STATUS.setReady()
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
            track=ESC.reqAcp(pvdr,model)
            reqlist=ESC.DATADICT['REQ']
            if pvdr.item.value in AROVE_INDEX:
                api=AROVE_INDEX.index(pvdr.item.value)
            else:
                AROVE_INDEX.append(pvdr.item.value)
                api=len(AROVE_INDEX)-1
            if track in TRACK_INDEX:
                ati=TRACK_INDEX.index(track)
            else:
                TRACK_INDEX.append(track)
                ati=len(TRACK_INDEX)-1
            for aroid in reqlist:
                OUTPUT.append([aroid,api,ati])
                for acp in track:
                    if isinstance(acp,ESC.AcpSelector):
                        resdict=ESC.DATADICT[(acp.getAcpo('acpid'),'RES')]
                        INPUT.update({(id(acp),aroid):resdict[aroid]})
    for model,excrlist in excrs.items():
        for _excr in excrlist:
            EXCR.append(_excr)
    for model,itorlist in itors.items():
        for _itor in itorlist:
            ITOR.append(_itor)
    ESC.COMPILED_MODEL={
        'INPUT':INPUT,
        'OUTPUT':OUTPUT,
        'EXCR':EXCR,
        'ITOR':ITOR,
        'AROVE_INDEX':AROVE_INDEX,
        'TRACK_INDEX':TRACK_INDEX}

    ESC.resetSim()
    return

class EsQueue(Queue):
    def __init__(self):
        super().__init__(ctx=mp.get_context())
        return
    pass
class RunProcess(mp.Process):
    def __init__(self,**argkw):
        ''' EvrSim running process.
            * Para argkw: stdin/stdout;'''
        self.stdin=EsQueue()
        self.stdout=EsQueue()
        super().__init__(target=self.running, daemon=True)

        # manager = BaseManager()
        # # 一定要在start前注册，不然就注册无效
        # manager.register('CoreSt', Test)
        # manager.start()
        # obj = manager.Test()
        return

    def running(self):
        global ESC
        if ESC.CORE_STATUS.isReady():
            ESC.info('ready')
        return

    def send(self,cmd):

        return

    def recv(self):
        return None
    pass
