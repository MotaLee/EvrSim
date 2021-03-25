import wx
from core import esui
def toggleWorkspace(target=None):
    if target is None:
        status=esui.UMR.MAP_DIV.IsShown()
    else:status=False
    if status or target=='ACP':
        esui.UMR.MAP_DIV.Hide()
        esui.UMR.MDL_DIV.Show()
        esui.UMR.MDL_DIV.drawConnection()
    elif not status or target=='ARO':
        esui.UMR.MAP_DIV.Show()
        esui.UMR.MDL_DIV.Hide()
    return

def getTextExtent(text,font):
    dc=wx.ClientDC(esui.UMR.ESMW)
    dc.SetFont(font)
    et:tuple=dc.GetTextExtent(text)
    return et
