from core import esui
def toggleWorkspace(target=None):
    if target is None:
        status=esui.IDX.MAP_DIV.IsShown()
    else:status=False
    if status or target=='ACP':
        esui.IDX.MAP_DIV.Hide()
        esui.IDX.MDL_DIV.Show()
        esui.IDX.MDL_DIV.drawConnection()
    elif not status or target=='ARO':
        esui.IDX.MAP_DIV.Show()
        esui.IDX.MDL_DIV.Hide()
    return
