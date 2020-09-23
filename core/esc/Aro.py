import math
import mod
import numpy as np
from core import esc as ESC
def getAro(aroid,queue=0):
    'Lv1: Get Aro by ID. Return Aro if succeed, None if failed;'
    if queue==0:aromap=ESC.ARO_MAP
    else:aromap=ESC.MAP_QUEUE[queue]
    for aro in aromap:
        if aro.AroID==aroid:return aro
    return

def getAroByName(aroname):
    'Lv1: Get Aro by name. Return Aro if succeed, bugstr if failed;'
    for aro in ESC.ARO_MAP:
        if aro.AroName==aroname:return aro
    return ESC.bug('E: Aro name not found.')

def addAro(aroclass):
    ''' Lv1: Add an Aro without initilization.

        Return Aro if succeed;'''
    if type(aroclass)==str:
        aro=eval(aroclass+'()')
    else:aro=aroclass()
    ESC.AROID_MAX+=1
    aro.AroID=ESC.AROID_MAX
    ESC.ARO_MAP.append(aro)
    return aro

def delAro(aroid):
    'Lv2: Return deleted Aro if succeed;'
    aro=ESC.getAro(aroid)
    aro.onDel()
    ESC.ARO_MAP.remove(aro)
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
    aro=addAro(aroclass)
    aro.onInit(arove)
    if 'AroID' in arove:
        ESC.AROID_MAX=max(arove['AroID'],ESC.AROID_MAX)
    return aro

def setAro(aroid,arove):
    ''' Lv2: Set Arove with Arove dict.

        AroID, AroClass shouldnt be set;'''
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
    aro=getAro(aroid)
    aro.onSet(arove)
    return
