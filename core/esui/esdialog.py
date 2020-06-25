# Parent lib;
import os
import wx
from core import esui
from core import esevt
gmv=esui.gmv

# Dialog wx sub class;
class EsDialog(wx.Dialog):
    def __init__(self,parent,p,s,logtitle,exstl=0):
        wx.Dialog.__init__(self,parent,-1,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            title=logtitle,
            style=wx.NO_BORDER | exstl)
        self.SetBackgroundColour('#333333')
        xu=s[0]/60
        yu=s[1]/60
        self.conbtn=esui.btn(self,(60*xu-9*yu,55*yu),(4*yu,4*yu),'V')
        self.canbtn=esui.btn(self,(60*xu-5*yu,55*yu),(4*yu,4*yu),'X')
        self.dlgttl=esui.Stc(self,(yu,0),(10*xu,4*yu),logtitle,align='left')

        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.canbtn.Bind(wx.EVT_LEFT_DOWN,self.onCancel)
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#333333'))
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        return

    def onCancel(self,e):
        self.EndModal(1)
        self.Destroy()
        return
    pass

# New Dialog wx sub class;
class NewDialog(EsDialog):
    def __init__(self,parent,pos,siz,txt,exstl=0):
        esui.EsDialog.__init__(self,parent,
            (pos[0],pos[1]),(siz[0],siz[1]),
            txt,exstl)
        xu=siz[0]/60
        yu=siz[1]/60
        self.dlgttl.SetLabel('New')
        self.smstc=esui.Stc(self,(yu,4*yu,),(12*yu,4*yu),'Sim Name:',align='left')
        self.nametcc=esui.Tcc(self,(12*yu,4*yu),(60*xu-14*yu,4*yu),tsize=1.5*yu)
        self.warnstc=esui.Stc(self,(12*yu,8*yu),(20*xu,4*yu),'Sim existed.',align='left')
        self.conbtn.Bind(wx.EVT_LEFT_DOWN,self.onConfirm)
        self.nametcc.Bind(wx.EVT_LEFT_DOWN,self.onNameTcc)
        self.warnstc.Hide()
        return

    def onConfirm(self,e):
        sim_name=self.nametcc.GetValue()
        file_list=os.listdir('sim/')
        for f in file_list:
            if sim_name==f:
                self.warnstc.Show()
                return
        self.Parent.sendEvent(esevt.esEVT_NEW_SIM,sim_name)
        return
    def onNameTcc(self,e):
        self.warnstc.Hide()
        e.Skip()
        return
    pass

# Open Dialog wx sub class;
class OpenDialog(EsDialog):
    def __init__(self,parent,p,s,loglabel,exstl=0):
        esui.EsDialog.__init__(self,parent,
            (p[0],p[1]),
            (s[0],s[1]),
            loglabel,exstl)
        xu=s[0]/60
        yu=s[1]/60
        # List view and tree view;
        self.lvbtn=esui.btn(self,(yu,55*yu),(4*yu,4*yu),'Lv',able=False)
        self.tibtn=esui.btn(self,(5*yu,55*yu),(4*yu,4*yu),'Tv')
        self.dlgttl.SetLabel(loglabel)
        self.vspl=ViewSimPanel(self,(1*yu,4*yu),(60*xu-2*yu,50*yu))
        self.vspl.loadSim()

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
            self.Parent.sendEvent(esevt.esEVT_OPEN_SIM,sim_name)
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
        self.lvbtn=esui.btn(self,(yu,55*yu),(4*yu,4*yu),'Lv',able=False)
        self.tibtn=esui.btn(self,(5*yu,55*yu),(4*yu,4*yu),'Tv')
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
        self.Parent.sendEvent(esevt.esEVT_LOAD_MOD,newlist)
        return
    pass


# View sim panel sub class;
class ViewSimPanel(wx.Panel):
    def __init__(self,parent,pos,siz,exstl=0):
        wx.Panel.__init__(self,parent,-1,
            pos=(int(pos[0]),int(pos[1])),
            size=(int(siz[0]),int(siz[1])),
            style=wx.NO_BORDER | exstl)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        return

    def loadSim(self):
        self.DestroyChildren()
        slist=os.listdir('sim/')
        nlist=[]
        for s in slist:
            if s[0]!='_':nlist.append(s)
        if len(nlist)==0: return

        bw=self.Size[0]//6
        bh=self.Size[1]//3
        for i in range(0,len(nlist)):
            bx=(i %6)*bw+bw//3
            by=(i//6)*bh+bh//3
            esui.SelectBtn(self,(bx,by),(bw//1.5,bh//1.5),nlist[i])
        return

    def onPaint(self,e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,0,self.Size[0],0)
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return
    pass

# View mod panel sub class;
class ViewModPanel(wx.Panel):
    def __init__(self,parent,p,s,nowlist,exstl=0):
        wx.Panel.__init__(self,parent,-1,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
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
        dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])
        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,0,self.Size[0],0)
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)
        return
    pass
