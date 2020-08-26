import os
from core import esc as ESC
def newMapFile(mapname):
    if ESC.SIM_FD is None:return ESC.bug('E: Sim not opened.')
    if mapname not in ESC.MAP_LIST:
        updateMapFile()
        ESC.MAP_LIST.append(mapname)
        ESC.ARO_MAP=list()
        ESC.ARO_MAP_NAME=mapname
        updateMapFile(mapname)
    else:
        return ESC.bug('E: Map name already existed.')
    return

def loadMapFile(mapname=''):
    ''' Lv.1: Read existed map.py;'''
    if ESC.SIM_FD is None: return ESC.bug('E: Sim not opened.')
    if mapname=='': mapname=ESC.ARO_MAP_NAME
    else: ESC.ARO_MAP_NAME=mapname
    ESC.ARO_MAP=list()
    with open('sim/'+ESC.SIM_NAME+'/map/'+mapname+'.py','r') as map_fd:
        txt=map_fd.read()
    _locals=dict(locals())
    exec(txt,globals(),_locals)
    aro_index=_locals['ARO_INDEX']
    key_dict=_locals['KEY_DICT']
    for aroid in aro_index:
        aro=_locals['Aro_'+str(aroid)]
        for k,v in key_dict.items():
            if k in aro:
                temp=aro[k]
                del aro[k]
                aro[v]=temp
        ESC.initAro(aro['AroClass'],aro)
    return

def updateMapFile(mapname=''):
    'Lv1: Update map;'
    if ESC.SIM_FD is None: return ESC.bug('E: Sim not opened.')
    if mapname=='': mapname=ESC.ARO_MAP_NAME
    # Build index and key dict;
    aro_index=[]
    key_dict=dict()
    for aro in ESC.ARO_MAP:
        aro_index.append(aro.AroID)
        for k,v in aro.__dict__.items():
            if k[0]=='_':continue
            if k not in key_dict.values():
                key_dict[len(key_dict)+1]=k
    # Complete building;
    txt='ARO_INDEX='+aro_index.__str__()+'\n'
    txt+='KEY_DICT='+key_dict.__str__()+'\n'
    # Replace key;
    temp_dict=dict()
    for aro in ESC.ARO_MAP:
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
    if ESC.SIM_FD is None: return ESC.bug('E: Sim not opened.')
    ESC.saveSim()
    if mapname=='': mapname=ESC.ARO_MAP_NAME
    ESC.ARO_MAP_NAME=newname
    ESC.MAP_LIST.remove(mapname)
    ESC.MAP_LIST.append(newname)
    os.rename('sim/'+ESC.SIM_NAME+'/map/'+mapname+'.py','sim/'+ESC.SIM_NAME+'/map/'+newname+'.py')
    ESC.saveSim()
    return
