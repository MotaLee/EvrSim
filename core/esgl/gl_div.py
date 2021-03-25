# System libs;
import wx
import wx.glcanvas as wg
# Built-in libs;
from core import ESC,esgl,esui
GLC=esgl.glc
class GLDiv(wg.GLCanvas):
    ''' Aro OpenGL Canvas.
        Para accepts: `backgroundColor`: tuple4.'''
    def __init__(self,parent,p,s,**argkw):
        wg.GLCanvas.__init__(self,parent,pos=p,size=s,
            style=wx.NO_BORDER | wg.WX_GL_RGBA | wg.WX_GL_DOUBLEBUFFER | wg.WX_GL_DEPTH_SIZE)
        GLC.GLDIV=self
        GLC.RATIO_WH=self.Size.x/self.Size.y
        GLC.GLDIV_WIDTH=self.Size.x
        GLC.GLDIV_HEIGHT=self.Size.y

        self.Bind(esui.EBIND_COMEVT,self.onComEvt)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND,lambda e: None)
        # Initilize opengl;
        self.context = wg.GLContext(self)
        self.SetCurrent(self.context)
        GLC.initGL()
        self.Hide()
        return

    def readMap(self,clear=False):
        GLC.readMap(clear)
        return

    def onComEvt(self,e:esui.ESEvent):
        subtype=e.getEventArgs()
        if subtype==esui.ETYPE_UPDATE_MAP:
            self.readMap()
        elif subtype==esui.ETYPE_OPEN_SIM:
            self.readMap()
            GLC.lookAt()
            self.Show()
        elif subtype==esui.ETYPE_RESET_SIM:
            ESC.resetSim()
            self.readMap()
        return

    def onPaint(self,e):
        self.SetCurrent(self.context)
        GLC.drawGL()
        e.Skip()
        return
    pass
