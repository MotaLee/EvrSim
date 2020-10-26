import math
import mod
import numpy as np
from core import esc as ESC
def getAro(aroid,queue=-1):
    'Lv1: Get Aro by ID. Return Aro if succeed, None if failed;'
    if queue==-1:aromap=ESC.ARO_MAP
    else:aromap=ESC.MAP_QUEUE[queue]
    if aroid in aromap:return aromap[aroid]
    else:return None
    return

def getAroByName(aroname):
    'Lv1: Get Aro by name. Return Aro if succeed, bugstr if failed;'
    for aro in ESC.ARO_MAP.values():
        if aro.AroName==aroname:return aro
    return ESC.bug('E: Aro name not found.')

def addAro(aroclass,aroid=0):
    ''' Lv1: Add an Aro without initilization.

        Return Aro if succeed;'''
    if type(aroclass)==str:aro=eval(aroclass+'()')
    else:aro=aroclass()
    if aroid==0:
        aro.AroID=max(ESC.ARO_ORDER)+1
    else:
        aro.AroID=aroid
    ESC.ARO_MAP[aro.AroID]=aro
    if aro.AroID not in ESC.ARO_ORDER:
        ESC.ARO_ORDER.append(aro.AroID)
    return aro

def delAro(aro):
    'Lv2: Return deleted Aro if succeed;'
    if isinstance(aro,int):aro=ESC.getAro(aro)
    aro.onDel()
    del ESC.ARO_MAP[aro.AroID]
    ESC.ARO_ORDER.remove(aro.AroID)
    return aro

def initAro(aroclass,arove):
    'Lv3: Add an Aro with initilization;'
    for k,v in arove.items():
        if v=='inf':arove[k]=math.inf
        if type(v)==list:
            temp=list()
            for ve in v:
                if ve=='inf':temp.append(math.inf)
                else:temp.append(ve)
            arove[k]=temp
    aro=addAro(aroclass,arove.get('AroID',0))
    aro.onInit(arove)
    # if 'AroID' in arove:
    #     k,v=list(ESC.ARO_MAP.items())[-1]
    #     if k!=v.AroID:
    #         ESC.ARO_MAP[aro.AroID]=aro
    #         del ESC.ARO_MAP[k]
    #     ESC.AROID_MAX=max(arove['AroID'],ESC.AROID_MAX)

    return aro

def setAro(aroid,arove):
    ''' Lv2: Set Arove with Arove dict.

        AroID, AroClass shouldnt be set;'''
    aro=getAro(aroid)
    for k,v in arove.items():
        if type(v)==str:
            if v=='inf':arove[k]=math.inf
        elif type(v)==list:
            temp=list()
            for ve in v:
                if ve=='inf':temp.append(math.inf)
                else:temp.append(ve)
            arove[k]=temp
        elif type(v)==np.array:
            arove[k]=v.tolist()
        if k not in aro.__dict__:continue
        setattr(aro,k,v)
    aro.onSet(arove)
    return

def sortAro(srcs,tar,direction='after'):
    ''' Para srcs/tar: Accept Aro;'''
    new_list=list()
    for aro in srcs:
        ESC.ARO_ORDER.remove(aro.AroID)
        new_list.append(aro.AroID)
    tar_index=ESC.ARO_ORDER.index(tar.AroID)
    for newid in new_list:
        ESC.ARO_ORDER.insert(tar_index+1,newid)
    ESC.sortAroMap()
    return
