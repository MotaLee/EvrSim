import threading,time
import wx
import wx.glcanvas as wg

class GLThreadRender(threading.Thread):
    def __init__(self,glc):
        threading.Thread.__init__(self,daemon=True)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter
        self.glc=glc
        self._list_cmd=list()
        self._flag_ctn=True
        self.frame=wx.Frame(None)
        self.frame.Hide()
        self.canvas=wg.GLCanvas(self.frame,
            style=wx.NO_BORDER | wg.WX_GL_RGBA | wg.WX_GL_DOUBLEBUFFER | wg.WX_GL_DEPTH_SIZE)
        self.context=wg.GLContext(self.canvas,self.glc.GL_CONTEXT)
        self.start()
        return
    def run(self):
        while self._flag_ctn:
            if len(self._list_cmd):
                cmd=self._list_cmd.pop(0)
                if cmd=='draw':
                    self.context.SetCurrent(self.canvas)
                    self.glc.initGL()
                    self.glc.drawGL()
                    # print(cmd)
            time.sleep(0.01)
        return

    def send(self,cmd):
        self._list_cmd.append(cmd)
        return
