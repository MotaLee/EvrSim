# GLO
import sys,math
from . import glm
import numpy as np
import OpenGL.GL as gl

from core import ESC
from .variable import *
from .drawpart import DrawPart,Mesh,VtxLayout
EPSILON=1e-4
LCS_DFT=[[1,0,0],[0,1,0],[0,0,1]]
# Geometry
def getVectorAngle(v1:list,v2:list):
    v1=glm.normalize(glm.vec3(v1))
    v2=glm.normalize(glm.vec3(v2))
    agl=glm.acos(glm.dot(v1,v2))
    return agl
def rotateToVec(srcvec,tarvec):
    l1=glm.l1Norm(srcvec)
    l2=glm.l1Norm(tarvec)
    is_zero=l1*l2
    if is_zero==0.0:return glm.mat4(1.0)
    agl=getVectorAngle(srcvec,tarvec)
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
    [m11,m21,m31]=list(vx)
    [m12,m22,m32]=list(vy)
    [m13,m23,m33]=list(vz)

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
def cvtRGB(color):
    ''' Convert color string to RGB or backwise.
        * Para color: Accept str like '#ffffff', or list like [1,1,1];'''
    if isinstance(color,(tuple,list)):
        output="#"
        for v in color:
            hexv=hex(int(v*255))
            hexv = hexv.rjust(2, '0')
            output+=hexv
    else:
        str1=color[1:3]
        str2=color[3:5]
        str3=color[5:7]
        num1=int('0x'+str1,16)
        num2=int('0x'+str2,16)
        num3=int('0x'+str3,16)
        output=(num1,num2,num3)
    return output
def genCircleArr(r=1,inum=2,center=False):
    ''' Generate vertices, edges and faces of a circle.
        Return va, ea, fa.
        * Para p: position of circle center;
        '''
    VA=np.array([[0,0,0]],dtype=np.float32)
    EA=np.array([],dtype=np.uint32)
    FA=np.array([],dtype=np.uint32)
    pt_c=VA[0]
    ax=np.array([1,0,0],dtype=np.float32)
    ay=np.array([0,1,0],dtype=np.float32)
    n_pt=int(4*2**inum)
    d_agl=2*math.pi/n_pt
    for i in range(n_pt):
        agl=i*d_agl
        dx=r*math.sin(agl)
        dy=r*math.cos(agl)
        dv=dx*ax+dy*ay
        VA=np.row_stack((VA,pt_c+dv))
    VA.astype(np.float32)

    r1=np.zeros((n_pt,1))
    r2=np.reshape(np.arange(1,n_pt+1),(n_pt,1))
    r3=np.reshape(np.arange(2,n_pt+2),(n_pt,1))

    EA=np.hstack((r2,r3)).astype(np.uint32)
    EA[n_pt-1,1]=1
    if center:EA=np.vstask((EA,np.hstack((r1,r2))))

    FA=np.hstack((r1,r2,r3))
    FA[n_pt-1,2]=1
    return VA,EA,FA
def genRectArr(size=(2,2),shape=4,inline=True):
    rx=np.linspace(-0.5,0.5,size[0])
    rx=rx.reshape((rx.size,1))
    rx=np.tile(rx,(size[0],1))

    ry=np.linspace(-0.5,0.5,size[1])
    ry=ry.reshape((ry.size,1))
    ry=np.tile(ry,(1,size[1]))
    ry=ry.reshape((ry.size,1))

    rz=np.zeros((size[0]*size[1],1))
    VA=np.hstack((rx,ry,rz)).astype(np.float32)
    'todo: ea fa'
    EA=np.array([],dtype=np.uint32)
    FA=np.array([],dtype=np.uint32)
    return VA,EA,FA
def stackColorArr(va,color,alpha=1):
    if isinstance(color,str):color=cvtRGB(color)
    CA=np.array([color],dtype=np.float32)
    CA=np.tile(CA,(va.shape[0],1))
    AA=np.array([alpha],dtype=np.float32)
    AA=np.tile(AA,(va.shape[0],1))
    VA=np.hstack((va,CA,AA))
    return VA


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
def bindBufferData(mesh,array=''):
    VA=mesh.vertices
    if (array=='' and len(mesh.faces)!=0) or array=='faces':
        EA=mesh.faces
    elif (array=='' and len(mesh.edges)!=0) or array=='edges':
        EA=mesh.edges
    else:
        EA=mesh.faces
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

def transMat(option='translate',mat=None,vec=None,agl=0):
    if mat is None:mat=glm.mat4(1.0)
    if option=='translate':
        mat=glm.translate(mat,glm.vec3(vec))
    elif option=='scale':
        mat=glm.scale(mat,glm.vec3(vec))
    elif option=='rotate':pass
    return mat
