# System libs;
import sys
import math
from ctypes import c_void_p
# Builtin libs;
from core import ESC
from core import esui
# Outer libs;
import wx
import glm
import wx.glcanvas as wg
import OpenGL.GL as gl
import numpy as np
# GL libs;
from .draw import GLDrawPart
xyz_axis=GLDrawPart('CS','xyzAxis')
xz_grid=GLDrawPart('GRID','xzGrid')
xy_grid=GLDrawPart('GRID','xyGrid')
yz_grid=GLDrawPart('GRID','yzGrid')
emp_grid=GLDrawPart('GRID','emp')

# OpenGL container wx sub class;
class Glc(wg.GLCanvas):

    def __init__(self,parent,p,s):
        wg.GLCanvas.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            name='aropl',
            style=wx.NO_BORDER | wg.WX_GL_RGBA | wg.WX_GL_DOUBLEBUFFER | wg.WX_GL_DEPTH_SIZE)
        # Var;
        self.drawlist=[xyz_axis,xz_grid]
        self.k=self.MinWidth/self.MinHeight
        self.whl_d=0    # Wheel distance;
        self.spos=(0,0)     #
        self.ep=np.array([5,5,5])    # Eye point;
        self.ap=np.array([0,0,0])    # Aim point;
        self.up=np.array([0,1,0])    # Up point;
        # self.gridable=True
        self.viewPrep=True   # View perspective mode;
        self.time_step=0

        xu=s[0]/75
        yu=s[1]/75
        self.prpbtn=esui.btn(self,(37.5*xu-15.5*yu,0.5*yu),(4*yu,4*yu),'Pp')
        self.oribtn=esui.btn(self,(37.5*xu-11*yu,0.5*yu),(4*yu,4*yu),'Oi')
        self.xybtn=esui.btn(self,(37.5*xu-6.5*yu,0.5*yu),(4*yu,4*yu),'Xy')
        self.xzbtn=esui.btn(self,(37.5*xu-2*yu,0.5*yu),(4*yu,4*yu),'Xz')
        self.yzbtn=esui.btn(self,(37.5*xu+2.5*yu,0.5*yu),(4*yu,4*yu),'Yz')
        self.fitbtn=esui.btn(self,(37.5*xu+7*yu,0.5*yu),(4*yu,4*yu),'Ft')
        self.grdbtn=esui.btn(self,(37.5*xu+11.5*yu,0.5*yu),(4*yu,4*yu),'Gd')

        for ctrl in (self.xybtn,self.xzbtn,self.yzbtn):
            ctrl.Bind(wx.EVT_LEFT_DCLICK,self.onDClkViewBtn)
        for ctrl in (self.prpbtn,self.oribtn,self.xybtn,self.xzbtn,self.yzbtn,self.fitbtn,self.grdbtn):
            ctrl.Bind(wx.EVT_LEFT_DOWN,self.onClkViewBtn)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onClk)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onRoWhl)
        self.Bind(wx.EVT_MIDDLE_DOWN,self.onClkWhl)
        self.Bind(wx.EVT_MOTION,self.onMove)

        # Initilize opengl;
        self.initGL()
        self.Hide()
        return

    def initGL(self):
        self.context = wg.GLContext(self)
        self.SetCurrent(self.context)

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
        gl.glClearColor(0,0,0,1)    # 设置画布背景色
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

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
        self.shade_program = gl.glCreateProgram()
        gl.glAttachShader(self.shade_program, vertexShader)
        gl.glAttachShader(self.shade_program, fragmentShader)
        gl.glLinkProgram(self.shade_program)
        gl.glDeleteShader(vertexShader)
        gl.glDeleteShader(fragmentShader)
        gl.glUseProgram(self.shade_program)

        self.projMode()
        self.lookAt()
        return

    def drawGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Draw libs;
        for dp in self.drawlist:
            VAO=gl.glGenVertexArrays(1)
            VBO,EBO=gl.glGenBuffers(2)
            VA=dp.VA
            EA=dp.EA
            gl.glBindVertexArray(VAO)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER,VBO)
            gl.glBufferData(gl.GL_ARRAY_BUFFER,sys.getsizeof(VA),VA,gl.GL_STATIC_DRAW)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(EA), EA, gl.GL_STATIC_DRAW)

            pos_loc=gl.glGetAttribLocation(self.shade_program,'in_pos')
            gl.glVertexAttribPointer(pos_loc,3, gl.GL_FLOAT, gl.GL_FALSE,28,c_void_p(0))
            color_loc=gl.glGetAttribLocation(self.shade_program,'in_color')
            gl.glVertexAttribPointer(color_loc,4,gl.GL_FLOAT,gl.GL_FALSE,28,c_void_p(12))
            if dp.dim==2: ftrans=self.trans2D(dp.trans)
            else: ftrans=glm.mat4(1.0)
            trans_loc=gl.glGetUniformLocation(self.shade_program,'trans')
            gl.glUniformMatrix4fv(trans_loc,1,gl.GL_FALSE,glm.value_ptr(ftrans))
            if dp.highlight:hl=1
            else: hl=0
            hl_loc=gl.glGetUniformLocation(self.shade_program,'highlight')
            gl.glUniform1iv(hl_loc,1,hl)

            gl.glEnableVertexAttribArray(0)
            gl.glEnableVertexAttribArray(1)

            if len(EA)!=0:
                gl.glDrawElements(dp.gl_type,len(EA),gl.GL_UNSIGNED_INT,None)
            else:
                gl.glDrawArrays(dp.gl_type,0,len(VA))
        self.SwapBuffers()

        for ctrl in self.Children:
            if type(ctrl) is esui.Ttc:
                ctrl.Refresh()
        return

    def readMap(self):
        for aro in ESC.ARO_MAP:
            in_list=False
            for dp in self.drawlist:
                if dp.name==aro.AroID:
                    dp.updateAro(aro)
                    in_list=True
                    break
            if not in_list and 'position' in aro.__dict__:
                pnt=GLDrawPart(aro.AroID,'point',aro)
                self.drawlist.append(pnt)
        self.drawGL()
        return

    def highlightAroes(self,aroidlist):
        for dp in self.drawlist:
            if dp.Aro is None:
                continue
            elif dp.Aro.AroID in aroidlist:
                dp.highlight=True
            else:
                dp.highlight=False
        self.drawGL()
        return

    def projMode(self):
        if self.viewPrep:
            self.projection=glm.perspective(glm.radians(45),self.k,0.1,100)
        else:
            b=0.25*self.whl_d+4
            self.projection=glm.ortho(-1*self.k*b,self.k*b,-1*b,b,-100,100)

        proj_loc=gl.glGetUniformLocation(self.shade_program,'projection')
        gl.glUniformMatrix4fv(proj_loc,1,gl.GL_FALSE,glm.value_ptr(self.projection))
        return

    def lookAt(self):
        self.view=glm.lookAt(
            glm.vec3(self.ep),
            glm.vec3(self.ap),
            glm.vec3(self.up))
        view_loc=gl.glGetUniformLocation(self.shade_program,'view')
        gl.glUniformMatrix4fv(view_loc,1,gl.GL_FALSE,glm.value_ptr(self.view))
        self.drawGL()
        return

    def trans2D(self,oritrans):
        ve_z=glm.vec3(0,0,1)
        ve_AE=glm.vec3(self.ep-self.ap)
        ve_AE=glm.normalize(ve_AE)
        agl=glm.acos(glm.dot(ve_z,ve_AE))
        if abs(glm.cos(agl))==1:v_axis=glm.vec3(0,0,1)
        else:v_axis=glm.cross(ve_z,ve_AE)
        r1=glm.rotate(glm.mat4(1.0),agl,v_axis)
        ve_z=glm.vec4(ve_z,0)
        ve_z=r1*ve_z
        ve_z=glm.vec3(ve_z)
        if glm.dot(ve_z,ve_AE)<0.9:
            r1=glm.rotate(glm.mat4(1.0),-1*agl,v_axis)
        ftrans=oritrans*r1
        return ftrans

    def onPaint(self, e):
        self.SetCurrent(self.context)
        self.drawGL()
        e.Skip()
        return

    def onClk(self,e):
        TOR=0.05
        cpos=e.GetPosition()
        cx=2*cpos[0]/self.MinWidth-1
        cy=1-2*cpos[1]/self.MinHeight
        for dp in self.drawlist:
            if dp.Aro is None:continue
            if dp.dim==2:ftrans=self.trans2D(dp.trans)
            else:ftrans=glm.mat4(1.0)
            slct=False
            for p in dp.VA:
                glm_p=glm.vec4(p[0],p[1],p[2],1.0)
                glm_p=self.projection*self.view*ftrans*glm_p
                if abs(cx-glm_p[0]/glm_p[3])<TOR and abs(cy-glm_p[1]/glm_p[3])<TOR:
                    dp.highlight=True
                    slct=True
                    break
            if not slct:dp.highlight=False
        self.drawGL()
        return

    def onRoWhl(self,e):
        ZS=1    # Zoom speed;
        t=np.sign(e.WheelRotation)
        if self.whl_d==-10 and t>0:return
        if self.whl_d==15 and t<0:return

        v_ae=self.ep-self.ap
        z1=(v_ae)/np.linalg.norm(v_ae)    # ev_ae;
        x1=np.cross(self.up,z1)
        x1=x1/np.linalg.norm(x1)
        y1=np.cross(z1,x1)
        y1=y1/np.linalg.norm(y1)
        cpos=e.GetPosition()
        v_ac=0.414/ZS*np.array([
            (2*cpos.x/self.MinWidth-1)*self.k,
            1-2*cpos.y/self.MinHeight,
            0])
        v_ac=v_ac[0]*x1+v_ac[1]*y1
        self.ap=self.ap+t*v_ac-t/ZS*z1
        self.ep=self.ep+t*v_ac-t/ZS*z1
        self.whl_d-=t
        self.projMode()
        self.lookAt()
        e.Skip()
        return

    def onClkWhl(self,e):
        self.spos=e.GetPosition()
        e.Skip()
        return

    def onMove(self,e):
        if e.leftIsDown:pass
        if e.middleIsDown:
            cpos=e.GetPosition()
            self.up=np.array([0,1,0])
            dx=(cpos.x-self.spos.x)/self.MinHeight*math.pi
            dy=(self.spos.y-cpos.y)/self.MinHeight*math.pi
            self.spos=cpos
            v_ae=self.ep-self.ap
            r=np.linalg.norm(v_ae)
            tmp=v_ae[1]/r
            if abs(tmp)>1: tmp=1
            if v_ae[0]==0:
                theta=math.acos(tmp)
                psi=np.sign(v_ae[2])*math.pi/2
            else:
                psi=math.atan(v_ae[2]/v_ae[0])
                theta=math.acos(tmp)*np.sign(v_ae[0])
            if abs(theta)<0.1:
                if dy<0:dy=0
            elif abs(theta-math.pi)<0.1:
                if dy>0:dy=0
            if v_ae[0]==0:theta+=dy
            else:theta+=(dy*np.sign(v_ae[0]))
            psi+=dx
            v_ae=np.array([r*math.sin(theta)*math.cos(psi),
                r*math.cos(theta),
                r*math.sin(theta)*math.sin(psi)])
            self.ep=v_ae+self.ap
            self.lookAt()
        e.Skip()
        return

    def onClkViewBtn(self,e):
        lb=e.EventObject.Label
        if lb=='Oi':
            self.ep=np.array([5,5,5])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,1,0])
            self.drawlist[1]=xz_grid
            self.whl_d=0
        elif lb=='Xy':
            self.ep=np.array([0,0,5])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,1,0])
            self.drawlist[1]=xy_grid
            self.whl_d=0
        elif lb=='Xz':
            self.ep=np.array([0,-5,0])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,0,1])
            self.drawlist[1]=xz_grid
            self.whl_d=0
        elif lb=='Yz':
            self.ep=np.array([-5,0,0])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,1,0])
            self.drawlist[1]=yz_grid
            self.whl_d=0
        elif lb=='Ft':
            pass
        elif lb=='Gd':
            self.drawlist[1]=emp_grid
        elif lb=='Pp':
            self.viewPrep= not self.viewPrep
            self.projMode()
        self.lookAt()
        e.Skip()
        return

    def onDClkViewBtn(self,e):
        lb=e.EventObject.Label
        if lb=='Xy':
            self.ep=np.array([0,0,-5])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,1,0])
            self.drawlist[1]=xy_grid
            self.whl_d=0
        elif lb=='Xz':
            self.ep=np.array([0,5,0])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,0,1])
            self.drawlist[1]=xz_grid
            self.whl_d=0
        elif lb=='Yz':
            self.ep=np.array([5,0,0])
            self.ap=np.array([0,0,0])
            self.up=np.array([0,1,0])
            self.drawlist[1]=yz_grid
            self.whl_d=0
        self.lookAt()
        e.Skip()
        return

    pass
