import os,sys,ctypes
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
import glm
import OpenGL.GL as gl
import OpenGL.GLU as glu
import numpy as np
import assimp_py as ai
import PIL.Image as pili
import mod
from core import ESC,esui

# Esgl global variable
ADP_DICT=dict()     # {int AroID:[ins adp,...],...}
TDP_LIST=list()
ASPECT_RATIO=1
VIEW_RATIO=1
WHEEL_DIS=0
FPS=30
EPSILON=1e-4
EP=np.array([5,5,5])    # Eye point
AP=np.array([0,0,0])    # Aim point
UP=np.array([0,1,0])    # Up point
ZS=1    # Zoom speed
ARO_SELECTION=list()    # [ins Aro,...]
PLC_W=0
PLC_H=0
MAT_PROJ=glm.mat4(1.0)
MAT_VIEW=glm.mat4(1.0)

# View option
PROJ_MODE=True   # View perspective mode
WIREFRAME=True
FACE_ALPHA=1
BACK_FACE=False

# Shader needed;
GL_PROGRAM=None
BGC=[0,0,0,0]
LOC_POS=0
LOC_COLOR=0
LOC_HL=0
LOC_HT=0
LOC_TEX=0
LOC_TRANS=0
LOC_PROJ=0

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
    process_flags = (ai.Process_Triangulate | ai.Process_CalcTangentSpace)
    sence=ai.ImportFile(path, process_flags)
    va=sence.meshes[0].vertices
    if len(va[0])==3:
        color=np.tile([0.5,0.5,0.5,1],(len(va),1))
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
    img=pili.open(imgpath)
    if img.mode!='RGBA':img=img.convert('RGBA')
    imgdata=np.array(img)
    if width is None:width=img.width
    if height is None:height=img.height
    gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,width,height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,imgdata)
    return gen_tex

def genGLProgram(vs='default',fs='default'):
    ''' Para vs/fs: Allow 'simple', empty for 'default'.'''
    vs='core/esgl/shaders/'+vs+'_vs.glsl'
    fs='core/esgl/shaders/'+fs+'_fs.glsl'
    with open(vs,'r') as fd:
        vertexShaderSource=fd.read()
    with open(fs,'r') as fd:
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
    global PROJ_MODE,MAT_PROJ,GL_PROGRAM,LOC_PROJ
    PROJ_MODE=perspective
    if PROJ_MODE:
        MAT_PROJ=glm.perspective(glm.radians(45),ASPECT_RATIO,0.1,100)
    else:
        b=0.25*WHEEL_DIS+4
        MAT_PROJ=glm.ortho(-1*ASPECT_RATIO*b,ASPECT_RATIO*b,-1*b,b,-100,100)

    gl.glUniformMatrix4fv(LOC_PROJ,1,gl.GL_FALSE,glm.value_ptr(MAT_PROJ))
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
    drawGL()
    return

def initGL():
    global LOC_COLOR,LOC_POS,LOC_HL,LOC_HT,LOC_TRANS,LOC_TEX,GL_PROGRAM,LOC_PROJ,LOC_TYPE
    gl.glEnable(gl.GL_DEPTH_TEST)   # 开启深度测试，实现遮挡关系
    gl.glEnable(gl.GL_BLEND)            # 开启混合
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)           # 设置混合函数
    # gl.glEnable(gl.GL_LINE_SMOOTH)  # 开启线段反走样
    # glDepthFunc(GL_LEQUAL)      # 设置深度测试函数
    # glShadeModel(GL_SMOOTH)      # GL_SMOOTH(光滑着色)/GL_FLAT(恒定着色)
    # gl.glEnable(gl.GL_ALPHA_TEST)                   # 启用Alpha测试
    # gl.glAlphaFunc(gl.GL_GREATER, 0.1)        # 设置Alpha测试条件为大于05则通过
    # glFrontFace(GL_CW)               # 设置逆时针索引为正面（GL_CCW/GL_CW）
    # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    gl.glClearColor(BGC[0],BGC[1],BGC[2],BGC[3])    # 设置画布背景色
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    GL_PROGRAM=genGLProgram()
    LOC_POS=gl.glGetAttribLocation(GL_PROGRAM,'in_pos')
    LOC_COLOR=gl.glGetAttribLocation(GL_PROGRAM,'in_color')
    LOC_TRANS=gl.glGetUniformLocation(GL_PROGRAM,'trans')
    LOC_HL=gl.glGetUniformLocation(GL_PROGRAM,'highlight')
    LOC_HT=gl.glGetUniformLocation(GL_PROGRAM,'has_texture')
    LOC_TEX=gl.glGetAttribLocation(GL_PROGRAM,'in_texture')
    LOC_PROJ=gl.glGetUniformLocation(GL_PROGRAM,'projection')

    projMode()
    return

def drawGL(mode=0):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    all_adp=list()
    for adplist in ADP_DICT.values():
        all_adp+=adplist
    for dp in TDP_LIST+all_adp:
        if (not dp.visible) or dp.VA.size==0:continue
        if dp.VAO==-1:
            VAO,VBO,EBO=genGLO()
            dp.VAO,dp.VBO,dp.EBO=VAO,VBO,EBO
            bindGLO(VAO,VBO,EBO)
        else:bindGLO(dp.VAO,dp.VBO,dp.EBO)
        if dp.update_data:
            bindBufferData(dp.VA,dp.EA)
            dp.update_data=False

        dp.viewDP()
        vertex_len=len(dp.VA[0])
        gl.glVertexAttribPointer(LOC_POS,3, gl.GL_FLOAT, gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(0))
        gl.glVertexAttribPointer(LOC_COLOR,4,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        if vertex_len>7:
            gl.glUniform1iv(LOC_HT,1,1)
            gl.glVertexAttribPointer(LOC_TEX,2,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(28))
            gl.glEnableVertexAttribArray(2)
            if dp.TAO==-1:
                dp.TAO=genGLTexture(dp.texture)
            else:
                gl.glBindTexture(gl.GL_TEXTURE_2D,dp.TAO)
        else:gl.glUniform1iv(LOC_HT,1,0)

        gl.glUniformMatrix4fv(LOC_TRANS,1,gl.GL_FALSE,glm.value_ptr(dp.ftrans))

        if dp.highlight:hl=1
        else: hl=0
        gl.glUniform1iv(LOC_HL,1,hl)

        if len(dp.EA)!=0:gl.glDrawElements(dp.gl_type,dp.EA.size,gl.GL_UNSIGNED_INT,None)
        # elif len(dp.VA)>1:gl.glDrawArrays(dp.gl_type,0,dp.VA.size)
        if WIREFRAME and dp.gl_type!=gl.GL_LINES:
            LOC_wire=gl.glGetUniformLocation(GL_PROGRAM,'wireframe')
            gl.glUniform1iv(LOC_wire,1,1)
            gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
            gl.glPolygonOffset(-1.0,-1.0)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
            gl.glDrawElements(dp.gl_type,dp.EA.size,gl.GL_UNSIGNED_INT,None)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_FILL)
            gl.glUniform1iv(LOC_wire,1,0)
            gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    esui.ARO_PLC.SwapBuffers()

    # for ctrl in esui.ARO_PLC.Children:
        # if type(ctrl)==esui.TransText:ctrl.Refresh()
    return

def normPos(p):
    px=2*p[0]/esui.ARO_PLC.Size.x-1
    py=1-2*p[1]/esui.ARO_PLC.Size.y
    return (px,py)

def selectADP(x,y,w=6,h=6):
    global ARO_SELECTION
    all_adp=list()
    for adplist in ADP_DICT.values():
        all_adp+=adplist
    for dp in all_adp:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if (not dp.visible) or dp.VA.size==0:continue
        if dp.VAO==-1:
            VAO,VBO,EBO=genGLO()
            dp.VAO,dp.VBO,dp.EBO=VAO,VBO,EBO
            bindGLO(VAO,VBO,EBO)
        else:bindGLO(dp.VAO,dp.VBO,dp.EBO)
        if dp.update_data:
            bindBufferData(dp.VA,dp.EA)
            dp.update_data=False
        dp.viewDP()
        vertex_len=len(dp.VA[0])
        gl.glVertexAttribPointer(LOC_POS,3, gl.GL_FLOAT, gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(0))
        gl.glVertexAttribPointer(LOC_COLOR,4,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(12))
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        if vertex_len>7:gl.glUniform1iv(LOC_HT,1,1)
        else:gl.glUniform1iv(LOC_HT,1,0)

        gl.glUniformMatrix4fv(LOC_TRANS,1,gl.GL_FALSE,glm.value_ptr(dp.ftrans))
        gl.glUniform1iv(LOC_HL,1,1)

        if len(dp.EA)!=0:gl.glDrawElements(dp.gl_type,dp.EA.size,gl.GL_UNSIGNED_INT,None)
        elif len(dp.VA)>1:gl.glDrawArrays(dp.gl_type,0,dp.VA.size)
        res=(ctypes.c_ubyte*36)()
        gl.glReadPixels(x-w/2, PLC_H-y-h/2, w,h,gl.GL_BLUE,gl.GL_UNSIGNED_BYTE,res)

        for i in range(0,len(res)):
            if res[i]!=0:
                ARO_SELECTION.append(dp.Aro)
                break
    return ARO_SELECTION

def highlight(selection=None):
    ''' Set Aroes in selection highlighted and selected.

        Para selection: Accept Aro/es.'''
    global ARO_SELECTION
    if selection is not None:
        if isinstance(selection,list):
            ARO_SELECTION=selection
        else:
            ARO_SELECTION=[selection]

    for adplist in ADP_DICT.values():
        for adp in adplist:
            if adp.Aro in ARO_SELECTION:adp.highlight=True
            else:adp.highlight=False
    drawGL()
    return

def getAABB(adp):
    """
    docstring
    """
    # if not hasattr(aro,'position'):
        # ESC.bug('E: Aro has no position.')
    vm=[-np.inf,np.inf]*3    # [x,-x,y,-y,z,-z];
    for vtx in adp.VA:
        vtx=getTransPosition(vtx,adp.trans)
        for i in range(0,3):
            vm[2*i]=max(vtx[i],vm[2*i])
            vm[2*i+1]=min(vtx[i],vm[2*i+1])
    # aabb_8=[
    #     [vm[0],vm[2],vm[4]],[vm[0],vm[3],vm[4]],
    #     [vm[0],vm[2],vm[5]],[vm[1],vm[2],vm[4]],
    #     [vm[1],vm[3],vm[4]],[vm[1],vm[2],vm[5]],
    #     [vm[0],vm[3],vm[5]],[vm[1],vm[3],vm[5]]]
    # for i in range(0,8):
    #     t=[float(aabb_8[i][0]),float(aabb_8[i][1]),float(aabb_8[i][2]),1.0]
    #     t=adp.trans*glm.vec4(t)
    #     aabb_8[i]=list(t)[0:3]
    # vm=vm=[-np.inf,np.inf]*3    # [x,-x,y,-y,z,-z];
    # for i in range(0,8):
    #     for j in range(0,3):
    #         vm[2*j]=max(aabb_8[i][j],vm[2*j])
    #         vm[2*j+1]=min(aabb_8[i][j],vm[2*j+1])
    return vm

def rotateToCS(trans,srccs,tarcs):
    trans1=rotateToVec(srccs[0],tarcs[0])
    t=glm.vec4([float(srccs[2][0]),float(srccs[2][1]),float(srccs[2][2]),1.0])
    v_z=glm.vec3(trans1*t)
    trans2=rotateToVec(tarcs[2],v_z)
    trans=trans*trans2*trans1
    return trans

def getAllAdp():
    alladp=list()
    for adplist in ADP_DICT.values():
        alladp+=adplist
    return alladp

def getTransPosition(p,trans,out='np'):
    ''' Para out: list/np'''
    p=[float(p[0]),float(p[1]),float(p[2]),1.0]
    p=glm.vec4(p)
    p=trans*p
    p=[p[0],p[1],p[2]]  # out==list;
    if out=='np':p=np.array(p)
    return p

def getDisFormPtToPlane(pt,plane,vn=False):
    ''' Para pt: numpy point.

        Para plane: numpy point list.'''
    pA=plane[0][0:3]
    pB=plane[1][0:3]
    vAB=pB-pA
    for ip in range(2,len(plane)):
        pC=plane[ip][0:3]
        vAC=pC-pA
        vn_face=np.cross(vAC,vAB)
        if np.linalg.norm(vn_face)>EPSILON:break
    dis=abs(np.dot(vn_face,pt-pC))
    ld=np.linalg.norm(vn_face)
    dis/=ld
    if vn:return dis,vn_face/ld
    else:return dis

def getSAT(pts):
    sat=[1000,-1000]*3
    for i in range(0,3):
        for j in range(0,len(pts)):
            sat[2*i]=min(sat[2*i],pts[j][i])
            sat[2*i+1]=max(sat[2*i+1],pts[j][i])
    return sat
