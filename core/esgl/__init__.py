import sys,ctypes,math,json
import _glm as glm
import numpy as np
import OpenGL.GL as gl

from core import ESC
from .variable import *
from .quaternion import Quaternion
from .drawpart import DrawPart,AroDrawPart,ToolDrawPart,Mesh,VtxLayout
EPSILON=1e-4

class GLCore(object):
    def __init__(self) -> None:
        # Esgl global variable
        self.DICT_ADP=dict()
        self.DICT_TDP=dict()
        self.ARO_SELECTION=list()    # [ins Aro,...]
        self.EP=[5,5,5]    # Eye point
        self.AP=[0,0,0]    # Aim point
        self.UP=[0,1,0]    # Up point
        self.MAT_PROJ=glm.mat4(1.0)
        self.MAT_VIEW=glm.mat4(1.0)
        self.WHEEL_DIS=0
        self.RATIO_WH=1
        self.SPEED_ZOOM=1
        self.GLDIV:GLDiv=None
        self.GLDIV_WIDTH=0
        self.GLDIV_HEIGHT=0
        # Options;
        self.DICT_FLAG={
            'PERSPECTIVE':True,
            'WIREFRAME':False,
            'LIGHT':False}
        # Shader needed;
        self.GL_PROGRAM=0
        self.BGC=[0,0,0,0]
        self.DICT_LOC={
            'pos':0,'color':0,'trans':0,'flags':0,
            'tex':0,'proj':0,'view':0,'normal':0}
        # Cache;
        self._cch_list_light=list()
        self._cch_list_adp=list()
        self._cch_list_tdp=list()
        return

# Adp
    def initAdp(self,aro:ESC.Aro):
        import mod
        if aro.adp.find('.')!=-1:prefix=''
        else:prefix=aro.__module__[0:aro.__module__.rfind('.')]+'.'
        adp=eval(prefix+aro.adp+'('+str(aro.AroID)+')')
        self.addAdp(adp)
        return adp
    def selectAdp(self,x,y,w=6,h=6):
        for dp in self.getAllAdp():
            dp:AroDrawPart
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            if not dp.visible:continue
            dp.highlight=True
            self._drawDP(dp)
            dp.highlight=False
            res=(ctypes.c_ubyte*(w*h))()
            gl.glReadPixels(x-w/2,self.GLDIV_HEIGHT-y-h/2,w,h,
                gl.GL_BLUE,gl.GL_UNSIGNED_BYTE,res)
            if (np.array(res)!=0).any():
                self.ARO_SELECTION.append(dp.Aro)
        return self.ARO_SELECTION
    def highlightAdp(self,selection=None):
        ''' Set Aroes in selection highlighted and selected.
            Para selection: Accept Aro/es.'''
        if selection is not None:
            if isinstance(selection,list):self.ARO_SELECTION=selection
            else:self.ARO_SELECTION=[selection]

        for adp in self.getAllAdp():
            if adp.Aro in self.ARO_SELECTION:adp.highlight=True
            else:adp.highlight=False
        self.drawGL()
        return
    def rmAdp(self,aroid:int):
        self._cch_list_adp.clear()
        item:AroDrawPart=self.DICT_ADP[aroid]
        del self.DICT_ADP[aroid]
        delDP(item)
        return item
    def clearAdp(self):
        self._cch_list_adp.clear()
        self.DICT_ADP.clear()
        return
    def getAllAdp(self):
        if len(self._cch_list_adp)==0:
            self._cch_list_adp=list(self.DICT_ADP.values())
        return self._cch_list_adp
    def addAdp(self,adp:AroDrawPart):
        self.DICT_ADP[adp.Aro.AroID]=adp
        self._cch_list_adp.clear()
        return
    def getAdp(self,idx):
        out:AroDrawPart=self.DICT_ADP[idx]
        return out
    def readMap(self,clear=False):
        if clear:self.clearAdp()
        aid_remain=list(self.DICT_ADP.keys())
        for aro in ESC.getFullMap():
            if aro.AroID in self.DICT_ADP:
                aid_remain.remove(aro.AroID)
                dp=self.getAdp(aro.AroID)
                if dp.dpclass.find(aro.adp)==-1:
                    self.initAdp(aro)
                else:
                    dp.updateAdp()
            else:
                if aro.adp!='':self.initAdp(aro)
        for aid in aid_remain:self.rmAdp(aid)
        self.drawGL()
        return

# Tdp
    def addTdp(self,name:str,tdp):
        self._cch_list_tdp.clear()
        self.DICT_TDP[name]=tdp
        return
    def rmTdp(self,name:str):
        self._cch_list_tdp.clear()
        item:ToolDrawPart=self.DICT_TDP[name]
        del self.DICT_TDP[name]
        delDP(item)
        return item
    def getAllTdp(self):
        if len(self._cch_list_tdp)==0:
            self._cch_list_tdp=list(self.DICT_TDP.values())
        return self._cch_list_tdp

# GL
    def initGL(self,shader='default'):
        # shader='phong'  # for test;
        with open('core/esgl/shaders/'+shader+'/setting.json','r') as fd:
            setting=json.loads(fd.read())
        for item_ena in setting['glEnable']:
            gl.glEnable(eval('gl.'+item_ena))
        if 'GL_BLEND' in setting['glEnable']:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        for k,v in setting['global'].items():
            globals()[k]=v
        self.DICT_FLAG.update(setting['DICT_FLAG'])
        # glDepthFunc(GL_LEQUAL)      # 设置深度测试函数
        # glShadeModel(GL_SMOOTH)      # GL_SMOOTH(光滑着色)/GL_FLAT(恒定着色)
        # gl.glEnable(gl.GL_ALPHA_TEST)                   # 启用Alpha测试
        # gl.glAlphaFunc(gl.GL_GREATER, 0.1)        # 设置Alpha测试条件为大于05则通过
        # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        gl.glFrontFace(gl.GL_CW)
        gl.glShadeModel(gl.GL_FLAT)
        gl.glClearColor(self.BGC[0],self.BGC[1],self.BGC[2],self.BGC[3])
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.GL_PROGRAM=genGLProgram(shader)
        for k in self.DICT_LOC.keys():
            v=gl.glGetAttribLocation(self.GL_PROGRAM,k)
            if v==-1:v=gl.glGetUniformLocation(self.GL_PROGRAM,k)
            self.DICT_LOC[k]=v
        self.setProjMode()
        return
    def drawGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.setUniform([li.getLightPara() for li in self.getLightList()],'lights')
        self.setUniform(self.EP,'pos_eye')
        for dp in self.getAllTdp()+self.getAllAdp():
            dp:DrawPart
            if not dp.visible:continue
            self._drawDP(dp)
            dp.flag_update=False
            if self.DICT_FLAG['WIREFRAME']:
                self.setUniform({'is_frame':1},'flags')
                gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
                gl.glPolygonOffset(-1.0,-1.0)
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
                self._drawDP(dp)
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_FILL)
                gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
                self.setUniform({'is_frame':0},'flags')
        self.GLDIV.SwapBuffers()
        return
    def _drawDP(self,dp:DrawPart):
        if dp.dict_fix['fix']:
            ftrans=self._getFixTrans(dp)
        else:
            gl.glViewport(0,0,self.GLDIV_WIDTH,self.GLDIV_HEIGHT)
            ftrans=dp.trans
        for mesh in dp.list_mesh:
            if len(mesh.vertices)==0:continue
            if self.DICT_FLAG['WIREFRAME']:
                if mesh.draw_type!=DT_TRI or mesh.draw_type!=DT_QUAD:
                    continue
            if mesh.dict_glo['VAO']==-1:
                mesh.dict_glo.update(genGLO())
            bindGLO(mesh.dict_glo)
            if 'tex' in mesh.dict_layout:
                if mesh.dict_glo['TAO']==-1:
                    mesh.dict_glo['TAO']=genGLTex(mesh.texture)
                else:
                    gl.glBindTexture(gl.GL_TEXTURE_2D,mesh.dict_glo['TAO'])
            if dp.flag_update:
                bindBufferData(mesh.vertices,mesh.faces)
            self.setUniform({
                    'is_highlight':int(dp.highlight),
                    'has_tex':int('tex' in mesh.dict_layout),
                    'has_color':int('color' in mesh.dict_layout)},'flags')
            self.setUniform(ftrans*mesh.trans,'trans')
            vtx_len=len(mesh.vertices[0])*4
            for vl in mesh.dict_layout.values():
                if self.DICT_LOC[vl.label]==-1:continue
                gl.glVertexAttribPointer(self.DICT_LOC[vl.label],vl.len
                    ,gl.GL_FLOAT,gl.GL_FALSE,
                    vtx_len,ctypes.c_void_p(vl.offset))
                gl.glEnableVertexAttribArray(vl.attr)
            if len(mesh.faces)!=0:
                gl.glDrawElements(mesh.draw_type,mesh.faces.size,gl.GL_UNSIGNED_INT,None)
            elif len(mesh.vertices)!=0:
                gl.glDrawArrays(mesh.draw_type,0,len(mesh.vertices))
        return
    def _getFixTrans(self,dp:DrawPart):
        ftrans=dp.trans
        if dp.dict_fix['pos']:
            dpp=dp.dict_fix['pos']
            gl.glViewport(int(dpp[0]+20),
                int(self.GLDIV_HEIGHT-dpp[1]-dpp[3]),
                int(dpp[2]),int(dpp[3]))
            ftrans=glm.translate(ftrans,glm.vec3(self.AP))
            ftrans=glm.scale(ftrans,glm.vec3(self.GLDIV_HEIGHT/dpp[3]))
        else:
            gl.glViewport(0,0,self.GLDIV_WIDTH,self.GLDIV_HEIGHT)
            if dp.dict_fix['size']:
                ep=np.array(self.EP)
                ap=np.array(self.AP)
                v_AE=(ep-ap).tolist()
                v_OE=(ep-np.array(dp.Aro.position)).tolist()
                agl_AEO=getVecsAngle(v_AE,v_OE)
                l_ArE=glm.length(v_OE)*glm.cos(agl_AEO)
                l_AE=glm.length(v_AE)
                ftrans=glm.scale(ftrans,glm.vec3(l_ArE/l_AE))
        if dp.dict_fix['orient']:
            ftrans=self.getFixOriMat(ftrans)
        return ftrans
    def setProjMode(self,perspective=True):
        self.DICT_FLAG['PERSPECTIVE']=perspective
        if self.DICT_FLAG['PERSPECTIVE']:
            self.MAT_PROJ=glm.perspective(glm.radians(45),self.RATIO_WH,0.1,100)
        else:
            b=0.25*self.WHEEL_DIS+4
            self.MAT_PROJ=glm.ortho(-1*self.RATIO_WH*b,self.RATIO_WH*b,-1*b,b,-100,100)
        self.setUniform(self.MAT_PROJ,'proj')
        return
    def lookAt(self,ep=None,ap=None,up=None):
        if ep is not None:self.EP=ep
        if ap is not None:self.AP=ap
        if up is not None:self.UP=up
        MAT_VIEW=glm.lookAt(
            glm.vec3(self.EP),
            glm.vec3(self.AP),
            glm.vec3(self.UP))
        self.setUniform(MAT_VIEW,'view')
        self.drawGL()
        return

# Other
    def getPosFromVtx(self,dp,p):
        if dp.dict_fix['orient']:ftrans=self.getFixOriMat(dp.trans)
        else:ftrans=glm.mat4(1.0)
        glm_p=glm.vec4(float(p[0]),float(p[1]),float(p[2]),1.0)
        glm_p=self.MAT_PROJ*self.MAT_VIEW*ftrans*glm_p
        px=glm_p[0]/glm_p[3]
        py=glm_p[1]/glm_p[3]
        return (px,py)

    def getLightList(self):
        from mod.AroCore import AroLight
        for aro in ESC.getFullMap():
            if isinstance(aro,AroLight):self._cch_list_light.append(aro)
        if len(self._cch_list_light)==0:
            light_default=AroLight()
            light_default.position=[5,5,0]
            self._cch_list_light.append(light_default)
        return self._cch_list_light

    def setUniform(self,obj,tar):
        if tar not in self.DICT_LOC:
            self.DICT_LOC[tar]=gl.glGetUniformLocation(self.GL_PROGRAM,tar)
        if isinstance(obj,list):
            if len(obj)==3 and isinstance(obj[0],(int,float)):
                gl.glUniform3f(self.DICT_LOC[tar],obj[0],obj[1],obj[2])
            else:
                for i in range(len(obj)):
                    self.setUniform(obj[i],tar+'['+str(i)+']')
        elif isinstance(obj,dict):
            for k,v in obj.items():self.setUniform(v,tar+'.'+k)
        elif isinstance(obj,int):gl.glUniform1i(self.DICT_LOC[tar],obj)
        elif isinstance(obj,float):gl.glUniform1f(self.DICT_LOC[tar],obj)
        elif isinstance(obj,glm.mat4):
            gl.glUniformMatrix4fv(self.DICT_LOC[tar],1,gl.GL_FALSE,glm.value_ptr(obj))
        return

    def getFixOriMat(self,oritrans):
        ve_z=glm.vec3(0,0,1)
        ep=glm.vec3(self.EP)
        ap=glm.vec3(self.AP)
        v_AE=glm.vec3(ep-ap)
        r1=rotateToVec(ve_z,v_AE)

        ve_x=glm.vec3(1,0,0)
        ve_xr=glm.vec3(r1*glm.vec4(ve_x,0))
        v_Ax=glm.cross(v_AE,glm.vec3(self.UP))
        r2=rotateToVec(ve_xr,v_Ax)

        ftrans=oritrans*r2*r1
        return ftrans

    def cvtPosToCoord(self,p:tuple):
        ''' Convert position in AroGlc to GL coordinate.'''
        px=2*p[0]/self.GLDIV_WIDTH-1
        py=1-2*p[1]/self.GLDIV_HEIGHT
        return (px,py)

    def getSelection(self):
        ''' Return Aro selection in GL.
            Return one Aro when only, otherwise list.'''
        out=list(self.ARO_SELECTION)
        return out
    def clearSelection(self):
        self.ARO_SELECTION.clear()
        return
    pass
glc=GLCore()


# Geometry
def getVecsAngle(v1:list,v2:list):
    v1=glm.normalize(glm.vec3(v1))
    v2=glm.normalize(glm.vec3(v2))
    agl=glm.acos(glm.dot(v1,v2))
    return agl
def rotateToVec(srcvec,tarvec):
    l1=glm.l1Norm(srcvec)
    l2=glm.l1Norm(tarvec)
    is_zero=l1*l2
    if is_zero==0.0:return glm.mat4(1.0)
    agl=getVecsAngle(srcvec,tarvec)
    if glm.cos(agl)==1:return glm.mat4(1.0)
    elif glm.cos(agl)==-1:return glm.mat4(-1.0)
    v_axis=glm.cross(srcvec,tarvec)
    ftrans=glm.rotate(glm.mat4(1.0),agl,v_axis)
    return ftrans
def rotateToCS(trans,srccs,tarcs):
    'todo: srccs'
    qua=getQuatFormCS(tarcs)
    trans=trans*glm.mat4_cast(glm.fquat(qua))
    return trans
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
def getQuatFormCS(cs):
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

# GLO
def genGLO():
    ''' Generate VAO/VBO/EBO and bind them to GL.'''
    VAO=gl.glGenVertexArrays(1)
    VBO,EBO=gl.glGenBuffers(2)
    out={'VAO':VAO,'VBO':VBO,'EBO':EBO}
    return out
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
    import PIL.Image as pili
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
        ESC.err(infolog.decode())

    frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(frag_shader,com_src+fragmentShaderSource)
    gl.glCompileShader(frag_shader)
    success=gl.glGetShaderiv(frag_shader,gl.GL_COMPILE_STATUS)
    if not success:
        infolog=gl.glGetShaderInfoLog(frag_shader)
        print(infolog.decode())
        ESC.err(infolog.decode())

    id_glprogram = gl.glCreateProgram()
    gl.glAttachShader(id_glprogram, vtx_shader)
    gl.glAttachShader(id_glprogram, frag_shader)
    gl.glLinkProgram(id_glprogram)
    success=gl.glGetProgramiv(id_glprogram,gl.GL_LINK_STATUS)
    if not success:
        infolog=gl.glGetProgramInfoLog(id_glprogram)
        ESC.err(infolog.decode())

    gl.glDeleteShader(vtx_shader)
    gl.glDeleteShader(frag_shader)
    gl.glUseProgram(id_glprogram)
    return id_glprogram

# Other
def import3DFile(path):
    import _pyassimp as ai
    list_mesh=list()
    trans=np.identity(4,dtype=np.float32)

    flag_ai=ai.postprocess.aiProcess_MakeLeftHanded \
        | ai.postprocess.aiProcess_Triangulate
    scene=ai.load(path,processing=flag_ai)
    layoutlist=[VtxLayout(),
        VtxLayout(label='color'),VtxLayout(label='normal')]

    for child in scene.rootnode.children:
        # i=child.transformation
        # mat=ai.structs.Matrix4x4(
        #     i[0][3],i[0][0],i[0][1],i[0][2],
        #     i[1][3],i[1][0],i[1][1],i[1][2],
        #     i[2][3],i[2][0],i[2][1],i[2][2],
        #     i[3][3],i[3][0],i[3][1],i[3][2])
        # s,r,t=ai.decompose_matrix(mat)
        # trans=glm.translate(glm.mat4(1.0),[t.x,t.y,t.z])
        for mesh in child.meshes:
            ca=np.tile([0.5,0.5,0.5,1],(len(mesh.vertices),1)).astype(np.float32)
            va=np.hstack((mesh.vertices,ca,mesh.normals))
            fa=np.array(mesh.faces,dtype=np.uint32)

            m=Mesh(vertices=va,faces=fa,trans=trans,layout=layoutlist)
            list_mesh.append(m)
    return list_mesh

def getAABB(dp:DrawPart,trans=True):
    """ docstring"""
    vm=[0]*6    # [x,-x,y,-y,z,-z];
    vtx=dp.getAllVtx()
    vtx=np.transpose(vtx)
    if trans:
        row1=np.tile(np.array([1]),(1,vtx.shape[0]))
        vtx=np.row_stack((vtx,row1))
        transmat=np.array(dp.trans)
        vtx=np.dot(transmat,vtx)
    for i in range(0,3):
        vm[2*i]=max(vtx[i])
        vm[2*i+1]=min(vtx[i])

    return vm

def getSAT(pts):
    sat=[1000,-1000]*3
    for i in range(0,3):
        for j in range(0,len(pts)):
            sat[2*i]=min(sat[2*i],pts[j][i])
            sat[2*i+1]=max(sat[2*i+1],pts[j][i])
    return sat

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

def delDP(dp:DrawPart):
    for mesh in dp.list_mesh:
        mesh:Mesh
        'todo: bug'
        # gl.glDeleteVertexArrays(1,mesh.dict_glo['VAO'])
        # gl.glDeleteBuffers(1,mesh.dict_glo['EBO'])
        # gl.glDeleteBuffers(1,mesh.dict_glo['VBO'])
        # gl.glDeleteTextures(1,)
    return

from .gl_div import GLDiv
