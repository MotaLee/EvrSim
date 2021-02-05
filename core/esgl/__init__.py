import os,sys,ctypes,math,json
sys.path.append(os.getcwd()+'\\res\\lib')
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
os.add_dll_directory(os.getcwd()+'\\res\\lib')
import _glm as glm
import numpy as np
import OpenGL.GL as gl
# import assimp as ai
import _pyassimp as ai
import PIL.Image as pili
import mod
from core import ESC,esui
from .quaternion import Quaternion
from .aroglc import AroGlc
from .drawpart import DrawPart,AroDrawPart,ToolDrawPart,Mesh,VertexLayout

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

# Options;
DICT_FLAG={'PERSPECTIVE':True,
    'WIREFRAME':False,
    'LIGHT':False}
# Shader needed;
GL_PROGRAM=0
BGC=[0,0,0,0]
DICT_LOC={'pos':0,'color':0,'trans':0,'flags':0,'tex':0,'proj':0,'view':0,'normal':0}
# Module-in variables;
_list_all_adp=list()
_list_light=list()

def initADP(aro):
    global _list_all_adp
    _list_all_adp.clear()
    if isinstance(aro.adp,list):adplist=aro.adp
    else:adplist=[aro.adp]
    outlist=list()
    for adp in adplist:
        if adp.find('.')!=-1: prefix=''
        else:
            prefix=aro.__module__[0:aro.__module__.rfind('.')]+'.'
        adp=eval(prefix+adp+'('+str(aro.AroID)+')')
        outlist.append(adp)
    return outlist

def import3DFile(path):
    'todo'
    list_mesh=list()
    trans=np.identity(4,dtype=np.float32)

    flag_ai=ai.postprocess.aiProcess_MakeLeftHanded \
        | ai.postprocess.aiProcess_Triangulate
    scene=ai.load(path,processing=flag_ai)
    layoutlist=[VertexLayout(),
        VertexLayout(label='color'),VertexLayout(label='normal')]

    for child in scene.rootnode.children:
        i=child.transformation
        mat=ai.structs.Matrix4x4(
            i[0][3],i[0][0],i[0][1],i[0][2],
            i[1][3],i[1][0],i[1][1],i[1][2],
            i[2][3],i[2][0],i[2][1],i[2][2],
            i[3][3],i[3][0],i[3][1],i[3][2])
        s,r,t=ai.decompose_matrix(mat)
        trans=glm.translate(glm.mat4(1.0),[t.x,t.y,t.z])
        # rt=glm.mat4_cast(glm.fquat(r.w,r.x,r.y,r.z))
        # trans=trans*rt
        # trans=trans*glm.scale(glm.mat4(1.0),[s.x/100,s.y/100,s.z/100])
        for mesh in child.meshes:
            # if mesh.normals.size==0:continue
            ca=np.tile([0.5,0.5,0.5,1],(len(mesh.vertices),1)).astype(np.float32)
            va=np.hstack((mesh.vertices,ca,mesh.normals))
            fa=np.array(mesh.faces,dtype=np.uint32)

            m=Mesh(vertices=va,faces=fa,trans=trans,layout=layoutlist)
            list_mesh.append(m)
    return list_mesh

def importDPM(path):
    va=None
    ea=None
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

def bindGLO(dict_glo):
    gl.glBindVertexArray(dict_glo['VAO'])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER,dict_glo['VBO'])
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER,dict_glo['EBO'])
    return

def bindBufferData(VA,EA):
    gl.glBufferData(gl.GL_ARRAY_BUFFER,sys.getsizeof(VA),VA,gl.GL_STREAM_DRAW)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(EA),EA, gl.GL_STREAM_DRAW)
    return

def genGLTex(imgpath,width=None,height=None):
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

def genGLProgram(shader):
    ''' Para shader: Empty for 'default'.'''
    vs='core/esgl/shaders/'+shader+'/vs.glsl'
    fs='core/esgl/shaders/'+shader+'/fs.glsl'
    com='core/esgl/shaders/'+shader+'/com.glsl'
    with open(vs,'r') as fd:
        vertexShaderSource=fd.read()
    with open(fs,'r') as fd:
        fragmentShaderSource=fd.read()
    with open(com,'r') as fd:
        com_src=fd.read()

    success=0
    vtx_shader=gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vtx_shader,com_src+vertexShaderSource)
    gl.glCompileShader(vtx_shader)
    success=gl.glGetShaderiv(vtx_shader,gl.GL_COMPILE_STATUS)
    if not success:
        infolog=gl.glGetShaderInfoLog(vtx_shader)
        ESC.bug(infolog.decode())

    frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(frag_shader,com_src+fragmentShaderSource)
    gl.glCompileShader(frag_shader)
    success=gl.glGetShaderiv(frag_shader,gl.GL_COMPILE_STATUS)
    if not success:
        infolog=gl.glGetShaderInfoLog(frag_shader)
        print(infolog.decode())
        ESC.bug(infolog.decode())

    id_glprogram = gl.glCreateProgram()
    gl.glAttachShader(id_glprogram, vtx_shader)
    gl.glAttachShader(id_glprogram, frag_shader)
    gl.glLinkProgram(id_glprogram)
    success=gl.glGetProgramiv(id_glprogram,gl.GL_LINK_STATUS)
    if not success:
        infolog=gl.glGetProgramInfoLog(id_glprogram)
        ESC.bug(infolog.decode())

    gl.glDeleteShader(vtx_shader)
    gl.glDeleteShader(frag_shader)
    gl.glUseProgram(id_glprogram)
    return id_glprogram

def projMode(perspective=True):
    global DICT_FLAG,MAT_PROJ,GL_PROGRAM,DICT_LOC
    DICT_FLAG['PERSPECTIVE']=perspective
    if DICT_FLAG['PERSPECTIVE']:
        MAT_PROJ=glm.perspective(glm.radians(45),ASPECT_RATIO,0.1,100)
    else:
        b=0.25*WHEEL_DIS+4
        MAT_PROJ=glm.ortho(-1*ASPECT_RATIO*b,ASPECT_RATIO*b,-1*b,b,-100,100)
    setUniform(MAT_PROJ,'proj')
    return

def lookAt(ep=None,ap=None,up=None):
    global EP,AP,UP,MAT_VIEW
    if ep is not None:EP=np.array(ep)
    if ap is not None:AP=np.array(ap)
    if up is not None:UP=np.array(up)
    MAT_VIEW=glm.lookAt(glm.vec3(EP.tolist()),
        glm.vec3(AP.tolist()),glm.vec3(UP.tolist()))
    setUniform(MAT_VIEW,'view')
    drawGL()
    return

def normPos(p):
    px=2*p[0]/esui.ARO_PLC.Size.x-1
    py=1-2*p[1]/esui.ARO_PLC.Size.y
    return (px,py)

def selectADP(x,y,w=6,h=6):
    global ARO_SELECTION
    all_adp=getAllAdp()
    for dp in all_adp:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if (not dp.visible) or dp.VA.size==0:continue
        if dp.dict_glo['VAO']==-1:
            dp.dict_glo['VAO'],dp.dict_glo['VBO'],dp.dict_glo['EBO']=genGLO()
        bindGLO(dp.dict_glo)
        vertex_len=len(dp.VA[0])
        gl.glVertexAttribPointer(DICT_LOC['pos'],3,
            gl.GL_FLOAT, gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        if dp.dict_fix['fix']:ftrans=_fixViewDP(dp)
        else:ftrans=dp.trans
        setUniform(ftrans,'trans')
        setUniform({'is_highlight':1},'flags')

        _drawDP(dp)
        res=(ctypes.c_ubyte*(w*h))()
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
        if isinstance(selection,list):ARO_SELECTION=selection
        else:ARO_SELECTION=[selection]

    for adp in getAllAdp():
        if adp.Aro in ARO_SELECTION:adp.highlight=True
        else:adp.highlight=False
    drawGL()
    return

def getAABB(adp,trans=True):
    """
    docstring
    """
    # if not hasattr(aro,'position'):
        # ESC.bug('Aro has no position.')
    vm=[-np.inf,np.inf]*3    # [x,-x,y,-y,z,-z];
    for vtx in adp.VA:
        if trans:
            vtx=getTransPosition(vtx,adp.trans)
        for i in range(0,3):
            vm[2*i]=max(vtx[i],vm[2*i])
            vm[2*i+1]=min(vtx[i],vm[2*i+1])

    return vm

def rotateToCS(trans,srccs,tarcs):
    'todo: srccs'
    qua=getQuaternionFormCS(tarcs)
    trans=trans*glm.mat4_cast(glm.fquat(qua))
    return trans

def getAllAdp():
    global _list_all_adp
    if len(_list_all_adp)==0:
        for adplist in ADP_DICT.values():
            _list_all_adp+=adplist
    return _list_all_adp

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
    pC=np.zreos(3)
    vAB=pB-pA
    vn_face=np.zreos(3)
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

def getQuaternionFormCS(cs):
    vx=np.array(cs[0])
    vx=vx/np.linalg.norm(vx)
    vy=np.array(cs[1])
    vy=vy/np.linalg.norm(vy)
    vz=np.array(cs[2])
    vz=vz/np.linalg.norm(vz)
    [m11,m21,m31]=vx.tolist()
    [m12,m22,m32]=vy.tolist()
    [m13,m23,m33]=vz.tolist()

    # //探测四元数中最大的项, test_t=4*t**2-1
    test_w = m11+m22+m33
    test_x = m11-m22-m33
    test_y = m22-m11-m33
    test_z = m33-m11-m22
    # //计算四元数的值
    if test_w>EPSILON:
        biggestVal=math.sqrt(test_w+1.0)*0.5
        mult = 0.25/biggestVal
        w=biggestVal
        x=(m32-m23)*mult
        y=(m13-m31)*mult
        z=(m21-m12)*mult
    elif test_x>EPSILON:
        biggestVal=math.sqrt(test_x+1.0)*0.5
        mult = 0.25/biggestVal
        x = biggestVal
        w =(m32-m23)*mult
        y =(m12+m21)*mult
        z =(m31+m13)*mult
    elif test_y>EPSILON:
        biggestVal=math.sqrt(test_y+1.0)*0.5
        mult = 0.25/biggestVal
        y =biggestVal
        w =(m13-m31)*mult
        x =(m12+m21)*mult
        z =(m23+m32)*mult
    else:
        biggestVal=math.sqrt(test_z+1.0)*0.5
        mult = 0.25/biggestVal
        z =biggestVal
        w =(m21-m12)*mult
        x =(m31+m13)*mult
        y =(m23+m32)*mult
    return [w,x,y,z]

def getLightList():
    from mod.AroCore import AroLight
    global _list_light
    for aro in ESC.ARO_MAP.values():
        if isinstance(aro,AroLight):_list_light.append(aro)
    if len(_list_light)==0:
        light_default=AroLight()
        light_default.position=[5,5,0]
        _list_light.append(light_default)
    return _list_light

def setUniform(obj,tar):
    global DICT_LOC
    if tar not in DICT_LOC:
        DICT_LOC[tar]=gl.glGetUniformLocation(GL_PROGRAM,tar)
    if isinstance(obj,list):
        if len(obj)==3 and isinstance(obj[0],(int,float)):
            gl.glUniform3f(DICT_LOC[tar],obj[0],obj[1],obj[2])
        else:
            for i in range(len(obj)):
                setUniform(obj[i],tar+'['+str(i)+']')
    elif isinstance(obj,dict):
        for k,v in obj.items():setUniform(v,tar+'.'+k)
    elif isinstance(obj,int):gl.glUniform1i(DICT_LOC[tar],obj)
    elif isinstance(obj,float):gl.glUniform1f(DICT_LOC[tar],obj)
    elif isinstance(obj,glm.mat4):
        gl.glUniformMatrix4fv(DICT_LOC[tar],1,gl.GL_FALSE,glm.value_ptr(obj))

    return

def initGL(shader='default'):
    shader='phong'  # for test;
    global DICT_LOC,GL_PROGRAM,DICT_FLAG
    with open('core/esgl/shaders/'+shader+'/setting.json','r') as fd:
        setting=json.loads(fd.read())
    for item_ena in setting['glEnable']:
        gl.glEnable(eval('gl.'+item_ena))
    if 'GL_BLEND' in setting['glEnable']:
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    for k,v in setting['global'].items():
        globals()[k]=v
    DICT_FLAG.update(setting['DICT_FLAG'])
    # glDepthFunc(GL_LEQUAL)      # 设置深度测试函数
    # glShadeModel(GL_SMOOTH)      # GL_SMOOTH(光滑着色)/GL_FLAT(恒定着色)
    # gl.glEnable(gl.GL_ALPHA_TEST)                   # 启用Alpha测试
    # gl.glAlphaFunc(gl.GL_GREATER, 0.1)        # 设置Alpha测试条件为大于05则通过
    # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    gl.glFrontFace(gl.GL_CW)
    gl.glShadeModel(gl.GL_FLAT)
    gl.glClearColor(BGC[0],BGC[1],BGC[2],BGC[3])
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    GL_PROGRAM=genGLProgram(shader)
    for k in DICT_LOC.keys():
        v=gl.glGetAttribLocation(GL_PROGRAM,k)
        if v==-1:v=gl.glGetUniformLocation(GL_PROGRAM,k)
        DICT_LOC[k]=v
    projMode()
    return

def drawGL():
    global GL_PROGRAM
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    setUniform([li.getLightPara() for li in getLightList()],'lights')
    setUniform(EP.tolist(),'pos_eye')
    for dp in TDP_LIST+getAllAdp():
        if (not dp.visible):continue
        if dp.dict_glo['VAO']==-1:
            dp.dict_glo['VAO'],dp.dict_glo['VBO'],dp.dict_glo['EBO']=genGLO()
        bindGLO(dp.dict_glo)
        if dp._is_modified:
            bindBufferData(dp.VA,dp.EA)
            dp._is_modified=False

        setUniform({
            'is_highlight':int(dp.highlight),
            'has_tex':int('tex' in dp.dict_layout),
            'has_color':int('color' in dp.dict_layout)},'flags')
        if dp.VA.size!=0:
            vtx_len=len(dp.VA[0])*4
            if 'pos' in dp.dict_layout:
                gl.glVertexAttribPointer(DICT_LOC['pos'],dp.dict_layout['pos'],
                    gl.GL_FLOAT,gl.GL_FALSE,vtx_len,ctypes.c_void_p(0))
                gl.glEnableVertexAttribArray(0)
            if 'color' in dp.dict_layout:
                gl.glVertexAttribPointer(DICT_LOC['color'],dp.dict_layout['color'],
                    gl.GL_FLOAT,gl.GL_FALSE,vtx_len,ctypes.c_void_p(12))
                gl.glEnableVertexAttribArray(1)
            if 'tex' in dp.dict_layout:
                gl.glVertexAttribPointer(DICT_LOC['tex'],dp.dict_layout['tex'],
                    gl.GL_FLOAT,gl.GL_FALSE,vtx_len,ctypes.c_void_p(12))
                gl.glEnableVertexAttribArray(2)
                if dp.dict_glo['TAO']==-1:dp.dp.dict_glo['TAO']=genGLTex(dp.texture)
                else:gl.glBindTexture(gl.GL_TEXTURE_2D,dp.dp.dict_glo['TAO'])
            if 'normal' in dp.dict_layout and DICT_LOC['normal']!=-1:
                gl.glVertexAttribPointer(DICT_LOC['normal'],dp.dict_layout['normal'],
                    gl.GL_FLOAT,gl.GL_FALSE,vtx_len,ctypes.c_void_p(28))
                gl.glEnableVertexAttribArray(3)

            if dp.dict_fix['fix']:ftrans=_fixViewDP(dp)
            else:ftrans=dp.trans
            setUniform(ftrans,'trans')

        _drawDP(dp)
        if DICT_FLAG['WIREFRAME'] and dp.gl_type!=gl.GL_LINES:
            setUniform({'is_frame':1},'flags')
            gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
            gl.glPolygonOffset(-1.0,-1.0)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
            _drawDP(dp)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_FILL)
            gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
            setUniform({'is_frame':0},'flags')
    esui.ARO_PLC.SwapBuffers()
    # for ctrl in esui.ARO_PLC.Children:
        # if type(ctrl)==esui.TransText:ctrl.Refresh()
    return

def _drawDP(dp:DrawPart):
    if len(dp.EA)!=0:gl.glDrawElements(dp.gl_type,dp.EA.size,gl.GL_UNSIGNED_INT,None)
    if len(dp.list_mesh)!=0:
        for mesh in dp.list_mesh:
            if mesh.dict_glo['VAO']==-1:
                mesh.dict_glo['VAO'],mesh.dict_glo['VBO'],mesh.dict_glo['EBO']=genGLO()
            bindGLO(mesh.dict_glo)
            bindBufferData(mesh.vertices,mesh.faces)
            setUniform(dp.trans*mesh.trans,'trans')
            vtx_len=len(mesh.vertices[0])*4
            for vl in mesh.dict_layout:
                if DICT_LOC[vl.label]==-1:continue
                gl.glVertexAttribPointer(DICT_LOC[vl.label],vl.len,gl.GL_FLOAT,gl.GL_FALSE,
                    vtx_len,ctypes.c_void_p(vl.offset))
                gl.glEnableVertexAttribArray(vl.attr)
            gl.glDrawElements(mesh.gl_type,mesh.faces.size,gl.GL_UNSIGNED_INT,None)

    return

def getPtNormal(va,ea):
    norm_list=list()
    vtx_dict=dict()
    for ei in range(len(ea)):
        for e in ea[ei]:
            if e in vtx_dict:vtx_dict[e].append(ei)
            else:vtx_dict[e]=[ei]
        pA=va[ea[ei][0]][0:3]
        pB=va[ea[ei][1]][0:3]
        pC=va[ea[ei][2]][0:3]
        vBC=pC-pB
        vAB=pB-pA
        vn=np.cross(vBC,vAB)
        vn/=np.linalg.norm(vn)
        norm_list.append(vn)
    out_norm_mat=np.array([0,0,0],dtype=np.float32)
    for vi in range(len(va)):
        vsum=np.array([0,0,0],dtype=np.float32)
        for fi in vtx_dict[vi]:
            vsum+=norm_list[fi]
        vsum/=np.linalg.norm(vsum)
        out_norm_mat=np.row_stack((out_norm_mat,vsum))
    return out_norm_mat[1:]

def _fixViewDP(dp:DrawPart):
        ftrans=dp.trans
        if dp.dict_fix['pos']:
            dpp=dp.dict_fix['pos']
            gl.glViewport(int(dpp[0]+4*esui.YU),int(PLC_H-dpp[1]-dpp[3]),int(dpp[2]),int(dpp[3]))
            ftrans=glm.translate(ftrans,glm.vec3(AP.tolist()))
            ftrans=glm.scale(ftrans,glm.vec3(PLC_H/dpp[3]))
        else:
            gl.glViewport(0,0,PLC_W,PLC_H)
            if dp.dict_fix['size']:
                v_AE=(EP-AP).tolist()
                v_OE=(EP-dp.Aro.position).tolist()
                agl_AEO=getAngleFrom2Vec3(v_AE,v_OE)
                l_ArE=glm.length(v_OE)*glm.cos(agl_AEO)
                l_AE=glm.length(v_AE)
                ftrans=glm.scale(ftrans,glm.vec3(l_ArE/l_AE))
        if dp.dict_fix['orient']:
            ftrans=getFixOriMat(ftrans)
        dp.ftrans=ftrans
        return ftrans
