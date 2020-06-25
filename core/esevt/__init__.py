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

# Create event type and binder;
esEVT_NEW_SIM = wx.NewEventType()
esEVT_OPEN_SIM = wx.NewEventType()
esEVT_RUN_SIM = wx.NewEventType()
esEVT_UPDATE_MAP = wx.NewEventType()
esEVT_LOAD_MOD = wx.NewEventType()
EVT_NEW_SIM = wx.PyEventBinder(esEVT_NEW_SIM, 1)
EVT_OPEN_SIM = wx.PyEventBinder(esEVT_OPEN_SIM, 1)
EVT_RUN_SIM = wx.PyEventBinder(esEVT_RUN_SIM, 1)
EVT_UPDATE_MAP = wx.PyEventBinder(esEVT_UPDATE_MAP, 1)
EVT_LOAD_MOD = wx.PyEventBinder(esEVT_LOAD_MOD, 1)
