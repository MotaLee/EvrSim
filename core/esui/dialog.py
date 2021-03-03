# Parent lib;
import sys
import os
import wx
from core import ESC,esui,esevt
xu=esui.XU
yu=esui.YU
# Dialog wx sub class;
class EsDialog(wx.Dialog):
    def __init__(self,parent,p,s,logtitle):
        super().__init__(parent,pos=p,size=s,title=logtitle,style=wx.NO_BORDER)
        self.SetBackgroundColour(esui.COLOR_LBACK)
        self.conbtn=esui.Btn(self,(self.Size[0]-10*yu,self.Size[1]-5*yu),(4*yu,4*yu),'√')
        self.canbtn=esui.Btn(self,(self.Size[0]-5*yu,self.Size[1]-5*yu),(4*yu,4*yu),'×')
        self.dlgttl=esui.StaticText(self,(yu,0),(12*yu,4*yu),logtitle,align='left')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.canbtn.Bind(wx.EVT_LEFT_UP,self.onCancel)
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
        esevt.sendEvent(esevt.ETYPE_COMEVT,[esevt.ETYPE_OPEN_SIM,sim_name])
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
            esevt.sendEvent(esevt.ETYPE_COMEVT,[esevt.ETYPE_OPEN_SIM,sim_name])
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
                esui.SltBtn(SP,(24*yu,i*5*yu+yu),(3*yu,3*yu),'√',select=v_esc,tip=value)
            elif type(v_esc)==int or type(v_esc)==float:
                esui.InputText(SP,(24*yu,i*5*yu+yu),(8*yu,4*yu),hint=str(v_esc),tip=value)
            i+=1
        # self.SIM_QUEUE_LEN=1
        # self.ACP_DEPTH=20
        # self.len_timestep=1/30     # Unit second, fps=30Hz;
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
    def __init__(self,parent,p,s):
        esui.EsDialog.__init__(self,parent,p,s,'Mod Manager')
        self.lvbtn=esui.Btn(self,(yu,55*yu),(4*yu,4*yu),'Ls',able=False)
        self.tibtn=esui.Btn(self,(6*yu,55*yu),(4*yu,4*yu),'Tr')
        self.plc_mod=esui.Plc(self,(yu,4*yu),(self.Size.x-2*yu,self.Size.y-10*yu),
            border={'all':esui.COLOR_ACTIVE})
        self.loadMod()
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        clist=self.plc_mod.Children
        newlist=list()
        for ctrl in clist:
            if ctrl.GetValue():
                newlist.append(ctrl.GetLabel())
        ESC.loadMod(newlist,unload=True)
        esevt.sendEvent(esevt.ETYPE_COMEVT,esevt.ETYPE_LOAD_MOD)
        self.EndModal(1)
        return

    def loadMod(self):
        fl=os.listdir('mod/')
        bw=self.plc_mod.Size.x/6
        bh=self.plc_mod.Size.y/3
        for i in range(0,len(fl)):
            if fl[i][0]=='_':continue
            bx=(i %6)*bw+bw//3
            by=(i//6)*bh+bh//3
            esui.SltBtn(self.plc_mod,(bx,by),(bw//1.5,bh//1.5),fl[i],
                select=fl[i] in ESC.MOD_TREE_DICT)
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
            esui.SltBtn(self,(bx,by),(bw//1.5,bh//1.5),slist[i],exclusive=True)

        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(esui.COLOR_BACK))
        dc.SetPen(wx.Pen(esui.COLOR_ACTIVE))
        dc.DrawRectangle((0,0),self.Size)
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
            self.nametcc.SetValue(ESC.MAP_ACTIVE)
        return

    def onConfirm(self,e):
        from core import estl
        map_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/'+ESC.SIM_NAME+'/map/')
        for f in file_list:
            if f[0:f.rfind('.')]==map_name:
                self.warnstc.Show()
                return
        if self.operation=='New':
            ESC.newMapFile(map_name)
            esui.IDX.SIDE_DIV.loadMaps()
            esui.toggleWorkspace(target='ARO')
        elif self.operation=='Rename':
            ESC.renameMapFile(newname=map_name)
            esui.IDX.SIDE_DIV.loadMaps()
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
            self.nametcc.SetValue(esui.IDX.MDL_DIV.model_tuple[1])
        return

    def onConfirm(self,e):
        from core import estl
        model_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/'+ESC.SIM_NAME+'/model/')
        for f in file_list:
            if f[0:f.rfind('.')]==model_name:
                self.warnstc.Show()
                return
        if self.operation=='New':
            ESC.newModelFile(model_name)
            esui.IDX.SIDE_DIV.loadModels()
            esui.toggleWorkspace(target='ACP')
            esui.IDX.MDL_DIV.drawMdl((ESC.SIM_NAME,model_name))
        elif self.operation=='Rename':
            ESC.renameModelFile(mdlname=esui.IDX.MDL_DIV.model_tuple[1],newname=model_name)
            esui.IDX.SIDE_DIV.loadModels()
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
