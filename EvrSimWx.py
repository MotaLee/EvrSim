# -*- coding: UTF-8 -*-
# system libs;
import sys
import threading
import wx
# Builtin libs
from EvrSim import ES_WX_TITLE,ES_VER
from core import ESC
from core import esui
wxapp = wx.App()
cx,cy,cw,ch=wx.ClientDisplayRect()
xu=cw/100
yu=ch/100
esui.XU=xu
esui.YU=yu
from core import esevt
from core import esgl
import mod
# Core thread class;
class ESCThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        return

    def run(self):
        ESC.runSim()
        return

    pass

# Wx frame main window;
class ESW(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None,pos=(cx,cy),size=(cw,ch),name='wxmw',
            style=wx.NO_BORDER | wx.ICON_HAND,title=ES_WX_TITLE)
        self.SetBackgroundColour(esui.COLOR_LBACK)

        self.dlgw=None
        self.esc_thread=ESCThread()
        self.gl_timer=wx.Timer(self)

        self.Bind(wx.EVT_TIMER,self.onRunSimTimer,self.gl_timer)
        self.Bind(esevt.EVT_NEW_SIM, self.onNewSim)
        self.Bind(esevt.EVT_OPEN_SIM, self.onOpenSim)
        self.Bind(esevt.EVT_SAVEAS_SIM, self.onSaveAsSim)
        self.Bind(esevt.EVT_RUN_SIM, self.onRunSim)
        self.Bind(esevt.EVT_CLOSE_SIM, self.onCloseSim)
        self.Bind(esevt.EVT_LOAD_MOD, self.onLoadMod)

        esui.WXMW=self
        esui.HEAD_PLC=esui.HeadPlc(self,(0,0),(cw,4*yu))
        esui.MOD_PLC=esui.ModPlc(self,(0,4*yu),(75*xu,21*yu))
        esui.COM_PLC=esui.ComPlc(self,(0,4*yu),(75*xu,21*yu))
        esui.ARO_PLC=esgl.AroGlc(self,(0,25*yu),(75*xu,75*yu))
        esui.ACP_PLC=esui.AcpPlc(self,(0,25*yu),(75*xu,75*yu))
        esui.SIDE_PLC=esui.SidePlc(self,(75*xu,4*yu),(25*xu,96*yu))
        esui.WEL_PLC=esui.Plc(self,(0,25*yu),(75*xu,75*yu),'esui.WEL_PLC')

        welttc=esui.Ttc(esui.WEL_PLC,(0,15*yu),(75*xu,10*yu),'E  v  r  S  i  m',tsize=int(4*yu))
        verttc=esui.Ttc(esui.WEL_PLC,(0,25*yu),(75*xu,4*yu),ES_VER,tsize=int(2*yu))
        return

    def esWxCom(self,e):
        'Execute command in Wx;'
        # com=comtxt.GetValue()
        # exec(com)
        # tres=''
        # res=sys.stdout.readline()
        # while res!='\n':
        #     tres=tres+res
        #     res=est.stdout.readline()
        # histxt.SetValue(tres)
        # esui.MOD_PLC.Hide()
        # compl.SetSize(int(75*xu),int(25*yu))
        return

    def estCom(self,e,procom=''):
        # res=''
        # tres=''
        # if procom=='':
        #     com=comtxt.GetValue()
        #     esui.MOD_PLC.Hide()
        #     compl.SetSize(int(75*xu),int(25*yu))
        # else:
        #     com=procom
        # comtxt.SetValue('')
        # if com=='clear()':
        #     histxt.SetValue('')   # Console extension;
        # else:
        #     # Main communication;
        #     est.stdin.write(com+'\n')
        #     est.stdin.flush()
        #     while res!='EOF\n':
        #         tres=tres+res
        #         res=est.stdout.readline()
        #     if procom=='':
        #         histxt.AppendText(self.COM_HEAD+com+'\n'+tres)
        #     else: return tres
        # comtxt.SetInsertionPointEnd()
        # sys.stderr=sys.stdout
        # sys.stdout=histxt
        # histxt.write(est.stdout.readline())
        return

    def onLoadMod(self,e):
        global dlgw
        dlgw.EndModal(1)
        dlgw.Destroy()
        ESC.loadMod(e.GetEventArgs())
        esui.MOD_PLC.loadMod()
        return

    def onNewSim(self,e):
        'Create sim and open;'
        if ESC.SIM_NAME!='':
            'todo: new sim after already opened another sim;'
            # self.sendEvent(esevt.saveSimEvent)
            # self.sendEvent(esevt.closeSimEvent)
            return
        sim_name=e.GetEventArgs()
        self.dlgw.EndModal(1)
        self.dlgw.Destroy()
        ESC.newSim(sim_name)
        esevt.sendEvent(esevt.openSimEvent,sim_name)
        return

    def onOpenSim(self,e):
        if ESC.SIM_NAME!='':
            'todo: open sim after already opened another sim;'
            return
        sim_name=e.GetEventArgs()
        self.dlgw.EndModal(1)
        self.dlgw.Destroy()

        ESC.openSim(sim_name)

        esui.WEL_PLC.Hide()
        esevt.sendEvent(esevt.esEVT_COMMON_EVENT,esevt.esEVT_LOAD_MOD)

        maps=list(ESC.ARO_MAP_LIST)
        models=list(ESC.ACP_MAP.keys())
        esui.SIDE_PLC.loadMaps(maps)
        esui.SIDE_PLC.loadModels(models)
        esui.SIDE_PLC.aro_btn.SetValue(True)
        esui.SIDE_PLC.Show()

        esui.ARO_PLC.Show()
        # esui.ARO_PLC.map_name=maps[0]

        esui.ACP_PLC.Hide()
        return

    def onSaveAsSim(self,e):
        new_sim_name=e.GetEventArgs()
        self.dlgw.EndModal(1)
        self.dlgw.Destroy()
        ESC.newSim(new_sim_name,src=ESC.SIM_NAME)
        return

    def onRunSim(self,e):
        if self.gl_timer.IsRunning():
            self.gl_timer.Stop()
        else:
            if ESC.CORE_STAUS=='STOP':ESC.CORE_STAUS='READY'
            self.gl_timer.Start(int(1000/esgl.FPS))
        return

    def onRunSimTimer(self,e):
        if ESC.CORE_STAUS=='STOP':
            self.gl_timer.Stop()
        elif ESC.CORE_STAUS=='BUSY':
            return
        elif ESC.CORE_STAUS=='READY':
            esui.ARO_PLC.readMap()
            # if len(esui.ARO_PLC.aro_selection)==1 and esui.SIDE_PLC.now_tab=='Arove':
            #     esui.SIDE_PLC.showArove()
            if not self.esc_thread.is_alive():
                self.esc_thread=ESCThread()
                self.esc_thread.start()
        return

    def onCloseSim(self,e):
        'todo: close opened sim;'
        return
    pass
wxmw=ESW()

# Main enterance;
wxmw.Show()
wxapp.MainLoop()
