# System libs;
import sys,ctypes
import wx
import wx.glcanvas as wg
import OpenGL.GL as gl
import numpy as np
import _glm as glm

# Built-in libs;
from core import ESC,esui,esgl,esevt
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
        # self.spos=(0,0)     # Start cursor postion;

        if 'backgroundColor' in argkw:self.bg=argkw['backgroundColor']
        else:self.bg=(0,0,0,1)

        self.Bind(esevt.EVT_COMMON_EVENT,self.onComEvt)
        self.Bind(wx.EVT_PAINT, self.onPaint)

        # Initilize opengl;
        self.context = wg.GLContext(self)
        self.SetCurrent(self.context)
        esgl.initGL()
        self.Hide()
        return

    def readMap(self,clear=False):
        if clear:esgl.ADP_DICT.clear()
        aid_remain=list(esgl.ADP_DICT.keys())
        for aro in ESC.ARO_MAP.values():
            if aro.AroID not in esgl.ADP_DICT:
                if aro.adp!='':
                    adplist=esgl.initADP(aro)
                    esgl.ADP_DICT[aro.AroID]=adplist
                    # for adp in adplist:adp.trans=esgl.fixViewDP(adp)
            else:
                for adp in esgl.ADP_DICT[aro.AroID]:
                    adp.updateADP()
                aid_remain.remove(aro.AroID)
        for aid in aid_remain:del esgl.ADP_DICT[aid]
        esgl.drawGL()
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
            self.readMap()
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
        esgl.drawGL()
        e.Skip()
        return
    pass
