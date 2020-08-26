# System libs;
import sys
import ctypes
# Outer libs;
import wx
import glm
import interval
import wx.glcanvas as wg
import OpenGL.GL as gl
import numpy as np

# Built-in libs;
from core import ESC
from core import esui
from core import esgl
from core import esevt
from .AroToolPlc import AroToolbarPlc
import mod

class AroGlc(wg.GLCanvas):
    ''' Aro OpenGL Canvas.

        Para accepts: `backgroundColor`: tuple4.'''
    def __init__(self,parent,p,s,**argkw):
        wg.GLCanvas.__init__(self,parent,pos=p,size=s,
            style=wx.NO_BORDER | wg.WX_GL_RGBA | wg.WX_GL_DOUBLEBUFFER | wg.WX_GL_DEPTH_SIZE)

        esgl.ASPECT_RATIO=self.Size[0]/self.Size[1]
        esgl.PLC_W=self.Size[0]
        esgl.PLC_H=self.Size[1]

        self.tool_list=list()
        self.spos=(0,0)     # Start cursor postion;
        self.aro_selection=[]
        self.shade_program=None

        self.toolbar=AroToolbarPlc(self,(0,0),(4*esui.YU,self.Size[1]))

        if 'backgroundColor' in argkw:
            self.bg=argkw['backgroundColor']
        else:self.bg=(0,0,0,1)

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onClk)
        self.Bind(wx.EVT_LEFT_UP, self.onRls)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDClk)
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

        # gl.glEnable(gl.GL_DEPTH_TEST)   # 开启深度测试，实现遮挡关系
        gl.glEnable(gl.GL_BLEND)            # 开启混合
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)           # 设置混合函数
        # gl.glEnable(gl.GL_LINE_SMOOTH)  # 开启线段反走样
        # glDepthFunc(GL_LEQUAL)      # 设置深度测试函数
        # glShadeModel(GL_SMOOTH)      # GL_SMOOTH(光滑着色)/GL_FLAT(恒定着色)
        # gl.glEnable(gl.GL_ALPHA_TEST)                   # 启用Alpha测试
        # gl.glAlphaFunc(gl.GL_GREATER, 0.1)        # 设置Alpha测试条件为大于05则通过
        # glFrontFace(GL_CW)               # 设置逆时针索引为正面（GL_CCW/GL_CW）
        # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        gl.glClearColor(self.bg[0],self.bg[1],self.bg[2],self.bg[3])    # 设置画布背景色
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.shade_program = esgl.genGLProgram()
        esgl.GL_PROGRAM=self.shade_program

        esgl.projMode()
        self.lookAt()
        return

    def drawGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        for dp in esgl.TDP_LIST+esgl.ADP_LIST:
            VA=dp.VA
            EA=dp.EA
            if not dp.visible or VA.size==0:continue
            if dp.VAO==-1:
                VAO,VBO,EBO=esgl.genGLO()
                dp.VAO,dp.VBO,dp.EBO=VAO,VBO,EBO
                esgl.bindGLO(VAO,VBO,EBO)
            else:esgl.bindGLO(dp.VAO,dp.VBO,dp.EBO)
            if dp.update_data:
                esgl.bindBufferData(VA,EA)
                dp.update_data=False

            vertex_len=len(VA[0])
            pos_loc=gl.glGetAttribLocation(self.shade_program,'in_pos')
            gl.glVertexAttribPointer(pos_loc,3, gl.GL_FLOAT, gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(0))
            gl.glEnableVertexAttribArray(0)
            color_loc=gl.glGetAttribLocation(self.shade_program,'in_color')
            gl.glVertexAttribPointer(color_loc,4,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(12))
            gl.glEnableVertexAttribArray(1)

            ht_loc=gl.glGetUniformLocation(self.shade_program,'has_texture')
            if vertex_len>7:
                gl.glUniform1iv(ht_loc,1,1)
                tex_loc=gl.glGetAttribLocation(self.shade_program,'in_texture')
                gl.glVertexAttribPointer(tex_loc,2,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(28))
                gl.glEnableVertexAttribArray(2)
                if dp.TAO==-1:dp.TAO=esgl.genGLTexture(dp.texture)
                else:gl.glBindTexture(gl.GL_TEXTURE_2D,dp.TAO)
            else:gl.glUniform1iv(ht_loc,1,0)

            dp.transDP()
            trans_loc=gl.glGetUniformLocation(self.shade_program,'trans')
            gl.glUniformMatrix4fv(trans_loc,1,gl.GL_FALSE,glm.value_ptr(dp.ftrans))

            if dp.highlight:hl=1
            else: hl=0
            hl_loc=gl.glGetUniformLocation(self.shade_program,'highlight')
            gl.glUniform1iv(hl_loc,1,hl)

            if len(EA)!=0:gl.glDrawElements(dp.gl_type,EA.size,gl.GL_UNSIGNED_INT,None)
            elif len(VA)>1:gl.glDrawArrays(dp.gl_type,0,VA.size)
        self.SwapBuffers()

        for ctrl in self.Children:
            if type(ctrl)==esui.TransText:ctrl.Refresh()
        return

    def readMap(self):
        esgl.ADP_LIST=list()
        for aro in ESC.ARO_MAP:
            if aro.adp!='':
                adplist=esgl.initADP(aro)
                esgl.ADP_LIST+=adplist
        self.drawGL()
        return

    def highlightADP(self,aroidlist=None):
        if aroidlist is None:
            aroidlist=list()
            for aro in self.aro_selection:
                aroidlist.append(aro.AroID)
        elif type(aroidlist)!=list():
            aroidlist=[aroidlist]
        for adp in esgl.ADP_LIST:
            if adp.Aro.AroID in aroidlist:adp.highlight=True
            else:adp.highlight=False
        self.drawGL()
        return

    def lookAt(self,ep=None,ap=None,up=None):

        esgl.MAT_VIEW=glm.lookAt(
            glm.vec3(esgl.EP.tolist()),
            glm.vec3(esgl.AP.tolist()),
            glm.vec3(esgl.UP.tolist()))
        view_loc=gl.glGetUniformLocation(self.shade_program,'view')
        gl.glUniformMatrix4fv(view_loc,1,gl.GL_FALSE,glm.value_ptr(esgl.MAT_VIEW))
        self.drawGL()
        return

    def normPos(self,p):
        px=2*p[0]/self.Size[0]-1
        py=1-2*p[1]/self.Size[1]
        return (px,py)

    def regToolEvent(self,tool):
        if tool not in self.tool_list:
            self.tool_list.append(tool)
            tool.SetExtraStyle(wx.WS_EX_BLOCK_EVENTS)
        else:
            self.tool_list.remove(tool)
        return

    def onComEvt(self,e):
        etype=e.GetEventArgs()
        if etype==esevt.ETYPE_UPDATE_MAP:
            self.readMap()
        elif etype==esevt.ETYPE_OPEN_SIM:
            self.Show()
        elif etype==esevt.ETYPE_RESET_SIM:
            ESC.loadMapFile()
            self.readMap()
        for tool in self.tool_list:
            esevt.sendEvent(etype,target=tool)
        return

    def onPaint(self,e):
        self.SetCurrent(self.context)
        self.drawGL()
        e.Skip()
        return

    def onClk(self,e):
        TOR=0.05
        cpos=e.GetPosition()
        cx,cy=self.normPos(cpos)
        self.spos=cpos
        if self.toolbar.selecting:
            if e.controlDown:
                for adp in esgl.ADP_LIST:
                    if not hasattr(adp.Aro,'position'):continue
                    slct=False
                    for p in adp.VA:
                        p_2d=esgl.getPosFromVertex(adp,p)
                        if abs(cx-p_2d[0])<TOR and abs(cy-p_2d[1])<TOR:
                            self.aro_selection.append(adp.Aro)
                            adp.highlight=True
                            slct=True
                            break
                    if slct:break
            else:
                self.aro_selection=[]
                for adp in esgl.ADP_LIST:
                    if not hasattr(adp.Aro,'position'):continue
                    slct=False
                    for p in adp.VA:
                        p_2d=esgl.getPosFromVertex(adp,p)
                        if abs(cx-p_2d[0])<TOR and abs(cy-p_2d[1])<TOR:
                            self.aro_selection=[adp.Aro]
                            adp.highlight=True
                            slct=True
                            break
                    if slct:break
                    else:adp.highlight=False
        else:pass
        self.drawGL()
        return

    def onRls(self,e):
        if self.toolbar.rect_selecting:
            self.aro_selection=[]
            cpos=e.GetPosition()
            cx,cy=self.normPos(cpos)
            sx,sy=self.normPos(self.spos)
            for adp in esgl.ADP_LIST:
                if not hasattr(adp.Aro,'position'):continue
                slct=False
                for p in adp.VA:
                    p_2d=esgl.getPosFromVertex(adp,p)
                    c1=p_2d[0] in interval.Interval(cx,sx)
                    c2=p_2d[1] in interval.Interval(cy,sy)
                    if c1 and c2:
                        self.aro_selection.append(adp.Aro)
                        adp.highlight=True
                        slct=True
                        break
                if not slct:adp.highlight=False
            self.spos=cpos
            self.drawGL()
        return

    def onDClk(self,e):
        if len(self.aro_selection)==1:
            esui.SIDE_PLC.showDetail(self.aro_selection[0].AroID)

        return

    def onRoWhl(self,e):
        t=np.sign(e.WheelRotation)
        if esgl.WHEEL_DIS==-10 and t>0:return
        if esgl.WHEEL_DIS==15 and t<0:return
        cpos=e.GetPosition()
        cx,cy=self.normPos(cpos)

        v_ae=esgl.EP-esgl.AP
        z1=(v_ae)/np.linalg.norm(v_ae)    # ev_ae;
        x1=np.cross(esgl.UP,z1)
        x1=x1/np.linalg.norm(x1)
        y1=np.cross(z1,x1)
        y1=y1/np.linalg.norm(y1)
        v_ac=0.414/esgl.ZS*np.array([cx*esgl.ASPECT_RATIO,cy,0])
        v_ac=v_ac[0]*x1+v_ac[1]*y1
        esgl.AP=esgl.AP+t*v_ac-t/esgl.ZS*z1
        esgl.EP=esgl.EP+t*v_ac-t/esgl.ZS*z1
        esgl.WHEEL_DIS-=t
        esgl.projMode()
        self.lookAt()
        e.Skip()
        return

    def onClkWhl(self,e):
        self.spos=e.GetPosition()
        e.Skip()
        return

    def onMove(self,e):
        if e.leftIsDown and self.toolbar.rect_selecting:
            cpos=e.GetPosition()
            self.drawGL()
            dc=wx.ClientDC(self)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(wx.Pen(esui.COLOR_FRONT))
            dc.DrawRectangle(self.spos[0],self.spos[1],
                cpos[0]-self.spos[0],cpos[1]-self.spos[1])
        elif e.middleIsDown:
            cpos=e.GetPosition()
            esgl.UP=np.array([0,1,0])
            dx=(cpos.x-self.spos.x)/self.Size[1]*glm.pi()
            dy=(self.spos.y-cpos.y)/self.Size[1]*glm.pi()
            self.spos=cpos
            v_ae=esgl.EP-esgl.AP
            r=np.linalg.norm(v_ae)
            tmp=v_ae[1]/r
            if abs(tmp)>1: tmp=1
            if v_ae[0]==0:
                theta=glm.acos(tmp)
                psi=np.sign(v_ae[2])*glm.pi()/2
            else:
                psi=glm.atan(v_ae[2]/v_ae[0])
                theta=glm.acos(tmp)*np.sign(v_ae[0])
            if abs(theta)<0.1:
                if dy<0:dy=0
            elif abs(theta-glm.pi())<0.1:
                if dy>0:dy=0
            if v_ae[0]==0:theta+=dy
            else:theta+=(dy*np.sign(v_ae[0]))
            psi+=dx
            v_ae=np.array([r*glm.sin(theta)*glm.cos(psi),
                r*glm.cos(theta),
                r*glm.sin(theta)*glm.sin(psi)])
            esgl.EP=v_ae+esgl.AP
            self.lookAt()
        e.Skip()
        return
    pass
