# Libs;
import wx

# EvrSim Custom event;
class EvrSimEvent(wx.PyCommandEvent):
    def __init__(self,evtType,id):
        wx.PyCommandEvent.__init__(self,evtType,id)
        self.eventArgs=""
        return

    def GetEventArgs(self):
        return self.eventArgs

    def SetEventArgs(self,args):
        self.eventArgs = args
        return
    pass

# Event type;
esEVT_COMMON_EVENT = wx.NewEventType()
esEVT_NEW_SIM = wx.NewEventType()
esEVT_OPEN_SIM = wx.NewEventType()
esEVT_SAVEAS_SIM = wx.NewEventType()
esEVT_RUN_SIM = wx.NewEventType()
esEVT_RESET_SIM = wx.NewEventType()
esEVT_CLOSE_SIM = wx.NewEventType()

esEVT_UPDATE_MAP = wx.NewEventType()
esEVT_UPDATE_MODEL = wx.NewEventType()

esEVT_LOAD_MOD = wx.NewEventType()

# Event binder;
EVT_COMMON_EVENT = wx.PyEventBinder(esEVT_COMMON_EVENT, 1)
EVT_NEW_SIM = wx.PyEventBinder(esEVT_NEW_SIM, 1)
EVT_OPEN_SIM = wx.PyEventBinder(esEVT_OPEN_SIM, 1)
EVT_SAVEAS_SIM = wx.PyEventBinder(esEVT_SAVEAS_SIM, 1)
EVT_RUN_SIM = wx.PyEventBinder(esEVT_RUN_SIM, 1)
EVT_RESET_SIM = wx.PyEventBinder(esEVT_RESET_SIM, 1)
EVT_CLOSE_SIM = wx.PyEventBinder(esEVT_CLOSE_SIM, 1)

EVT_UPDATE_MAP =wx.PyEventBinder(esEVT_UPDATE_MAP, 1)
EVT_UPDATE_MODEL =wx.PyEventBinder(esEVT_UPDATE_MODEL, 1)
EVT_LOAD_MOD = wx.PyEventBinder(esEVT_LOAD_MOD, 1)

def sendEvent(etype,args=None,target=None):
    ''' Para target: None for wxmw main window;'''
    evt =EvrSimEvent(etype,-1)
    evt.SetEventArgs(args)
    if target is None:
        wxmw=wx.Window.FindWindowByName('wxmw')
        for plc in wxmw.Children:
            plc.GetEventHandler().ProcessEvent(evt)
        wxmw.GetEventHandler().ProcessEvent(evt)
    else:
        target.GetEventHandler().ProcessEvent(evt)
    return
