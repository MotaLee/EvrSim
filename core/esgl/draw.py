import glm
import numpy as np
import OpenGL.GL as gl
# OpenGL drawing part class;
class GLDrawPart(object):
    'Attr: name, gl_type, VA, EA, trans, Aro, dim'
    def __init__(self,name,func,aro=None):
        self.name=name
        self.gl_type=gl.GL_POINTS
        self.dim=3
        self.highlight=False
        self.VA=np.array([],dtype=np.float32)
        self.EA=np.array([],dtype=np.uint32)
        self.trans=glm.mat4(1.0)
        self.Aro=aro
        self.func=func

        _locals=dict(locals())
        exec('self.'+func+'()',globals(),_locals)
        self.VA=_locals['self'].VA
        self.EA=_locals['self'].EA
        self.gl_type=_locals['self'].gl_type
        self.dim=_locals['self'].dim
        self.trans=_locals['self'].trans
        return

    def updateAro(self,aro):
        self.Aro=aro
        _locals=dict(locals())
        exec('self.'+self.func+'()',globals(),_locals)
        self.VA=_locals['self'].VA
        self.EA=_locals['self'].EA
        self.trans=_locals['self'].trans
        return

    # Preset parts;
    def emp(self):
        return

    def xyzAxis(self):
        self.gl_type=gl.GL_LINES
        self.VA=np.array([
            [0,0,0,     1,0,0,1],
            [.5,0,0,     1,0,0,1],
            [0,0,0,     0,1,0,1],
            [0,.5,0,     0,1,0,1],
            [0,0,0,     0,0,1,1],
            [0,0,.5,     0,0,1,1]],
            dtype=np.float32)
        self.EA=np.array([0,1,2,3,4,5],dtype=np.uint32)
        return

    def xzGrid(self):
        'gap=0.5;'
        self.gl_type=gl.GL_LINES
        self.EA=np.array([],dtype=np.uint32)
        self.VA=np.zeros([44,7],dtype=np.float32)
        for i in range(0,21,2):
            self.VA[i]=[-5/2,0,i/4-2.5,.5,.5,.5,1]
            self.VA[i+1]=[5/2,0,i/4-2.5,.5,.5,.5,1]
            self.VA[i+22]=[i/4-2.5,0,-5/2,.5,.5,.5,1]
            self.VA[i+23]=[i/4-2.5,0,5/2,.5,.5,.5,1]
        return

    def xyGrid(self):
        'gap=0.5;'
        self.gl_type=gl.GL_LINES
        self.EA=np.array([],dtype=np.uint32)
        self.VA=np.zeros([44,7],dtype=np.float32)
        for i in range(0,21,2):
            self.VA[i]=[-5/2,i/4-2.5,0,.5,.5,.5,1]
            self.VA[i+1]=[5/2,i/4-2.5,0,.5,.5,.5,1]
            self.VA[i+22]=[i/4-2.5,-5/2,0,.5,.5,.5,1]
            self.VA[i+23]=[i/4-2.5,5/2,0,.5,.5,.5,1]
        return

    def yzGrid(self):
        'gap=0.5;'
        self.gl_type=gl.GL_LINES
        self.EA=np.array([],dtype=np.uint32)
        self.VA=np.zeros([44,7],dtype=np.float32)
        for i in range(0,21,2):
            self.VA[i]=[0,-5/2,i/4-2.5,.5,.5,.5,1]
            self.VA[i+1]=[0,5/2,i/4-2.5,.5,.5,.5,1]
            self.VA[i+22]=[0,i/4-2.5,-5/2,.5,.5,.5,1]
            self.VA[i+23]=[0,i/4-2.5,5/2,.5,.5,.5,1]
        return

    def point(self):
        self.dim=2
        self.gl_type=gl.GL_LINES
        ps=0.1

        VA=np.array([[0,0,0,1,1,1,1]],dtype=np.float32)
        VA=np.tile(VA,(4,1))
        VA[0][0]+=ps
        VA[1][0]-=ps
        VA[2][1]+=ps
        VA[3][1]-=ps
        self.VA=VA
        self.EA=np.array([0,1,0,2,0,3,1,2,1,3,2,3],dtype=np.uint32)
        self.trans=glm.translate(glm.mat4(1.0),glm.vec3(self.Aro.position))
        return
    pass
