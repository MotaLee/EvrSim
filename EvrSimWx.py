# -*- coding: UTF-8 -*-
# system libs;
import sys
import os
import re
import subprocess
# Outer libs;
import wx
# Builtin libs
from core import esui
from core import esevt
from core import esgl
from core import ESC
# system vars;
wxapp = wx.App()
cx,cy,cw,ch=wx.ClientDisplayRect()
xu=cw/100
yu=ch/100
esui.gmv.XU=xu
esui.gmv.YU=yu
# Wx frame main window;
class ESW(wx.Frame):
    WIN_TITLE='EvrSimWx'
    WIN_VER='0.0.2'

    def __init__(self):
        wx.Frame.__init__(self,None,
            pos=(cx,cy),
            size=(cw,ch),
            style=wx.NO_BORDER | wx.ICON_HAND,
            title=self.WIN_TITLE)
        self.SetBackgroundColour('#333333')
        self.dlgw=None
        self.gl_timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onRunSimTimer,self.gl_timer)
        self.Bind(esevt.EVT_NEW_SIM, self.onNewSim)
        self.Bind(esevt.EVT_OPEN_SIM, self.onOpenSim)
        self.Bind(esevt.EVT_RUN_SIM, self.onRunSim)
        self.Bind(esevt.EVT_LOAD_MOD, self.onLoadMod)
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
        # modpl.Hide()
        # compl.SetSize(int(75*xu),int(25*yu))
        return

    def estCom(self,e,procom=''):
        # res=''
        # tres=''
        # if procom=='':
        #     com=comtxt.GetValue()
        #     modpl.Hide()
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
        modpl.loadMod()
        return

    def onNewSim(self,e):
        'Create sim and open;'
        global dlgw
        if ESC.SIM_NAME=='':
            # self.sendEvent(esevt.saveSimEvent)
            # self.sendEvent(esevt.closeSimEvent)
            return
        sim_name=e.GetEventArgs()
        dlgw.EndModal(1)
        dlgw.Destroy()
        ESC.newSim(sim_name)
        self.sendEvent(esevt.openSimEvent,sim_name)
        return

    def onOpenSim(self,e):
        if ESC.SIM_NAME!='':return
        sim_name=e.GetEventArgs()
        self.dlgw.EndModal(1)
        self.dlgw.Destroy()

        ESC.openSim(sim_name)
        welpl.Hide()
        modpl.loadMod()
        acppl.Hide()
        aropl.Show()
        aropl.readMap()

        maps=list(ESC.ARO_MAP_LIST)
        models=list(ESC.ACP_MAP.keys())
        sidepl.loadMM(maps,models)
        sidepl.updateAroList()
        aropl.map_name=maps[0]
        acppl.acpmodel=models[0]
        acppl.drawAcp()
        return

    def onRunSim(self,e):
        if self.gl_timer.IsRunning():
            self.gl_timer.Stop()
        else:
            aropl.time_step=ESC.TIME_STEP
            self.gl_timer.Start(int(ESC.TIME_STEP*1000))
        return

    def onRunSimTimer(self,e):
        ESC.runSim()
        aropl.readMap()
        return

    def sendEvent(self,ecode,args=None,target=None):
        evt =esevt.EvrSimEvent(ecode,-1)
        evt.SetEventArgs(args)
        if target is None: target=self
        target.GetEventHandler().ProcessEvent(evt)
        return
    pass
wxmw=ESW()

# Command panel;
compl=esui.ComPlc(wxmw,(0,0),(cw,4*yu))
# Module panel;
modpl=esui.ModPlc(wxmw,(0,4*yu),(75*xu,21*yu))
# Aro Opengl container;
aropl=esgl.Glc(wxmw,(0,25*yu),(75*xu,75*yu))
# Acp panel;
acppl=esui.AcpPlc(wxmw,(0,25*yu),(75*xu,75*yu))
# Side panel;
sidepl=esui.SidePlc(wxmw,(75*xu,4*yu),(25*xu,96*yu))

# Welcome panel;
welpl=esui.Plc(wxmw,(0,25*yu),(75*xu,75*yu),'welpl')
welttc=esui.Ttc(welpl,(0,15*yu),(75*xu,10*yu),'E  v  r  S  i  m',tsize=int(4*yu))
verttc=esui.Ttc(welpl,(0,25*yu),(75*xu,4*yu),wxmw.WIN_VER,tsize=int(2*yu))

# Main enterance;
wxmw.Show()
wxapp.MainLoop()
