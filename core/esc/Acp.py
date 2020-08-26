import mod
from core import esc as ESC
def getAcp(acpid,acpmodel):
    'Lv1: Get Acp by AcpID;'
    for model,acplist in ESC.ACP_MODELS.items():
        if model==acpmodel:
            for acp in acplist:
                if acp.AcpID==acpid: return acp
    return

def addAcp(acpclass,acpmodel):
    'Lv1: Add an Acp into list. Return added Acp;'
    if type(acpclass)==str:acp=eval(acpclass+'()')
    else:acp=acpclass()
    ESC.ACPID_MAX[acpmodel]+=1
    acp.AcpID=ESC.ACPID_MAX[acpmodel]
    ESC.ACP_MODELS[acpmodel].append(acp)
    return acp

def setAcp(acp,acpo,acpmodel):
    '''Lv2: Set Acp with acpo dict.

        AcpID shouldnt be set manually.

        Para acp: Accept AcpID and Acp:'''
    if type(acp)==int:
        acp=getAcp(acp,acpmodel)
    elif type(acp)==str:
        pass
    ava_acpo=dict()
    for k,v in acpo.items():
        if k in acp.__dict__:
            ava_acpo[k]=v
    acp.__dict__.update(ava_acpo)
    if 'AcpID' in acpo:
        ESC.ACPID_MAX[acpmodel]=max(acpo['AcpID'],ESC.ACPID_MAX[acpmodel])
    return acp

def delAcp(acpid,acpmodel):
    'Lv2: Deleted an Acp. Return deleted Acp;'
    acp=getAcp(acpid,acpmodel)
    for ip,ip_tar in acp.inport.items():
        if ip_tar is None:continue
        acpid=ip_tar[0]
        port=ip_tar[1]
        tar_acp=getAcp(acpid,acpmodel)
        tar_acp.outport[port].remove((acp.AcpID,ip))
    for op,op_tar_list in acp.outport.items():
        if op_tar_list==[]:continue
        for op_tar in op_tar_list:
            acpid=op_tar[0]
            port=op_tar[1]
            tar_acp=getAcp(acpid,acpmodel)
            tar_acp.inport[port]=None
    ESC.ACP_MODELS[acpmodel].remove(acp)
    return acp

def initAcp(acpclass,acpo,acpmodel):
    '''Lv3: Add an Acp with initilization.

        Acpo must contain AcpID;'''
    acp=addAcp(acpclass,acpmodel)
    acp=ESC.setAcp(acp.AcpID,acpo,acpmodel)
    return acp

def connectAcp(sid,stport,eid,edport,acpmodel):
    ''' Lv.2: Connect Acp port.

        Return 1 for connection while 0 for disconnetion.

        Repeat ports to remove this connection.

        Inport only accepts one while outport can accept more;'''
    sacp=getAcp(sid,acpmodel)
    eacp=getAcp(eid,acpmodel)
    s_combo=(sid,stport)
    e_combo=(eid,edport)
    if stport in sacp.outport:
        # Outport to inport;
        if edport in eacp.inport:
            if eacp.inport[edport] is None:
                # New connection;
                eacp.inport[edport]=s_combo
                sacp.outport[stport].append(e_combo)
                return 1
            elif eacp.inport[edport]==s_combo:
                # Delete connection;
                eacp.inport[edport]=None
                sacp.outport[stport].remove(e_combo)
                return 0
            else:return ESC.bug('E: End inport already connected.')
        else:return ESC.bug('E: End inport not existed.')
    elif stport in sacp.inport:
        # Inport to outport;
        if edport in eacp.outport:
            if s_combo not in eacp.outport[edport]:
                # New connection;
                eacp.outport[edport].append(s_combo)
                sacp.inport[stport]=e_combo
                return 1
            else:
                # Delete connection;
                eacp.outport[edport].remove(s_combo)
                sacp.inport[stport]=None
                return 0
        else:return ESC.bug('E: End outport not existed.')
    else:return ESC.bug('E: Start port not existed.')
    return
