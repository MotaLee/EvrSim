# Parent lib;
import core.esui as esui
wx=esui.wx
gmv=esui.gmv

# Move bar wx sub class;
class MoveBar(wx.ScrollBar):
    def __init__(self,parent,pos,siz,direction,exstl=0):
        if direction=='H':direction=wx.SB_HORIZONTAL
        else: direction=wx.SB_VERTICAL
        wx.ScrollBar.__init__(self,parent,-1,
            pos=(int(pos[0]),int(pos[1])),
            size=(int(siz[0]),int(siz[1])),
            style=direction | exstl)
        return

    pass
