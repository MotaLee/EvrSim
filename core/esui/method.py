from core import esui
def toggleWorkspace(target=''):
    if target is None:
        status=esui.ARO_PLC.IsShown()
    else:status=False
    if status or target=='ACP':
        esui.ARO_PLC.Hide()
        esui.ACP_PLC.Show()
        esui.ACP_PLC.drawConnection()
    elif not status or target=='ARO':
        esui.ARO_PLC.Show()
        esui.ACP_PLC.Hide()
    return
