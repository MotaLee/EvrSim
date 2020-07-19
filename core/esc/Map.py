from core import esc as ESC
# def updateMap():
#     ''' Lv.1: Update all Aroves in current Aro map;'''
#     for aro in ESC.ARO_MAP:
#         aro.onSet()
#     return

def newMapFile(mapname):
    if ESC.SIM_FD is None:return ESC.bug('E: Sim not opened.')
    if mapname not in ESC.ARO_MAP_LIST:
        updateMapFile()
        ESC.ARO_MAP_LIST.append(mapname)
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
            if k not in key_dict.values():
                key_dict[len(key_dict)+1]=k
    # Complete building;
    txt='ARO_INDEX='+aro_index.__str__()+'\n'
    txt+='KEY_DICT='+key_dict.__str__()+'\n'
    # Replace key;
    for aro in ESC.ARO_MAP:
        temp_dict=dict(aro.__dict__)
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
