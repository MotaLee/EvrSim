# System libs;
import sys
import ctypes
import time
# Outer libs;
import wx,glm
import wx.glcanvas as wg
import OpenGL.GL as gl
import numpy as np

# Built-in libs;
from core import ESC
from core import esui
from core import esgl
from core import esevt
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
        self.aro_selection=[]   # Aroes in list;
        self.shade_program=None

        if 'backgroundColor' in argkw:self.bg=argkw['backgroundColor']
        else:self.bg=(0,0,0,1)

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(wx.EVT_PAINT, self.onPaint)

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
        gl.glClearColor(self.bg[0],self.bg[1],self.bg[2],self.bg[3])    # 设置画布背景色
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.shade_program = esgl.genGLProgram()
        esgl.GL_PROGRAM=self.shade_program
        self.pos_loc=gl.glGetAttribLocation(self.shade_program,'in_pos')
        self.color_loc=gl.glGetAttribLocation(self.shade_program,'in_color')
        self.trans_loc=gl.glGetUniformLocation(self.shade_program,'trans')
        self.hl_loc=gl.glGetUniformLocation(self.shade_program,'highlight')
        self.ht_loc=gl.glGetUniformLocation(self.shade_program,'has_texture')
        self.tex_loc=gl.glGetAttribLocation(self.shade_program,'in_texture')

        esgl.projMode()
        # esgl.lookAt()
        return

    def drawGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        all_adp=list()
        for adplist in esgl.ADP_DICT.values():
            all_adp+=adplist
        # for dp in esgl.TDP_LIST:
        for dp in esgl.TDP_LIST+all_adp:
            if not dp.visible or dp.VA.size==0:continue
            if dp.VAO==-1:
                VAO,VBO,EBO=esgl.genGLO()
                dp.VAO,dp.VBO,dp.EBO=VAO,VBO,EBO
                esgl.bindGLO(VAO,VBO,EBO)
            else:esgl.bindGLO(dp.VAO,dp.VBO,dp.EBO)
            if dp.update_data:
                esgl.bindBufferData(dp.VA,dp.EA)
                dp.update_data=False

            dp.viewDP()
            vertex_len=len(dp.VA[0])
            gl.glVertexAttribPointer(self.pos_loc,3, gl.GL_FLOAT, gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(0))
            gl.glVertexAttribPointer(self.color_loc,4,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(12))
            gl.glEnableVertexAttribArray(0)
            gl.glEnableVertexAttribArray(1)
            if vertex_len>7:
                gl.glUniform1iv(self.ht_loc,1,1)
                gl.glVertexAttribPointer(self.tex_loc,2,gl.GL_FLOAT,gl.GL_FALSE,4*vertex_len,ctypes.c_void_p(28))
                gl.glEnableVertexAttribArray(2)
                if dp.TAO==-1:
                    dp.TAO=esgl.genGLTexture(dp.texture)
                else:
                    gl.glBindTexture(gl.GL_TEXTURE_2D,dp.TAO)
            else:gl.glUniform1iv(self.ht_loc,1,0)

            gl.glUniformMatrix4fv(self.trans_loc,1,gl.GL_FALSE,glm.value_ptr(dp.ftrans))

            if dp.highlight:hl=1
            else: hl=0
            gl.glUniform1iv(self.hl_loc,1,hl)

            if len(dp.EA)!=0:gl.glDrawElements(dp.gl_type,dp.EA.size,gl.GL_UNSIGNED_INT,None)
            elif len(dp.VA)>1:gl.glDrawArrays(dp.gl_type,0,dp.VA.size)
        self.SwapBuffers()

        for ctrl in self.Children:
            if type(ctrl)==esui.TransText:ctrl.Refresh()
        return

    def readMap(self,clear=False):
        if clear:esgl.ADP_DICT=dict()
        for aro in ESC.ARO_MAP.values():
            if aro.AroID not in esgl.ADP_DICT:
                if aro.adp!='':
                    adplist=esgl.initADP(aro)
                    esgl.ADP_DICT[aro.AroID]=adplist
                    for adp in adplist:
                        adp.viewDP()
            else:
                for adp in esgl.ADP_DICT[aro.AroID]:
                        # adp.update_data=True
                    adp.updateDP(aro)
                    # adp.viewDP()
        self.drawGL()
        return

    def highlightADP(self,selection=None):
        ''' Set Aroes in selection highlighted and selected.

            Para selection: Accept Aro/es.'''
        if selection is None:
            selection=list()
            for aro in self.aro_selection:
                selection.append(aro)
        elif not isinstance(selection,list):
            selection=[selection]
        self.aro_selection=selection
        for adplist in esgl.ADP_DICT.values():
            for adp in adplist:
                if adp.Aro in selection:adp.highlight=True
                else:adp.highlight=False
        self.drawGL()
        return

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
            self.readMap(clear=True)
        elif etype==esevt.ETYPE_OPEN_SIM:
            # self.readMap()
            esgl.lookAt()
            self.Show()
        elif etype==esevt.ETYPE_RESET_SIM:
            ESC.resetSim()
            self.readMap()
        for tool in self.tool_list:
            esevt.sendEvent(etype,target=tool)
        return

    def onPaint(self,e):
        self.SetCurrent(self.context)
        self.drawGL()
        e.Skip()
        return
    pass
