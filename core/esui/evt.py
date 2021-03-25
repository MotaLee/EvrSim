import wx
# Event type;
ETYPE_COMEVT=wx.NewEventType()
ETYPE_NEW_SIM=wx.NewEventType()
ETYPE_OPEN_SIM=wx.NewEventType()
ETYPE_SAVEAS_SIM=wx.NewEventType()
ETYPE_RUN_SIM=wx.NewEventType()
ETYPE_STOP_SIM=wx.NewEventType()
ETYPE_RESET_SIM=wx.NewEventType()
ETYPE_CLOSE_SIM=wx.NewEventType()
ETYPE_STEP_SIM=wx.NewEventType()
ETYPE_SET_SIM=wx.NewEventType()

ETYPE_UPDATE_MAP=wx.NewEventType()
ETYPE_UPDATE_MODEL=wx.NewEventType()

ETYPE_LOAD_MOD=wx.NewEventType()

ETYPE_KEY_DOWN=wx.NewEventType()

ETYPE_OPEN_CMD=wx.NewEventType()
ETYPE_CLOSE_CMD=wx.NewEventType()

ETYPE_CLOSE_ES=wx.NewEventType()

# Event binder;
EBIND_COMEVT=wx.PyEventBinder(ETYPE_COMEVT, 1)
# EBIND_NEW_SIM=wx.PyEventBinder(ETYPE_NEW_SIM, 1)
# EBIND_OPEN_SIM=wx.PyEventBinder(ETYPE_OPEN_SIM, 1)
# EVT_SAVEAS_SIM=wx.PyEventBinder(ETYPE_SAVEAS_SIM, 1)
EBIND_RUN_SIM=wx.PyEventBinder(ETYPE_RUN_SIM, 1)
EBIND_RESET_SIM=wx.PyEventBinder(ETYPE_RESET_SIM, 1)
# EVT_CLOSE_SIM=wx.PyEventBinder(ETYPE_CLOSE_SIM, 1)

EBIND_UPDATE_MAP=wx.PyEventBinder(ETYPE_UPDATE_MAP, 1)
# EVT_UPDATE_MODEL=wx.PyEventBinder(ETYPE_UPDATE_MODEL, 1)
# EVT_LOAD_MOD=wx.PyEventBinder(ETYPE_LOAD_MOD, 1)
EBIND_STEP_SIM=wx.PyEventBinder(ETYPE_STEP_SIM, 1)
# EVT_KEY_DOWN=wx.PyEventBinder(ETYPE_KEY_DOWN, 1)
EBIND_LEFT_CLK=wx.EVT_LEFT_DOWN
EBIND_LEFT_DCLK=wx.EVT_LEFT_DCLICK
# EvrSim Custom event;

class ESEvent(wx.PyCommandEvent):
    def __init__(self,etype,argkw=None):
        super().__init__(etype,-1)
        self.evt_argkw=dict()
        if argkw:
            self.setEventArgs(**argkw)
        return

    def getEventArgs(self,key='subtype'):
        return self.evt_argkw[key]

    def setEventArgs(self,**argkw):
        self.evt_argkw=argkw
        return
    pass

def sendEvent(etype,target:wx.Window=None,**argkw):
    ''' Send event to target window.
        * Para target: None default for wxmw main window;
        * Para argkw: Parameter saved into event;'''
    from core import esui
    evt =ESEvent(etype,argkw)
    if target is None:
        esui.UMR.ESMW.GetEventHandler().ProcessEvent(evt)
        for div in esui.UMR.ESMW.Children:
            div.GetEventHandler().ProcessEvent(evt)
    else:target.ProcessEvent(evt)
    return

def sendComEvt(subtype,target:wx.Window=None,**argkw):
    ''' Send common event.'''
    argkw['subtype']=subtype
    sendEvent(ETYPE_COMEVT,target,**argkw)
    return
