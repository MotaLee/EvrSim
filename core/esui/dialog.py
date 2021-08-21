# Parent lib;
import sys
import os
import wx
from core import ESC,esui
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
        self.nametcc=esui.InputText(self,tsize=1.5*yu,
            style={'p':(12*yu,4*yu),'s':(60*xu-14*yu,4*yu)})
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Sim existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        return

    def onConfirm(self,e):
        sim_name=self.nametcc.getValue()
        file_list=os.listdir('sim/')
        for f in file_list:
            if sim_name==f:
                self.warnstc.Show()
                return
        ESC.newSim(sim_name)
        esui.sendComEvt(esui.ETYPE_OPEN_SIM,None,simname=sim_name)
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
        self.div_sims=ViewSimDiv(self,style={'p':(1*yu,4*yu),'s':(60*xu-2*yu,50*yu)})

        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        sim_name=''
        for ctrl in self.div_sims.getChildren():
            if ctrl.GetValue():
                sim_name=ctrl.GetLabel()
                break
        if sim_name!='':
            ESC.openSim(sim_name)
            esui.sendComEvt(esui.ETYPE_OPEN_SIM)
            esui.sendComEvt(esui.ETYPE_LOAD_MOD)
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
        self.nametcc=esui.InputText(self,tsize=1.5*yu,
            style={'p':(12*yu,4*yu),'s':(60*xu-14*yu,4*yu)})
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
        self.div_setting=esui.ScrollDiv(self,style={'p':(yu,4*yu),
            's':(self.Size[0]-2*yu,self.Size[1]-10*yu)})

        i=0
        SP=self.div_setting
        for desc,value in ESC.SETTING_DICT.items():
            # last_ctrl=
            esui.StaticText(SP,(yu,i*5*yu+yu),(24*yu,4*yu),desc+':',align='left')
            v_esc=ESC.__dict__[value]
            if type(v_esc)==bool:
                esui.SltBtn(SP,(24*yu,i*5*yu+yu),(3*yu,3*yu),'√',select=v_esc,tip=value)
            elif type(v_esc)==int or type(v_esc)==float:
                esui.InputText(SP,hint=str(v_esc),tip=value,
                    style={'p':(24*yu,i*5*yu+yu),'s':(8*yu,4*yu)})
            i+=1
        # self.SIM_QUEUE_LEN=1
        # self.ACP_DEPTH=20
        # self.fps=1/30     # Unit second, fps=30Hz;
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        setting_dict=dict()
        for ctrl in self.div_setting.Children:
            if type(ctrl)!=esui.StaticText:
                pass
        esui.sendEvent(esui.ETYPE_SET_SIM,None,**setting_dict)
        return
    pass

# Mod Dialog wx sub class;
class ModDialog(EsDialog):
    def __init__(self,parent,p,s):
        esui.EsDialog.__init__(self,parent,p,s,'Mod Manager')
        self.lvbtn=esui.Btn(self,(yu,55*yu),(4*yu,4*yu),'Ls',able=False)
        self.tibtn=esui.Btn(self,(6*yu,55*yu),(4*yu,4*yu),'Tr')
        self.div_mod=esui.Div(self,style={
            'border':esui.COLOR_HOVER,
            'p':(yu,4*yu),
            's':(self.Size.x-2*yu,self.Size.y-10*yu)})
        self.loadMod()
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        return

    def onConfirm(self,e):
        newlist=list()
        for ctrl in self.div_mod.getChildren():
            if ctrl.GetValue():
                newlist.append(ctrl.GetLabel())
        ESC.loadMod(newlist,unload=True)
        esui.sendComEvt(esui.ETYPE_LOAD_MOD)
        self.EndModal(1)
        return

    def loadMod(self):
        fl=os.listdir('mod/')
        bw=self.div_mod.Size.x/6
        bh=self.div_mod.Size.y/3
        for i in range(0,len(fl)):
            if fl[i][0]=='_':continue
            bx=(i %6)*bw+bw//3
            by=(i//6)*bh+bh//3
            esui.SltBtn(self.div_mod,(bx,by),(bw//1.5,bh//1.5),fl[i],
                select=fl[i] in ESC.MOD_TREE_DICT)
        return
    pass

# View sim panel sub class;
class ViewSimDiv(esui.Div):
    def __init__(self,parent,**argkw):
        super().__init__(parent,**argkw)
        self.updateStyle(style={'border':esui.COLOR_HOVER})
        slist=os.listdir('sim/')
        bw=self.Size[0]//6
        bh=self.Size[1]//3
        for i in range(0,len(slist)):
            if slist[i].find('_')!=-1:continue
            bx=(i %6)*bw+bw//3
            by=(i//6)*bh+bh//3
            esui.SltBtn(self,(bx,by),(bw//1.5,bh//1.5),slist[i],exclusive=True)
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
        self.nametcc=esui.InputText(self,tsize=1.5*yu,
            style={'p':(12*yu,4*yu),'s':(self.Size[0]-13*yu,4*yu)})
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
            esui.UMR.SIDE_DIV.loadMaps()
            esui.toggleWorkspace(target='ARO')
        elif self.operation=='Rename':
            ESC.renameMapFile(newname=map_name)
            esui.UMR.SIDE_DIV.loadMaps()
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
        self.nametcc=esui.InputText(self,tsize=1.5*yu,
            style={'p':(12*yu,4*yu),'s':(self.Size[0]-13*yu,4*yu)})
        self.warnstc=esui.StaticText(self,(12*yu,8*yu),(20*xu,4*yu),'Name existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onClkNameTcc)
        self.warnstc.Hide()
        if operation!='New':
            self.nametcc.SetValue(esui.UMR.MDL_DIV.model_tuple[1])
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
            esui.UMR.SIDE_DIV.loadModels()
            esui.toggleWorkspace(target='ACP')
            esui.UMR.MDL_DIV.drawMdl((ESC.SIM_NAME,model_name))
        elif self.operation=='Rename':
            ESC.renameModelFile(mdlname=esui.UMR.MDL_DIV.model_tuple[1],newname=model_name)
            esui.UMR.SIDE_DIV.loadModels()
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
