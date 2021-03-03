import os
import numpy as np
from core import esc as ESC
inf=np.inf

def newMapFile(mapname):
    if not ESC.isSimOpened():return ESC.err('Sim not opened.')
    if mapname not in ESC.MAP_LIST:
        saveMapFile()
        ESC.MAP_LIST.append(mapname)
        ESC.ARO_MAP=dict()
        ESC.MAP_ACTIVE=mapname
        saveMapFile(mapname)
    else:
        return ESC.err('Map name already existed.')
    return

def loadMapFile(mapname=''):
    ''' Read existed map.py;'''
    if not ESC.isSimOpened():ESC.err('Sim not opened.')
    if mapname=='': mapname=ESC.MAP_ACTIVE
    else: ESC.MAP_ACTIVE=mapname
    ESC.ARO_MAP=dict()
    with open('sim/'+ESC.SIM_NAME+'/map/'+mapname+'.py','r') as map_fd:
        txt=map_fd.read()

    _locals=dict(locals())
    exec(txt,globals(),_locals)
    ESC.ARO_ORDER=_locals['ARO_INDEX']
    key_dict=_locals['KEY_DICT']
    for aroid in ESC.ARO_ORDER:
        aro=_locals['Aro_'+str(aroid)]
        for k,v in key_dict.items():
            if k in aro:
                temp=aro[k]
                del aro[k]
                aro[v]=temp
        ESC.initAro(aro['AroClass'],aro)
    return

def saveMapFile(mapname=''):
    'Lv1: Update map;'
    if not ESC.isSimOpened(): return ESC.err('Sim not opened.')
    if mapname=='': mapname=ESC.MAP_ACTIVE
    # Build index and key dict;
    key_dict=dict()
    for aro in ESC.getFullMap():
        # ESC.ARO_ORDER.append(aro.AroID)
        for k,v in aro.__dict__.items():
            if k[0]=='_':continue
            if k not in key_dict.values():
                key_dict[len(key_dict)+1]=k
    # Complete building;
    txt='ARO_INDEX='+ESC.ARO_ORDER.__str__()+'\n'
    txt+='KEY_DICT='+key_dict.__str__()+'\n'
    # Replace key;
    for aro in ESC.getFullMap():
        temp_dict=dict()
        for k,v in aro.__dict__.items():
            if k[0]!='_':temp_dict[k]=v
        for k,v in key_dict.items():
            if v in temp_dict:
                temp=temp_dict[v]
                del temp_dict[v]
                temp_dict[k]=temp
        txt+='Aro_'+str(aro.AroID)+'='+temp_dict.__str__()+'\n'

    with open('sim/'+ESC.SIM_NAME+'/map/'+mapname+'.py','w+') as map_fd:
        map_fd.truncate()
        map_fd.write(txt)
    return

def renameMapFile(mapname='',newname='NewMap'):
    'Lv1: Rename map;'
    if not ESC.isSimOpened(): return ESC.err('Sim not opened.')
    ESC.saveSim()
    if mapname=='': mapname=ESC.MAP_ACTIVE
    ESC.MAP_ACTIVE=newname
    ESC.MAP_LIST.remove(mapname)
    ESC.MAP_LIST.append(newname)
    os.rename('sim/'+ESC.SIM_NAME+'/map/'+mapname+'.py','sim/'+ESC.SIM_NAME+'/map/'+newname+'.py')
    ESC.saveSim()
    return

def sortMap():
    ''' Sort and update ARO_ORDER.'''
    new_order=list()
    for aroid in ESC.ARO_ORDER:
        tstack=[aroid]
        while len(tstack)!=0:
            node=tstack[-1]
            aro=ESC.getAro(node)
            allow_popout=True
            if hasattr(aro,'children'):
                if aro.AroID not in new_order:
                    new_order.append(aro.AroID)
                for child in aro.children:
                    if child not in new_order:
                        allow_popout=False
                        new_order.append(child)
                        tstack.append(child)
                        break
                    elif new_order.index(child)<new_order.index(aro.AroID):
                        allow_popout=False
                        new_order.remove(child)
                        new_order.append(child)
                        tstack.append(child)
                        break
            if allow_popout:
                if aro.AroID not in new_order:
                    new_order.append(aro.AroID)
                tstack.pop()
    ESC.ARO_ORDER=new_order
    return
