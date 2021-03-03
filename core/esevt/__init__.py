# Libs;
import wx
# Event type;
ETYPE_COMEVT = wx.NewEventType()
ETYPE_NEW_SIM = wx.NewEventType()
ETYPE_OPEN_SIM = wx.NewEventType()
ETYPE_SAVEAS_SIM = wx.NewEventType()
ETYPE_RUN_SIM = wx.NewEventType()
ETYPE_RESET_SIM = wx.NewEventType()
ETYPE_CLOSE_SIM = wx.NewEventType()

ETYPE_UPDATE_MAP = wx.NewEventType()
ETYPE_UPDATE_MODEL = wx.NewEventType()

ETYPE_LOAD_MOD = wx.NewEventType()

ETYPE_SIM_CIRCLED = wx.NewEventType()
ETYPE_KEY_DOWN = wx.NewEventType()

ETYPE_OPEN_CMD = wx.NewEventType()
ETYPE_CLOSE_CMD = wx.NewEventType()

ETYPE_CLOSE_ES = wx.NewEventType()


# Event binder;
EVT_COMMON_EVENT = wx.PyEventBinder(ETYPE_COMEVT, 1)
EVT_NEW_SIM = wx.PyEventBinder(ETYPE_NEW_SIM, 1)
EVT_OPEN_SIM = wx.PyEventBinder(ETYPE_OPEN_SIM, 1)
EVT_SAVEAS_SIM = wx.PyEventBinder(ETYPE_SAVEAS_SIM, 1)
EVT_RUN_SIM = wx.PyEventBinder(ETYPE_RUN_SIM, 1)
EVT_RESET_SIM = wx.PyEventBinder(ETYPE_RESET_SIM, 1)
EVT_CLOSE_SIM = wx.PyEventBinder(ETYPE_CLOSE_SIM, 1)

EVT_UPDATE_MAP =wx.PyEventBinder(ETYPE_UPDATE_MAP, 1)
EVT_UPDATE_MODEL =wx.PyEventBinder(ETYPE_UPDATE_MODEL, 1)
EVT_LOAD_MOD = wx.PyEventBinder(ETYPE_LOAD_MOD, 1)
EVT_SIM_CIRCLED = wx.PyEventBinder(ETYPE_SIM_CIRCLED, 1)
EVT_LEFT_DOWN = wx.PyEventBinder(ETYPE_KEY_DOWN, 1)

# EvrSim Custom event;
class EvrSimEvent(wx.PyCommandEvent):
    def __init__(self,evtType,id):
        wx.PyCommandEvent.__init__(self,evtType,id)
        self.eventArgs=None
        return

    def GetEventArgs(self,index=0):
        if type(self.eventArgs)!=list:
            out=self.eventArgs
        else:out=self.eventArgs[index]
        return out

    def SetEventArgs(self,args):
        self.eventArgs = args
        return
    pass


def sendEvent(etype,args=None,target=None):
    ''' Para target: None for wxmw main window;'''
    from core import esui
    evt =EvrSimEvent(etype,-1)
    evt.SetEventArgs(args)
    if target is None:
        esui.IDX.ESMW.GetEventHandler().ProcessEvent(evt)
        for plc in esui.IDX.ESMW.Children:
            plc.GetEventHandler().ProcessEvent(evt)
    else:target.ProcessEvent(evt)
    return
