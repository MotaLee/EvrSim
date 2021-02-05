import json,ctypes
from core import ESC

class PresetStructs(object):
    class DataBlock(ctypes.Structure):
        _fields_=[
            ('inherit',ctypes.pointer*8),
            ("size"),ctypes.c_int
            ('prev',ctypes.pointer),
            ('next',ctypes.pointer),
            ('addr',ctypes.pointer)]
        pass
    pass

class JsonESF(object):
    def __init__(self,esf,**argkw):
        self.version=esf['Header'].get('version',"0.0.12")
        self.extension=esf['Header'].get('extension',"0.0.12")
        self.coding="json"
        self.struct_index=dict()
        for k,v in esf['Index'].items():
            pass
        return
    pass

def loadJsonESF(path):
    esf=None
    try:
        fd=open(path,'r')
        esf=json.load(fd.read())

    except BaseException as e:ESC.bug(e)
    return esf

def saveJsonESF(esf:JsonESF,path):

    return
