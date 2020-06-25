# Parent lib;
import wx
from core import ESC
from core import esui
gmv=esui.gmv

# List box wx sub class;
class ListBox(wx.Panel):
    def __init__(self,parent,p,s):
        wx.Panel.__init__(self,parent,
            pos=(int(p[0]),int(p[1])),
            size=(int(s[0]),int(s[1])),
            style=wx.NO_BORDER)
        self.items=list()
        self.ipos=0
        self.spos=-1
        self.SetBackgroundColour(gmv.COLOR_Back)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_MOTION,self.onMove)
        self.Bind(wx.EVT_LEFT_DOWN,self.onClk)
        return

    def updateList(self,itemlist):
        self.items=itemlist
        self.Refresh()
        return

    def onPaint(self,e):
        dc=wx.BufferedPaintDC(self)
        yu=gmv.YU
        dc.SetBrush(wx.Brush(gmv.COLOR_Back))
        dc.SetPen(wx.Pen(gmv.COLOR_Back))
        dc.DrawRectangle(0,0,self.Size[0],self.Size[1])

        dc.SetPen(wx.Pen(gmv.COLOR_Front))
        dc.DrawLine(0,1,self.Size[0],1)
        dc.DrawLine(0,self.Size[1]-1,self.Size[0],self.Size[1]-1)

        txtfont=wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL,False,'微软雅黑')
        dc.SetFont(txtfont)
        dc.SetTextForeground(gmv.COLOR_Text)
        for i in range(0,len(self.items)):
            aroname=ESC.getAro(self.items[i]).AroName
            dc.DrawText(aroname,4*yu+1,i*4*yu+1)

        ip=self.ipos+1
        if self.ipos<len(self.items):
            aroname=ESC.getAro(self.items[self.ipos]).AroName
            ts=dc.GetTextExtent(aroname)
            dc.DrawLine(4*yu,ip*4*yu-yu,4*yu+ts[0],ip*4*yu-yu)
        if self.spos!=-1:
            dc.SetBrush(wx.Brush(gmv.COLOR_Front))
            dc.DrawRectangle(yu,self.spos*4*yu+yu,2*yu,2*yu)
        return

    def onMove(self,e):
        self.ipos=int(e.GetPosition()[1]/(4*gmv.YU))
        if self.ipos<len(self.items):
            self.Refresh(eraseBackground=False)
        e.Skip()
        return

    def onClk(self,e):
        if self.spos==self.ipos:self.spos=-1
        else:self.spos=self.ipos
        self.Refresh(eraseBackground=False)
        e.Skip()
    pass
