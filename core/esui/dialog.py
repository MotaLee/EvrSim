# Parent lib;
import sys
import os
import wx
from core import ESC
from core import esui
from core import esevt

# Dialog wx sub class;
class EsDialog(wx.Dialog):
    def __init__(self,parent,p,s,logtitle):
        wx.Dialog.__init__(self,parent,-1,
            pos=p,
            size=s,
            title=logtitle,
            style=wx.NO_BORDER)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        yu=esui.YU
        self.conbtn=esui.Btn(self,(self.Size[0]-10*yu,self.Size[1]-5*yu),(4*yu,4*yu),'√')
        self.canbtn=esui.Btn(self,(self.Size[0]-5*yu,self.Size[1]-5*yu),(4*yu,4*yu),'×')
        self.dlgttl=esui.StaticText(self,(yu,0),(12*yu,4*yu),logtitle,align='left')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.canbtn.Bind(wx.EVT_LEFT_DOWN,self.onCancel)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_LBACK))
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawRectangle((0,0),self.Size)
        return

    def onCancel(self,e):
        self.EndModal(1)
        self.Destroy()
        return
    pass

# New Dialog wx sub class;
class NewDialog(EsDialog):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'New')
        xu=esui.XU
        yu=esui.YU
        self.dlgttl.SetLabel('New')
        self.smstc=esui.StaticText(self,(yu,4*yu,),(12*yu,4*yu),'Sim Name:',align='left')
        self.nametcc=esui.InputText(self,(12*yu,4*yu),(60*xu-14*yu,4*yu),tsize=1.5*yu)
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Sim existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        return

    def onConfirm(self,e):
        sim_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/')
        for f in file_list:
            if sim_name==f:
                self.warnstc.Show()
                return
        ESC.newSim(sim_name)
        esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,[esevt.ETYPE_OPEN_SIM,sim_name])
        self.EndModal(1)
        return

    def onClkNameTcc(self,e):
        self.warnstc.Hide()
        e.Skip()
        return
    pass

# Open Dialog wx sub class;
class OpenDialog(EsDialog):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'Open')
        xu=esui.XU
        yu=esui.YU
        self.dlgttl.SetLabel('Open')
        self.vspl=ViewSimPlc(self,(1*yu,4*yu),(60*xu-2*yu,50*yu))

        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        clist=self.vspl.Children
        sim_name=''
        for ctrl in clist:
            if ctrl.GetValue():
                sim_name=ctrl.GetLabel()
                break
        if sim_name!='':
            esevt.sendEvent(esevt.ETYPE_COMMON_EVENT,[esevt.ETYPE_OPEN_SIM,sim_name])
        self.EndModal(1)
        return
    pass

# New Dialog wx sub class;
class SaveAsDialog(EsDialog):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'Save as')
        xu=esui.XU
        yu=esui.YU
        self.dlgttl.SetLabel('Save as')
        self.smstc=esui.StaticText(self,(yu,4*yu,),(12*yu,4*yu),'Sim Name:',align='left')
        self.nametcc=esui.InputText(self,(12*yu,4*yu),(60*xu-14*yu,4*yu),tsize=1.5*yu)
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Sim existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        return

    def onConfirm(self,e):
        sim_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/')
        for f in file_list:
            if sim_name==f:
                self.warnstc.Show()
                return
        ESC.newSim(sim_name,src=ESC.SIM_NAME)
        return

    def onClkNameTcc(self,e):
        self.warnstc.Hide()
        e.Skip()
        return
    pass

class SettingDialog(EsDialog):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s,'Setting')
        yu=esui.YU
        self.dlgttl.SetLabel('Setting')
        self.setting_plc=esui.ScrolledPlc(self,(yu,4*yu),(self.Size[0]-2*yu,self.Size[1]-10*yu))

        i=0
        SP=self.setting_plc
        for desc,value in ESC.SETTING_DICT.items():
            # last_ctrl=
            esui.StaticText(SP,(yu,i*5*yu+yu),(24*yu,4*yu),desc+':',align='left')
            v_esc=ESC.__dict__[value]
            if type(v_esc)==bool:
                esui.SelectBtn(SP,(24*yu,i*5*yu+yu),(4*yu,4*yu),'V',select=v_esc,tip=value)
            elif type(v_esc)==int or type(v_esc)==float:
                esui.InputText(SP,(24*yu,i*5*yu+yu),(8*yu,4*yu),hint=str(v_esc),tip=value)
            i+=1
        # self.SIM_QUEUE_LEN=1
        # self.ACP_DEPTH=20
        # self.TIME_STEP=1/30     # Unit second, fps=30Hz;
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        setting_dict=dict()
        for ctrl in self.setting_plc.Children:
            if type(ctrl)!=esui.StaticText:
                pass
        esevt.sendEvent(esevt.ETYPE_SET_SIM,setting_dict)
        return
    pass

# Mod Dialog wx sub class;
class ModDialog(EsDialog):
    def __init__(self,parent,p,s,loglabel,exstl=0):
        esui.EsDialog.__init__(self,parent,
            (p[0],p[1]),
            (s[0],s[1]),
            loglabel,exstl)
        xu=s[0]/60
        yu=s[1]/60
        # List view and tree view;
        self.lvbtn=esui.Btn(self,(yu,55*yu),(4*yu,4*yu),'Lv',able=False)
        self.tibtn=esui.Btn(self,(5*yu,55*yu),(4*yu,4*yu),'Tv')
        self.dlgttl.SetLabel(loglabel)
        nowlist=list(self.Parent.WX_MOD_LIST)
        nowlist.remove('Self')
        self.vmpl=ViewModPanel(self,(1*yu,4*yu),(60*xu-2*yu,50*yu),nowlist)

        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        clist=self.vmpl.Children
        newlist=list()
        for ctrl in clist:
            if ctrl.GetValue():
                newlist.append(ctrl.GetLabel())
        esevt.sendEvent(esevt.ETYPE_LOAD_MOD,newlist)
        return
    pass

# View sim panel sub class;
class ViewSimPlc(esui.Plc):
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        slist=os.listdir('sim/')
        bw=self.Size[0]//6
        bh=self.Size[1]//3
        for i in range(0,len(slist)):
            if slist[i].find('_')!=-1:continue
            bx=(i %6)*bw+bw//3
            by=(i//6)*bh+bh//3
            esui.SelectBtn(self,(bx,by),(bw//1.5,bh//1.5),slist[i])

        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_SECOND))
        dc.DrawRectangle((0,0),self.Size)
        return
    pass

# View mod panel sub class;
class ViewModPanel(wx.Panel):
    def __init__(self,parent,p,s,nowlist,exstl=0):
        wx.Panel.__init__(self,parent,-1,
            pos=p,
            size=s,
            style=wx.NO_BORDER | exstl)
        self.now_list=nowlist
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.loadMod()
        return

    def loadMod(self):
        'Update MOD_SET via Mods Manager;'
        self.DestroyChildren()
        fl=os.listdir('mod/')
        nf=[]
        for f in fl:
            if f[0]!='_':
                nf.append(f[0:f.find('.')])
        bw=self.Size[0]//4
        bh=self.Size[1]//3
        for i in range(0,len(nf)):
            bx=(i %4)*bw+bw//6
            by=(i//4)*bh+bh//6
            esui.SelectBtn(self,(bx,by),(bw//1.5,bw//1.5),nf[i],
                select=nf[i] in self.now_list,
                enable=not nf[i] in self.now_list)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(esui.COLOR_FRONT))
        dc.DrawLine(0,0,self.Size[0],0)
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return
    pass

class MapDialog(EsDialog):
    def __init__(self,parent,p,s,operation):
        super().__init__(parent,p,s,operation+' Map')
        xu=esui.XU
        yu=esui.YU
        self.operation=operation
        self.dlgttl.SetLabel(operation+' Map:')
        self.smstc=esui.StaticText(self,(yu,4*yu,),(12*yu,4*yu),'Name:',align='left')
        self.nametcc=esui.InputText(self,(12*yu,4*yu),(self.Size[0]-13*yu,4*yu),tsize=1.5*yu)
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Name existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        if operation!='New':
            self.nametcc.SetValue(ESC.ARO_MAP_NAME)
        return

    def onConfirm(self,e):
        map_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/'+ESC.SIM_NAME+'/map/')
        for f in file_list:
            if f[0:f.rfind('.')]==map_name:
                self.warnstc.Show()
                return
        if self.operation=='New':
            ESC.newMapFile(map_name)
            esui.SIDE_PLC.loadMaps()
            esui.SIDE_PLC.onClkWorkspace(call='ARO_PLC')
        elif self.operation=='Rename':
            ESC.renameMapFile(newname=map_name)
            esui.SIDE_PLC.loadMaps()
        elif self.operation=='Saveas':
            pass
        self.EndModal(1)
        self.Destroy()
        return

    def onClkNameTcc(self,e):
        self.warnstc.Hide()
        e.Skip()
        return
    pass

class ModelDialog(EsDialog):
    def __init__(self,parent,p,s,operation):
        super().__init__(parent,p,s,operation+' Model')
        xu=esui.XU
        yu=esui.YU
        self.operation=operation
        self.dlgttl.SetLabel(operation+' Model:')
        self.smstc=esui.StaticText(self,(yu,4*yu,),(12*yu,4*yu),'Name:',align='left')
        self.nametcc=esui.InputText(self,(12*yu,4*yu),(self.Size[0]-13*yu,4*yu),tsize=1.5*yu)
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Name existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        if operation!='New':
            self.nametcc.SetValue(esui.ACP_PLC.model_tuple[1])
        return

    def onConfirm(self,e):
        model_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/'+ESC.SIM_NAME+'/model/')
        for f in file_list:
            if f[0:f.rfind('.')]==model_name:
                self.warnstc.Show()
                return
        if self.operation=='New':
            ESC.newModelFile(model_name)
            esui.SIDE_PLC.loadModels()
            esui.SIDE_PLC.onClkWorkspace(call='ACP_PLC')
            esui.ACP_PLC.drawAcp((ESC.SIM_NAME,model_name))
        elif self.operation=='Rename':
            ESC.renameModelFile(mdlname=esui.ACP_PLC.model_tuple[1],newname=model_name)
            esui.SIDE_PLC.loadModels()
        elif self.operation=='Saveas':
            pass
        self.EndModal(1)
        self.Destroy()
        return

    def onClkNameTcc(self,e):
        self.warnstc.Hide()
        e.Skip()
        return
    pass
