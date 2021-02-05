import sys,os
import numpy as np
import _glm as glm
import OpenGL.GL as gl
from core import ESC,esui,esgl

class VertexLayout(object):
    _dict_default={'pos':(0,3,0),'color':(1,4,12),
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
        self.id=0
        self.name=''
        self.gl_type=gl.GL_TRIANGLES
        self.dict_glo={'VAO':-1,'VBO':-1,'EBO':-1}
        self.dict_layout=argkw.get('layout',[VertexLayout()])
        self.vertices=argkw.get('vertices',np.array([],dtype=np.float32))
        self.edges=argkw.get('edges',np.array([],dtype=np.uint32))
        self.faces=argkw.get('faces',np.array([],dtype=np.uint32))
        self.trans=argkw.get('trans',glm.mat4(1.0))
        return
    pass

# OpenGL drawing part class;
class DrawPart(object):
    ''' Attr: name, gl_type,

        VA, EA, trans, etc..'''
    def __init__(self):
        self.name=''
        self.gl_type=gl.GL_POINTS
        self.list_mesh=list()

        self.visible=True
        self.highlight=False
        self.dict_fix={'fix':False,'pos':False,
            'size':False,'orient':False,'mat':glm.mat4(1.0)}

        self._is_modified=True

        self.dict_layout={'pos':3}
        self.VA=np.array([],dtype=np.float32)
        self.EA=np.array([],dtype=np.uint32)
        self.TA=''
        self.dict_glo={'VAO':-1,'VBO':-1,'EBO':-1,'TAO':-1}
        self.trans=glm.mat4(1.0)

        return

    @staticmethod
    def delDP(self):
        gl.glDeleteVertexArrays(1,self.VAO)
        gl.glDeleteBuffers(1,self.EBO)
        gl.glDeleteBuffers(1,self.VBO)
        return
    pass

class AroDrawPart(DrawPart):
    ''' Para aroid: accept AroID.;'''
    def __init__(self,aroid=None):
        super().__init__()
        self.Aro=ESC.getAro(aroid)
        self.name=self.Aro.AroID
        return

    def updateADP(self):
        ''' Update Adp after reading Aro map, Specificate by ADP self.'''
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

def writeDpFile(dp:DrawPart,path:str):

    return

def readDpFile(path:str):

    return
