import mod
from core import ESC
from core import esui
from core import esgl

def getToolByName(toolname,modname):
    # ''' Para mod: empty for self mod.;'''
    TOOL_INDEX=eval('mod.'+modname+'.TOOL_INDEX')
    if toolname in TOOL_INDEX:
        return eval('mod.'+modname+'.'+toolname)
    else:
        ESC.bug('E: Tool not found.')
        return

class BaseTool(object):
    'Lv:1: Base tool class. Only build base var;'
    def __init__(self,name,label='',p=(0,0),s=(0,0),host='MOD_PLC'):
        self.name=name
        self.label=label
        self.p=p
        self.s=s
        self.host=host  # 'MOD_PLC' default, or 'ARO_PLC';
        self.ctrl=None
        self.tdp=None
        return

    def build(self,parent):
        # self.ctrl=None
        return

    pass

class StaticDPTool(BaseTool):
    def __init__(self,name):
        super().__init__(name,host='ARO_PLC')
        # self.tdp=TdpXyzAxis(self)
        return

    def build(self,parent):
        esgl.TDP_LIST.append(self.tdp)
        return
    pass

class CreateTool(BaseTool):
    'Lv:2: Second tool class. Build MenuBtn ctrl;'
    def __init__(self,name,label,p,s,items):
        super().__init__(name,label,p,s)
        self.items=items
        return

    def build(self,parent):
        self.ctrl=esui.MenuBtn(parent,
            self.p,self.s,
            self.label,self.items)
        self.ctrl.name=self.name
        self.ctrl.shell=self
        return
    pass

class ToggleTool(BaseTool):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,label,p,s,state=False,tip=''):
        super().__init__(name,label,p,s)
        self.state=state
        self.tip=tip
        return

    def build(self,parent):
        self.ctrl=esui.SelectBtn(parent,
            self.p,self.s,
            self.label,
            select=self.state,
            tip=self.tip,tsize=self.s[1]/2)
        self.ctrl.name=self.name
        self.ctrl.shell=self
        return
    pass

class TextTool(BaseTool):
    'Lv:2: Second tool class. Build SelectBtn ctrl;'
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        self.ctrl=esui.Stc(parent,self.p,self.s,
            self.label,
            tsize=self.s[1]/2)
        self.ctrl.name=self.name
        self.ctrl.shell=self
        return
    pass

class ButtonTool(BaseTool):
    'Lv:2: Second tool class. Build Btn ctrl;'
    def __init__(self,name,label,p,s):
        super().__init__(name,label,p,s)
        return

    def build(self,parent):
        self.ctrl=esui.btn(parent,self.p,self.s,
            self.label)
        self.ctrl.name=self.name
        self.ctrl.shell=self
        return
    pass

class SelectMenuTool(BaseTool):
    def __init__(self,name,label,p,s,items=[]):
        super().__init__(name,label,p,s)
        self.items=items
        return

    def build(self,parent):
        self.ctrl=esui.SelectMenuBtn(parent,
            self.p,self.s,
            self.label,self.items)
        self.ctrl.name=self.name
        self.ctrl.shell=self
        return
    pass
