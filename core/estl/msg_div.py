import wx
from core import ESC,esui
yu=esui.YU
class MsgDiv(esui.IndePopupDiv):
    def __init__(self, parent, **argkw):
        super().__init__(parent, **argkw)
        self.timer=wx.Timer(self)
        self.txt_head=esui.DivText(self,
            label='ESC Info:',
            style={'p':(yu,yu),'s':(8*yu,4*yu)})
        self.txt_info=esui.InputText(self,tsize=yu,readonly=True,style={
                'p':(yu,6*yu),'s':(self.Size.x-2*yu,self.Size.y-7*yu)})
        self.btn_can=esui.DivBtn(self,label='×',style={
            'p':(self.Size.x-5*yu,yu),'s':(4*yu,4*yu)})
        self.updateStyle(style={'bgc':esui.COLOR_LBACK})

        self._info=ESC.info
        ESC.info=self.info

        self.Bind(wx.EVT_TIMER,self.onHideTimer,self.timer)
        self.btn_can.Bind(esui.EBIND_LEFT_CLK,self.onClkCan)
        self.Hide()
        return

    def info(self,string):
        string=self._info(string)
        if not self.Shown:
            self.txt_info.setValue(string)
        else:
            self.txt_info.appendText('\n'+string)
        self.Show()
        self.timer.StartOnce(2000)
        return

    def onClkCan(self,e):
        self.Hide()
        return

    def onHideTimer(self,e):
        self.Hide()
        return
    pass
