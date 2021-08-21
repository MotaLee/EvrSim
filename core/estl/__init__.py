import wx
from core import ESC,esui,esgl
GLC=esgl.GLC
yu=esui.YU
xu=esui.XU

def getToolByName(toolname:str,modname:str):
    ''' Get tool by its name and mod/app name;'''
    try:
        import mod,app
        if hasattr(mod,modname):
            tool:ToolBase=eval('mod.'+modname+'.'+toolname)
        else:
            tool:ToolBase=eval('app.'+modname+'.'+toolname)
    except BaseException:
        ESC.err('Tool not found.')
    return tool

class ToolBase(object):
    def __init__(self,name:str,mod:str):
        ''' Tool base class.
            Mod custom tool need this class to be indexed.
            * Para name: Particular. Shold be the same with attribute name in mod;
            * Para mod: Mod name where tool located;
            * Attr '''
        self.name=name
        self.mod=mod
        self.fullname=self.mod+'.'+self.name
        return
    pass

class GLTool(esui.Div):
    def __init__(self,**argkw):
        super().__init__(esui.UMR.MAP_DIV,**argkw)
        self.tdp=None
        self.Hide()
        return

    def addToGL(self):
        GLC.addTdp(id(self),self.tdp)
        return
    pass

class ToggleButton(esui.TglBtn,ToolBase):
    def __init__(self,parent,name,mod,**argkw):
        ToolBase.__init__(self,name,mod)
        esui.TglBtn.__init__(self,parent,**argkw)
        return
    pass

class Button(esui.DivBtn,ToolBase):
    'Lv:2: Second tool class. Build Btn ctrl;'
    def __init__(self,parent,name,mod,**argkw):
        esui.DivBtn.__init__(self,parent,**argkw)
        ToolBase.__init__(self,name,mod)
        return
    pass

class SelectMenu(esui.MenuBtnDiv,ToolBase):
    def __init__(self,parent,name,mod,**argkw):
        argkw['select']=True
        esui.MenuBtnDiv.__init__(self,parent,**argkw)
        ToolBase.__init__(self,name,mod)
        return
    pass

class Bar(esui.Div,ToolBase):
    def __init__(self,parent,name,mod,**argkw):
        esui.Div.__init__(self,parent,**argkw)
        ToolBase.__init__(self,name,mod)
        self.updateStyle(style={'bgc':esui.COLOR_FRONT})
        return
    pass

class Input(esui.InputText,ToolBase):
    def __init__(self,parent,name,mod,**argkw):
        esui.InputText.__init__(self,parent,**argkw)
        ToolBase.__init__(self,name,mod)
        return
    pass

from .tool_div import ToolDiv,ModTab
from .aro_toolbar import AroToolbar
from .msg_div import MsgDiv
from .mdl_div import MdlDiv

from .side_div import SideDiv
from .cmd_div import CmdDiv
from .head_div import HeadDiv,HeadBar
