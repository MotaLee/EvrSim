import mod
from core import ESC,esui,esgl


def getToolByName(toolname,modname):
    try:
        tool=eval('mod.'+modname+'.'+toolname)
        return tool
    except BaseException:
        ESC.err('Tool not created.')

class BaseTool(object):
    'Lv:1: Base tool class. Only build base var;'
    def __init__(self,name:str):
        self.name=name
        self.fullname=self.__module__+self.name
        return
    pass

class GLTool(BaseTool):
    def __init__(self,name):
        super().__init__(name)
        self.tdp=None
        return

    def addToGL(self):
        esgl.DICT_TDP.add(self.fullname,self.tdp)
        return
    pass

class UIGLTool(GLTool,esui.Plc):
    def __init__(self,name,p=(0,0),s=(0,0)):
        GLTool.__init__(self,name)
        esui.Plc.__init__(self,esui.ARO_PLC,p,s,cn=name)
        return
    pass

class CreateMenuTool(BaseTool,esui.MenuBtn):
    'Lv:2: Second tool class. Build MenuBtn ctrl;'
    def __init__(self,name,parent,p,s,label,items):
        BaseTool.__init__(self,name)
        esui.MenuBtn.__init__(self,parent,p,s,label,items)
        self.items=items
        return
    pass

class ToggleTool(BaseTool,esui.SltBtn):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,parent,p,s,label,select=False,tip=''):
        BaseTool.__init__(self,name)
        esui.SltBtn.__init__(self,parent,p,s,label,tip=tip,select=select,tsize=s[1]/2)
        return
    pass

class TextTool(BaseTool,esui.StaticText):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,parent,p,s,label):
        BaseTool.__init__(self,name)
        esui.StaticText.__init__(self,parent,p,s,label)
        return
    pass

class ButtonTool(BaseTool,esui.Btn):
    'Lv:2: Second tool class. Build Btn ctrl;'
    def __init__(self,name,parent,p,s,label):
        BaseTool.__init__(self,name)
        esui.Btn.__init__(self,parent,p,s,label)
        return
    pass

class SelectMenuTool(BaseTool,esui.SelectMenuBtn):
    def __init__(self,name,parent,p,s,label,items=[]):
        BaseTool.__init__(self,name)
        esui.SelectMenuBtn.__init__(self,parent,p,s,label,items)
        self.items=items
        return
    pass

class BarTool(BaseTool,esui.Plc):
    def __init__(self,name,parent,p,s):
        BaseTool.__init__(self,name)
        esui.Plc.__init__(self,parent,p,s)
        self.SetBackgroundColour(esui.COLOR_FRONT)
        return
    pass

class InputTool(BaseTool,esui.InputText):
    def __init__(self,name,parent,p,s,label):
        BaseTool.__init__(self,name)
        esui.InputText.__init__(self,parent,p,s,hint=label)
        return
    pass

from .tool_plc import ToolPlc
from .aro_toolbar import AroToolbar
