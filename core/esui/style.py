import wx
from core import esui
class Style(dict):
    def __init__(self,**argkw) -> None:
        ''' Style for esui control. Para argkw supports:
            * border: Color of all border, transparent default.
            * fgc/bgc:.
            * hover:.'''
        super().__init__(**argkw)
        self.style_hover=argkw.get('hover',None)
        return

    def draw(self,dc,e):
        return
    pass
