import os
os.environ['PATH']+=';'+os.getcwd()+'\\lib'
import glm
import numpy as np
import assimp as ai
import mod

# Esgl global variable;
TDP_LIST=list()
ADP_LIST=list()
ASPECT_RATIO=1
VIEW_RATIO=1
WHEEL_DIS=0
FPS=30
EP=np.array([5,5,5])    # Eye point;
AP=np.array([0,0,0])    # Aim point;
UP=np.array([0,1,0])    # Up point;
ZS=1    # Zoom speed;
VIEW_PERP=True   # View perspective mode;

PLC_W=0
PLC_H=0

MAT_PROJ=None
MAT_VIEW=None

from .aroglc import AroGlc
from .drawpart import DrawPart,AroDrawPart,ToolDrawPart
def initADP(aro):
    if aro.adp.find('.')!=-1: prefix=''
    else:
        prefix=aro.__module__[0:aro.__module__.rfind('.')]+'.'
    adp=eval(prefix+aro.adp+'('+str(aro.AroID)+')')
    return adp

def importDPM(path):
    va=None
    ea=None
    sence=ai.load(path)
    va=sence.meshes[0].vertices
    if len(va[0])==3:
        color=np.tile([1,1,1,1],(len(va),1))
        va=np.hstack((va,color))
    va=np.array(va,dtype=np.float32)
    ea=sence.meshes[0].faces
    ea=np.array(ea,dtype=np.uint32)
    return va,ea

def getAngleFrom2Vec3(v1,v2):
    v1=glm.normalize(glm.vec3(v1))
    v2=glm.normalize(glm.vec3(v2))
    agl=glm.acos(glm.dot(v1,v2))
    return agl

def getFixOriMat(oritrans):
    ve_z=glm.vec3(0,0,1)
    v_AE=glm.vec3((EP-AP).tolist())
    r1=rotateToVec(ve_z,v_AE)

    ve_x=glm.vec3(1,0,0)
    ve_xr=glm.vec3(r1*glm.vec4(ve_x,0))
    v_Ax=glm.cross(v_AE,glm.vec3(UP.tolist()))
    r2=rotateToVec(ve_xr,v_Ax)

    ftrans=oritrans*r2*r1
    return ftrans

def getPosFromVertex(drawpart,p):
    if drawpart.fix_orientation:ftrans=getFixOriMat(drawpart.trans)
    else:ftrans=glm.mat4(1.0)
    glm_p=glm.vec4(float(p[0]),float(p[1]),float(p[2]),1.0)
    glm_p=MAT_PROJ*MAT_VIEW*ftrans*glm_p
    px=glm_p[0]/glm_p[3]
    py=glm_p[1]/glm_p[3]
    return (px,py)

def rotateToVec(srcvec,tarvec):
    l1=glm.l1Norm(srcvec)
    l2=glm.l1Norm(tarvec)
    is_zero=l1*l2
    if is_zero==0.0:return glm.mat4(1.0)
    agl=getAngleFrom2Vec3(srcvec,tarvec)
    if glm.cos(agl)==1:return glm.mat4(1.0)
    elif glm.cos(agl)==-1:return glm.mat4(-1.0)
    v_axis=glm.cross(srcvec,tarvec)
    ftrans=glm.rotate(glm.mat4(1.0),agl,v_axis)
    return ftrans
