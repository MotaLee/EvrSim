import ctypes,json
from ._pyglm import glm
import numpy as np
import OpenGL.GL as gl
from core import esc,ESC
from .method import *
from .variable import *
from .cls import Quaternion
from .drawpart import DrawPart,AroDrawPart,ToolDrawPart,Mesh,VtxLayout
from .subthread import GLThreadRender

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
        self.GLDIV=None
        self.GLDIV_WIDTH=0
        self.GLDIV_HEIGHT=0
        # Options;
        self.DICT_FLAG={
            'PERSPECTIVE':True,
            'WIREFRAME':False,
            'LIGHT':False}
        # Shader needed;
        self.GL_CONTEXT=None
        self.GL_PROGRAM=0
        self.BGC=[0,0,0,1]
        self.DICT_LOC={
            'pos':0,'color':0,'trans':0,'flags':0,
            'tex':0,'proj':0,'view':0,'normal':0}
        # Cache;
        self._cch_list_light=list()
        self._cch_list_adp=list()
        self._cch_list_tdp=list()
        return

    # Adp
    def initAdp(self,aro:esc.Aro):
        import mod,app
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
        # self.drawGL()
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
        if hasattr(self.GLDIV,'SwapBuffers'):
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
                bindBufferData(mesh)
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
            elif len(mesh.edges)!=0:
                gl.glDrawElements(mesh.draw_type,mesh.edges.size,gl.GL_UNSIGNED_INT,None)
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
                agl_AEO=getVectorAngle(v_AE,v_OE)
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
        self.MAT_VIEW=glm.lookAt(
            glm.vec3(self.EP),
            glm.vec3(self.AP),
            glm.vec3(self.UP))
        self.setUniform(self.MAT_VIEW,'view')
        self.drawGL()
        return

    # Other
    def setShell(self,w,h,div=None):
        self.GLDIV_WIDTH=w
        self.GLDIV_HEIGHT=h
        self.RATIO_WH=w/h
        self.GLDIV=div
        return
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
        ''' Return Aro selection in GL.'''
        out=list(self.ARO_SELECTION)
        return out
    def clearSelection(self):
        self.ARO_SELECTION.clear()
        return
    pass

GLC=GLCore()
