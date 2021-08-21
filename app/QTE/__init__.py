import os
import EvrSim
from core import esc,esqt,esgl
from .gltoolbar import GLToolbar
from .tool import ToolDiv
ESC=esc.ESC
YU=esqt.YU
XU=esqt.XU
ESQTAPP=esqt.ESQTAPP
QTE_TITLE='EvrSim QEditor'
QTE_VER='0.0.1'

class OpenDialog(esqt.Dialog):
    def __init__(self, parent:esqt.qt.QWidget, **argkw) -> None:
        argkw['title']='Open Sim'
        super().__init__(parent=parent, **argkw)

        self.btn_path=esqt.Btn(self,text='  Sim:',size=(0,4*YU),align='left')
        self.table=esqt.TableView(self,size=(0,self.h-17*YU),editable=False,exclusive=True)
        self.btn_simfolder=esqt.Btn(self,text='Sim Folder',size=(8*YU,4*YU))
        self.vlay.insertWidget(1,self.btn_path)
        self.vlay.insertWidget(2,self.table)
        self.hlay3.insertWidget(1,self.btn_simfolder)

        list_fdr=os.listdir('sim\\')
        self.table.setColumnCount(4)
        self.table.setRowCount(len(list_fdr)//4+1)
        count=0
        for i in range(len(list_fdr)):
            if list_fdr[i][0]=='_':continue
            self.table.addItem(list_fdr[i],(count//4,count%4))
            count+=1

        self.btn_con.clicked.connect(self.onClkCon)
        return

    def onClkCon(self):
        simname=self.table.getCurrentText()
        ESC.openSim(simname)
        ESQTAPP.emitSignal(esqt.SIG_OPEN_SIM)
        self.close()
        return
    pass

class WelDiv(esqt.Box):
    def __init__(self, parent:esqt.qt.QWidget, **argkw) -> None:
        super().__init__(parent, **argkw)
        s=self.size()
        self.bgi=esqt.Image(self,size=s,src='res/img/splash.png')
        self.weltt=esqt.StaticText(self,text=QTE_TITLE+' : '+QTE_VER,pos=(4*YU,s.height()-10*YU))
        self.weltt=esqt.StaticText(self,text='EvrSim ver : '+EvrSim.ES_VER,pos=(4*YU,s.height()-5*YU))
        return

    pass

class SideDiv(esqt.Tab):
    def __init__(self, parent, **argkw) -> None:
        super().__init__(parent, **argkw)
        self.mgr_div=esqt.Box(None)
        self.addTab(self.mgr_div,'Manager')
        return

    pass

class ESQtEditor(esqt.MainWindow):
    def __init__(self):
        super().__init__(title=QTE_TITLE)
        self.headbar=esqt.HeadBar(self)
        self.weldiv=WelDiv(self,
            pos=(esqt.CW//4,esqt.CH//4),
            size=(esqt.CW//2,esqt.CH//2))
        self.tooldiv=ToolDiv(self,pos=(0,5*YU),size=(75*XU,20*YU))
        self.gldiv=esqt.GLBox(self,pos=(4*YU,25*YU),size=(75*XU,75*YU))
        ESQTAPP.bindIndex(self.gldiv,'MAP_DIV')
        self.toolbar=GLToolbar(self,pos=(0,25*YU),size=(4*YU,75*YU))
        self.sidediv=SideDiv(self,pos=(75*XU,5*YU),size=(25*XU,95*YU))
        self.gldiv.hide()
        self.tooldiv.hide()
        self.sidediv.hide()
        self.toolbar.hide()
        self.headbar.btn_sim.bindPopup(self.onClkSim)
        esqt.ESQTAPP.applyQSS('app\\QTE\\qeditor.qss')
        esqt.ESQTAPP.bindSignal(self.onOpenSim,signal=esqt.SIG_OPEN_SIM)
        self.show()
        return

    def onClkSim(self,action:esqt.qg.QAction):
        item=action.text()
        if item=='Open..':
            dia_open=OpenDialog(None)
            dia_open.exec()
        return

    def onOpenSim(self,e):
        self.weldiv.hide()
        self.gldiv.show()
        self.tooldiv.show()
        self.toolbar.show()
        self.sidediv.show()
        esgl.GLC.lookAt([5,5,5])
        return

    pass

ESMW=ESQtEditor()
ESQTAPP=esqt.ESQTAPP
