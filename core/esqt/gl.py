import numpy as np
import PySide6.QtOpenGLWidgets as qglw
from . import qc,qg,qt,QUIBase
from . import ESQTAPP,SIG_OPEN_SIM,CW,CH,SIG_UPDATE_MAP
from core import esc,esgl
ESC=esc.ESC
GLC=esgl.GLC
glm=esgl.glm
class GLBox(qglw.QOpenGLWidget,QUIBase):
    def __init__(self, parent: qt.QWidget, **argkw):
        qglw.QOpenGLWidget.__init__(self,parent)
        QUIBase.__init__(self,**argkw)
        self.enum_slt=esc.EsEnum(['deact','pick','rect','picktop'],prev='pick')
        # GLC.setShell(self.w,self.h,self)
        GLC.setShell(self.w,self.h,self)
        ESQTAPP.bindSignal(self.onOpenSim,SIG_OPEN_SIM)
        ESQTAPP.bindSignal(self.onUpdateMap,SIG_UPDATE_MAP)
        fmt =qg.QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(qg.QSurfaceFormat.CoreProfile)
        self.setFormat(fmt)
        self._drawGL=GLC.drawGL
        GLC.drawGL=self.update
        return

    def onOpenSim(self,e):
        GLC.readMap()
        return

    def onUpdateMap(self,e):
        GLC.readMap()
        return

    def readMap(self,clear=False):
        GLC.readMap(clear)
        return

    def initializeGL(self):
        GLC.initGL()
        # import OpenGL.GL as gl
        # gl.glClearColor(0.2, 0.4, 0.52, 1.0)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        return

    def paintGL(self):
        if self.isVisible():
            # GLC.drawGL()
            self._drawGL()
            # import OpenGL.GL as gl
            # gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            # gl.glLoadIdentity()

            # #gl.glRotated(30.0, 1.0, 0.0, 0.0)
            # gl.glBegin(gl.GL_TRIANGLES)
            # gl.glColor3d(1.0, 0.0, 0.0)
            # gl.glVertex3d(0.0, 1.0, 0.0)
            # gl.glColor3d(0.0, 1.0, 0.0)
            # gl.glVertex3d(-1.0, -1.0, 0.0)
            # gl.glColor3d(0.0, 0.0, 1.0)
            # gl.glVertex3d(1.0, -1.0, 0.0)
            # gl.glEnd()
        return

    def resizeGL(self, w: int, h: int) -> None:
        GLC.setShell(w,h,self)
        self._drawGL()
        return

    pass
