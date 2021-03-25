import numpy as np
import _glm as glm
from core import ESC,esgl

class VtxLayout(object):
    _dict_default={
        'pos':(0,3,0),'color':(1,4,12),
        'tex':(2,2,12),'normal':(3,3,28)}
    def __init__(self,label='pos') -> None:
        self.label=label
        self.attr=self._dict_default[label][0]
        self.len=self._dict_default[label][1]
        self.offset=self._dict_default[label][2]
        return
    pass
class Mesh(object):
    def __init__(self,**argkw):
        ''' Para argkw: vertices/faces/edges/layout.'''
        self.id=argkw.get('id',0)
        self.name=argkw.get('name','')
        self.draw_type=argkw.get('draw_type',esgl.DT_TRI)
        self.dict_glo={'VAO':-1,'VBO':-1,'EBO':-1,'TAO':-1}
        self.vertices=argkw.get('vertices',np.array([],dtype=np.float32))
        self.edges=argkw.get('edges',np.array([],dtype=np.uint32))
        self.faces=argkw.get('faces',np.array([],dtype=np.uint32))
        self.trans=argkw.get('trans',glm.mat4(1.0))
        self.texture=argkw.get('texture','')
        self.dict_layout={'pos':VtxLayout()}
        dl=argkw.get('layout',[])
        for layout in dl:
            self.dict_layout[layout.label]=layout
        return
    pass

# OpenGL drawing part class;
class DrawPart(object):
    ''' Attr: name, gl_type,VA, EA, trans, etc..'''
    def __init__(self):
        self.name=''
        self.dpclass=ESC.getCls(self)
        self.list_mesh=list()
        self.visible=True
        self.highlight=False
        self.flag_update=True
        self.dict_fix={'fix':False,'pos':False,
            'size':False,'orient':False,'mat':glm.mat4(1.0)}
        self.trans=glm.mat4(1.0)
        return

    def addMesh(self,**argkw):
        mesh=Mesh(**argkw)
        self.list_mesh.append(mesh)
        return

    def getAllVtx(self):
        vtx=self.list_mesh[0].vertices[:,0:3]
        for i in range(1,len(self.list_mesh)):
            vtx2=self.list_mesh[i].vertices[:,0:3]
            vtx=np.hstack((vtx,vtx2))
        return vtx
    pass

class AroDrawPart(DrawPart):
    ''' Para aroid: accept AroID.;'''
    def __init__(self,aroid):
        super().__init__()
        self.Aro=ESC.getAro(aroid)
        self.name=self.Aro.AroID
        return

    def updateAdp(self):
        ''' Update Adp during readMap.
            default for rebind Aro and translate to position.'''
        self.Aro=ESC.getAro(self.name)
        v_p=list(self.Aro.position)
        self.trans=glm.translate(glm.mat4(1.0),v_p)
        return
    pass

class ToolDrawPart(DrawPart):
    ''' Para tool: accept tool.'''
    def __init__(self,tool):
        super().__init__()
        self.tool=tool
        return
    pass
