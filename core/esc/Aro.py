import mod
from core import esc as ESC
def getAro(aroid):
    'Lv1: Get Aro by ID. Return Aro if succeed, None if failed;'
    for aro in ESC.ARO_MAP:
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
    ESC.ARO_MAP.remove(aro)
    return aro

def initAro(aroclass,arove):
    'Lv3: Add an Aro with initilization;'
    aro=addAro(aroclass)
    setAro(aro.AroID,arove)
    return aro

def setAro(aroid,arove):
    ''' Lv2: Set Arove with Arove dict.

        AroID, AroClass shouldnt be set;'''
    aro=getAro(aroid)
    aro.onSet(arove)
    if 'AroID' in arove:
        ESC.AROID_MAX=max(arove['AroID'],ESC.AROID_MAX)
    return
