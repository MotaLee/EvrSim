import os
import sys
import ctypes
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
import glm
import OpenGL.GL    as gl
import numpy        as np
import assimp       as ai
import PIL.Image    as pil
import mod
from core import ESC,esui
from .detail import DetailDialog
# Esgl global variable;
TDP_LIST=list()
ADP_DICT=dict()
ASPECT_RATIO=1
VIEW_RATIO=1
WHEEL_DIS=0
FPS=30
EP=np.array([5,5,5])    # Eye point;
AP=np.array([0,0,0])    # Aim point;
UP=np.array([0,1,0])    # Up point;
ZS=1    # Zoom speed;
PROJ_MODE=True   # View perspective mode;

PLC_W=0
PLC_H=0

MAT_PROJ=glm.mat4(1.0)
MAT_VIEW=glm.mat4(1.0)

GL_PROGRAM=None

from .aroglc import AroGlc
from .drawpart import DrawPart,AroDrawPart,ToolDrawPart
def initADP(aro):
    if type(aro.adp)!=list:adplist=[aro.adp]
    else: adplist=aro.adp
    outlist=list()
    for adp in adplist:
        if adp.find('.')!=-1: prefix=''
        else:
            prefix=aro.__module__[0:aro.__module__.rfind('.')]+'.'
        adp=eval(prefix+adp+'('+str(aro.AroID)+')')
        outlist.append(adp)
    return outlist

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

def genGLO():
    ''' Generate VAO/VBO/EBO and bind them to GL.'''
    VAO=gl.glGenVertexArrays(1)
    VBO,EBO=gl.glGenBuffers(2)
    return VAO,VBO,EBO

def bindGLO(VAO,VBO,EBO):
    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER,VBO)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER,EBO)
    return

def bindBufferData(VA,EA):
    gl.glBufferData(gl.GL_ARRAY_BUFFER,sys.getsizeof(VA),VA,gl.GL_STREAM_DRAW)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(EA),EA, gl.GL_STREAM_DRAW)
    return

def genGLTexture(imgpath,width=None,height=None):
    texture=0
    gen_tex=gl.glGenTextures(1,texture).value
    gl.glBindTexture(gl.GL_TEXTURE_2D, gen_tex)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,gl.GL_LINEAR)
    img=pil.open(imgpath)
    if img.mode!='RGBA':img=img.convert('RGBA')
    imgdata=np.array(img)
    if width is None:width=img.width
    if height is None:height=img.height
    gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,width,height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,imgdata)
    return gen_tex

def genGLProgram():
    with open('core/esgl/vs.glsl','r') as fd:
        vertexShaderSource=fd.read()
    with open('core/esgl/fs.glsl','r') as fd:
        fragmentShaderSource=fd.read()
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertexShader, vertexShaderSource)
    gl.glCompileShader(vertexShader)
    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragmentShaderSource)
    gl.glCompileShader(fragmentShader)
    gl_program = gl.glCreateProgram()
    gl.glAttachShader(gl_program, vertexShader)
    gl.glAttachShader(gl_program, fragmentShader)
    gl.glLinkProgram(gl_program)
    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)
    gl.glUseProgram(gl_program)
    return gl_program

def projMode(perspective=True):
    global PROJ_MODE,MAT_PROJ
    PROJ_MODE=perspective
    if PROJ_MODE:
        MAT_PROJ=glm.perspective(glm.radians(45),ASPECT_RATIO,0.1,100)
    else:
        b=0.25*WHEEL_DIS+4
        MAT_PROJ=glm.ortho(-1*ASPECT_RATIO*b,ASPECT_RATIO*b,-1*b,b,-100,100)

    proj_loc=gl.glGetUniformLocation(GL_PROGRAM,'projection')
    gl.glUniformMatrix4fv(proj_loc,1,gl.GL_FALSE,glm.value_ptr(MAT_PROJ))
    return

def lookAt(ep=None,ap=None,up=None):
    global EP,AP,UP,MAT_VIEW
    if ep is not None:EP=np.array(ep)
    if ap is not None:AP=np.array(ap)
    if up is not None:UP=np.array(up)
    MAT_VIEW=glm.lookAt(
        glm.vec3(EP.tolist()),
        glm.vec3(AP.tolist()),
        glm.vec3(UP.tolist()))
    view_loc=gl.glGetUniformLocation(GL_PROGRAM,'view')
    gl.glUniformMatrix4fv(view_loc,1,gl.GL_FALSE,glm.value_ptr(MAT_VIEW))
    for adplist in ADP_DICT.values():
        if not isinstance(adplist,list):adplist=[adplist]
        for adp in adplist:
            adp.viewDP()
    esui.ARO_PLC.drawGL()
    return

def drawGL():
    esui.ARO_PLC.drawGL()
    return

def normPos(p):
    px=2*p[0]/esui.ARO_PLC.Size.x-1
    py=1-2*p[1]/esui.ARO_PLC.Size.y
    return (px,py)
