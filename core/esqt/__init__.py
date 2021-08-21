import PySide6.QtWidgets as qt
import PySide6.QtCore as qc
import PySide6.QtGui as qg
from .evt import *
CX=100
CY=100
CW=100
CH=100
XU=CW/100
YU=CH/100
COLOR_FRONT='#66ffcc'
COLOR_BLACK='#000000'
COLOR_BACK='#222222'
COLOR_LBACK='#333333'
COLOR_TEXT='#ffffff'
COLOR_HOVER='#555555'
COLOR_DECRO='#996600'
TEXT_FONT='Microsoft YaHei'
TEXT_LANG='简体中文'
SIZE_SBTN=(20,20)
class EvrSimQtApp(qt.QApplication):
    SIG_EVT=qc.Signal([str,EventArg])
    def __init__(self):
        super().__init__([])
        self.list_qss=['core\\esqt\\base.qss']
        self.dict_signal=dict()
        self.dict_img=dict()
        self.ESMW:MainWindow=None
        self.MAP_DIV=None
        self.SIG_EVT.connect(self.onComEvt)
        self.setAttribute(qc.Qt.AA_EnableHighDpiScaling)
        self.initQui()
        return

    def initQui(self):
        global CW,CH,XU,YU,CX,CY,SIZE_SBTN
        screen=self.primaryScreen()
        geo=screen.availableGeometry()
        CW=geo.width()
        CH=geo.height()
        CX=geo.x()
        CY=geo.y()
        XU=CW/100
        YU=CH/100
        SIZE_SBTN=(4*YU,4*YU)
        return

    def applyQSS(self,src='',base=True):
        if isinstance(src,str):
            self.list_qss.append(src)
        elif isinstance(src,list):
            self.list_qss+=src
        str_qss=''
        for qss_src in self.list_qss:
            qss=open(qss_src,'r')
            for line in qss.readlines():
                if '[[' in line:
                    il=line.index('[[')
                    ir=line.index(']]')
                    expr=str(int(eval(line[il+2:ir])))
                    line=line[:il]+expr+line[ir+2:]
                str_qss+=line
                qss.close()
        str_qss=str_qss.replace('COLOR_FRONT',COLOR_FRONT)\
            .replace('COLOR_TEXT',COLOR_TEXT)\
            .replace('COLOR_BACK',COLOR_BACK)\
            .replace('COLOR_LBACK',COLOR_LBACK)\
            .replace('COLOR_HOVER',COLOR_HOVER)\
            .replace('TEXT_FONT',TEXT_FONT)
        self.setStyleSheet(str_qss)
        return

    def lang(hint):

        return

    def loadImg(self,src:str):
        if src not in self.dict_img:
            self.dict_img[src]=qg.QImage(src)
        ret:qg.QImage=self.dict_img[src]
        return ret

    def getBitmap(self,src,resize=[0,0]):
        if isinstance(src,qg.QImage):img=src
        elif isinstance(src,str):img=self.loadImg(src)

        if isinstance(resize,qc.QSize):size=resize
        else:
            if resize[0]==0:resize[0]=img.width()
            if resize[1]==0:resize[0]=img.height()
            size=qc.QSize(resize[0],resize[1])
        img=img.scaled(size,qc.Qt.IgnoreAspectRatio)
        out=qg.QPixmap.fromImage(img)
        return out

    def bindIndex(self,container,label):
        ''' Reserved label:
            * ESMW/MAP_DIV/MDL_DIV/CMD_DIV;
            * TOOL_DIV/SIDE_DIV/HEAD_DIV;'''
        # if hasattr(self,label):return False
        if label=='ESMW':
            self.ESMW:MainWindow=container
        if label=='MAP_DIV':
            self.MAP_DIV=container
        # elif label=='MDL_DIV':
        #     from core import estl
        #     self.MDL_DIV:estl.MdlDiv=container
        # elif label=='CMD_DIV':
        #     from core import estl
        #     self.CMD_DIV:estl.CmdDiv=container
        # elif label=='TOOL_DIV':
        #     from core import estl
        #     self.TOOL_DIV:estl.ToolDiv=container
        # elif label=='SIDE_DIV':
        #     from core import estl
        #     self.SIDE_DIV:estl.SideDiv=container
        # elif label=='HEAD_DIV':
        #     from core import estl
        #     self.HEAD_DIV:estl.HeadDiv=container
        return True

    def hasIndex(self,label):
        return hasattr(self,label)

    def bindSignal(self,slot,signal=SIG_COM_EVT):
        if signal not in self.dict_signal:
            self.dict_signal[signal]=[slot]
        else:
            self.dict_signal[signal].append(slot)
        return

    def emitSignal(self,signal,**args):
        self.SIG_EVT.emit(signal,EventArg(**args))
        return

    def onComEvt(self,signal,e):
        for sig in self.dict_signal[signal]:
            sig(e)
        return
    pass
ESQTAPP=EvrSimQtApp()

class MainWindow(qt.QMainWindow):
    def __init__(self,**argkw) -> None:
        super().__init__()
        self.x_abs=CX
        self.y_abs=CY
        self.setGeometry(CX,CY,CW,CH)
        self.setWindowFlags(qc.Qt.FramelessWindowHint)
        icon=argkw.get('icon','res\\img\\evrsim.ico')
        self.setWindowIcon(qg.QIcon(icon))
        title=argkw.get('title','EvrSim')
        self.setWindowTitle(title)
        # ESAPP.bindSignal(self.onComEvt)
        ESQTAPP.bindIndex(self,'ESMW')
        return

    def onComEvt(e:EventArg):
        print(1)
        return

    pass

class QUIBase(object):
    ''' Box base class.'''
    def __init__(self:qt.QWidget,**argkw) -> None:
        ''' Para argkw:
            * `size`: Form like (w,h) or QSize.
                Item in `size` can be non-zero int for fixed,
                or (int,int) for min/max limited.
                Any item can be 0 for non-limited.
            * `pos`: Form like (x,y) or (x,y,a).
                Item a stands alignment using number dial 1-9.
            * style: str or dict.
                    * `border`: int or four ints forms like (top,bottom,left,right).
            '''

        self.prt:qt.QWidget=self.parent()
        self.cn=argkw.get('cn','')
        self.setObjectName(self.cn)
        if 'tip' in argkw:self.setToolTip(argkw['tip'])
        self._flag_passing=argkw.get('passing',False)

        if 'style' in argkw:
            self.setQSS(**argkw['style'])

        if 'pos' in argkw:
            self.move(int(argkw['pos'][0]),int(argkw['pos'][1]))

        if 'size' in argkw:
            s=argkw['size']
            if isinstance(s,qc.QSize):self.setFixedSize(s)
            elif isinstance(s,tuple):
                if isinstance(s[0],tuple):
                    if s[0][0]!=0:self.setMinimumWidth(s[0][0])
                    if s[0][1]!=0:self.setMaximumWidth(s[0][1])
                elif s[0]!=0:self.setFixedWidth(s[0])
                if isinstance(s[1],tuple):
                    if s[1][0]!=0:self.setMinimumHeight(s[1][0])
                    if s[1][1]!=0:self.setMaximumHeight(s[1][1])
                elif s[1]!=0:self.setFixedHeight(s[1])
        self.w=self.size().width()
        self.h=self.size().height()
        self._abs_pos=None
        return

    def setQSS(self,**style):
        str_stl=''
        for k,v in style.items():
            k=k.replace('_','-')
            if isinstance(v,str):str_stl+=k+':'+v+';'
            else:str_stl+=k+':'+str(v)+'px;'
        self.setStyleSheet(str_stl)
        return

    def getAbsPos(self:qt.QWidget):
        if self._abs_pos is not None:
            return self._abs_pos
        if hasattr(self.parent(),'getAbsPos'):
            prt_abs_pos=self.parent().getAbsPos()
        else:
            prt_abs_pos=(CX,CY)
        geo=self.geometry()
        pos=(prt_abs_pos[0]+geo.x(),prt_abs_pos[1]+geo.y())
        self._abs_pos=pos
        return pos

    def delChildren(self:qt.QWidget):
        children=self.children()
        for child in children:
            child.deleteLater()
        return
    pass

class Box(qt.QFrame,QUIBase):
    def __init__(self,parent:qt.QWidget,**argkw) -> None:
        qt.QFrame.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        return
    pass

class Btn(qt.QPushButton,QUIBase):
    def __init__(self,parent:qt.QWidget,**argkw) -> None:
        ''' Para:
            * argkw text: Text in button, empty default.
            * argkw border: False for the same color with bgc.
            * argkw toggle: If acting like a toggle button, False default.
            * argkw active: Being actived if True and toggle, False default.
            * argkw align: Default for 'center', 'left'/'right' optional.
            '''
        align=argkw.get('align','center')
        if 'style' not in argkw:argkw['style']=dict()
        argkw['style']['text-align']=align

        # argkw['style']['border-color']=self.color_border

        qt.QPushButton.__init__(self,parent=parent,text=argkw.get('text',''))
        QUIBase.__init__(self,**argkw)
        if argkw.get('toggle',False):
            self.flag_toggle=argkw.get('active',False)
            self.clicked.connect(self.onToggle)
        if argkw.get('border',True):
            self.setProperty('border','True')
        else:
            self.setProperty('border','False')
        return

    def onToggle(self):
        self.flag_toggle= not self.flag_toggle
        self.setToggle(self.flag_toggle)
        return

    def setToggle(self,flag=True):
        self.flag_toggle=flag
        if self.flag_toggle:
            self.setQSS(background_color=COLOR_FRONT,
                color=COLOR_BACK)
        else:
            self.setQSS(background_color=COLOR_LBACK,
                color=COLOR_TEXT)
            self.setStyleSheet(':hover{background-color:'+COLOR_HOVER+';}')
        return
    pass

class BtnMenu(Btn):
    def __init__(self, parent: qt.QWidget, **argkw) -> None:
        super().__init__(parent, **argkw)
        self._flag_border=argkw.get('border',True)
        self._pos_popup=argkw.get('pos_popup',7)
        self.list_item=argkw.get('item',list())
        self._menu=Menu(None)
        for item in self.list_item:
            self._menu.addAction(item)
        # self._menu.setStyleSheet('border-color:'+COLOR_FRONT+';')
        self.clicked.connect(self.popup)
        return

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._flag_border:
            qp = qg.QPainter()
            qp.begin(self)
            qp.setPen(qg.QColor(COLOR_FRONT))
            qp.setBrush(qg.QColor(COLOR_FRONT))
            m=YU//2
            rect=self.geometry()
            tri=qg.QPolygon([
                qc.QPoint(rect.width()-m,rect.height()-m),
                qc.QPoint(rect.width()-m,rect.height()-m-YU),
                qc.QPoint(rect.width()-m-YU,rect.height()-m),
                ])
            qp.drawPolygon(tri)
            qp.end()
        return

    def popup(self,pos:qc.QPoint=None):
        geo_menu=self._menu.geometry()
        abs_pos=self.getAbsPos()
        if self._pos_popup==7:
            pos=qc.QPoint(abs_pos[0],abs_pos[1]+self.h)
        elif self._pos_popup==9:
            pos=qc.QPoint(abs_pos[0]+self.w,abs_pos[1]+self.h-geo_menu.height())
        self._menu.popup(pos)
        return

    def bindPopup(self,method,signal='CLK'):
        if signal=='CLK':
            self._menu.triggered[qg.QAction].connect(method)
        if signal=='DCLK':
            self._menu.tri

        return
    pass
class Menu(qt.QMenu,QUIBase):
    def __init__(self, parent,**argkw) -> None:
        qt.QMenu.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        return
    pass

class Image(qt.QLabel,QUIBase):
    def __init__(self,parent:qt.QWidget,**argkw) -> None:
        qt.QLabel.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        self.setPixmap(ESQTAPP.getBitmap(argkw['src'],resize=self.size()))
        return
    pass

class StaticText(qt.QLabel,QUIBase):
    def __init__(self,parent:qt.QWidget,**argkw) -> None:
        ''' Para:
            * argkw text: Text.
            * font_size: h//2 px default.
            * argkw align: Default for 'center', 'left'/'right' optional.
            '''
        qt.QLabel.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        self.setTextFormat(qc.Qt.PlainText)
        self.setText(argkw.get('text',''))
        fsize=argkw.get('font_size',self.h//2)
        self.setStyleSheet('''
            padding:0px;
            font-size:'''+str(fsize)+'''px;''')
        align=argkw.get('align','center')
        if align=='left':
            self.setAlignment(qc.Qt.AlignLeft)
        elif align=='right':self.setAlignment(qc.Qt.AlignRight)
        else:self.setAlignment(qc.Qt.AlignHCenter)
        self.setAlignment(qc.Qt.AlignVCenter)
        return
    pass

class Dialog(qt.QDialog,QUIBase):
    ''' Dialog using QDialog.'''
    def __init__(self,parent:qt.QWidget=None,**argkw) -> None:
        ''' Para:
            * para parent: Qwidget.
            * argkw title: Title displayed on, 'Dialog' default.
            * argkw adjunct: If enable close button etc., True default.
            '''
        if 'size' not in argkw:argkw['size']=(60*XU,60*YU)
        if 'pos' not in argkw:argkw['pos']=(20*XU,20*YU)
        # argkw['relative']={'right':10}
        qt.QDialog.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        self.setWindowFlags(qc.Qt.FramelessWindowHint)
        self.box=Box(self,size=self.size(),style={'padding':YU,'margin':1})
        self._flag_adjunct=argkw.get('adjunct',True)
        if self._flag_adjunct:

            self.txt_title=StaticText(self.box,size=(20*YU,0),
                text=argkw.get('title','Dialog'),align='left')
            self.btn_close=Btn(self.box,text='×',size=SIZE_SBTN)
            self.btn_con=Btn(self.box,text='√',size=SIZE_SBTN)
            self.btn_can=Btn(self.box,text='×',size=SIZE_SBTN)


            hlay1=qt.QHBoxLayout()
            hlay1.addWidget(self.txt_title)
            hlay1.addStretch(1)
            hlay1.addWidget(self.btn_close)

            hlay3=qt.QHBoxLayout()
            hlay3.setSpacing(YU)
            hlay3.addStretch(1)
            hlay3.addWidget(self.btn_con)
            hlay3.addWidget(self.btn_can)
            self.hlay3=hlay3

            vlay=qt.QVBoxLayout(self.box)
            vlay.setContentsMargins(0,0,0,0)
            vlay.setSpacing(YU)
            vlay.addLayout(hlay1)
            vlay.addStretch(1)
            vlay.addLayout(hlay3)
            self.vlay=vlay

            self.btn_close.clicked.connect(self.close)
        return
    pass

class TableItem(Btn):
    def __init__(self,parent,**argkw):
        argkw['toggle']=True
        super().__init__(parent,**argkw)
        self.cell=argkw['cell']
        self.clicked.connect(self.onClk)
        return

    def onClk(self):
        self.prt.pos_selected=self.cell
        self.prt.deactiveOther(self.cell)
        return
    pass
class TableView(qt.QTableWidget,QUIBase):
    def __init__(self, parent,**argkw) -> None:
        if 'style' not in argkw:argkw['style']=dict()
        argkw['style']['padding']=0
        qt.QTableWidget.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        # self.verticalScrollBar().setVisible(False)
        # self.horizontalScrollBar().setVisible(False)
        self.setContentsMargins(0,0,0,0)
        self.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
        if not argkw.get('editable',False):
            self.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        if argkw.get('exclusive',False):
            self.setSelectionMode(qt.QAbstractItemView.SingleSelection)
        self.pos_selected=[-1,-1]
        return

    def addItem(self,item,pos):
        if isinstance(item,str):
            widget=TableItem(self,cell=pos,text=item)
            self.setCellWidget(pos[0],pos[1],widget)
        return

    def deactiveOther(self,pos):
        for i in range(self.rowCount()):
            for j in range(self.colorCount()):
                if i==pos[0] and j==pos[1]:continue
                cell=self.cellWidget(i,j)
                if cell is not None:cell.setToggle(False)
        return

    def getCurrentText(self):
        pos=self.pos_selected
        cell=self.cellWidget(pos[0],pos[1])
        return cell.text()

    pass

class TabPane(qt.QTabWidget,QUIBase):
    def __init__(self, parent,**argkw) -> None:
        if 'style' not in argkw:argkw['style']=dict()
        argkw['style']['padding']=0
        qt.QTabWidget.__init__(self,parent=parent)
        QUIBase.__init__(self,**argkw)
        return
    pass
class Tab(Box):
    def __init__(self, parent: qt.QWidget, **argkw) -> None:
        super().__init__(parent, **argkw)
        self.pane=TabPane(self,size=(self.w,self.h))
        return

    def addTab(self,parent,label):
        self.pane.addTab(parent,label)
        return
    pass

class HeadBar(Box):
    def __init__(self, parent: qt.QWidget, **argkw) -> None:
        if 'size' not in argkw:argkw['size']=(CW,5*YU)
        # dft_stl={
        #     'padding':YU//2,
        #     'border-bottom-style':'solid',
        #     'border-bottom-width':1,
        #     'border-bottom-color':COLOR_FRONT}
        # if 'style' not in argkw:argkw['style']=dft_stl
        # else:argkw['style'].update(dft_stl)
        super().__init__(parent,**argkw)
        self.str_title=argkw.get('title','')
        self._flag_menu=argkw.get('menu',True)
        self.btn_es=Btn(self,text='ES',size=SIZE_SBTN,border=False)
        self.btn_ext=Btn(self,text='×',size=SIZE_SBTN,border=False)
        if self._flag_menu:
            self.btn_sim=BtnMenu(self,text='Sim',size=(8*YU,4*YU),border=False,
                item=['New..','Open..','Save','Save as..','Setting..','Close'])
            self.btn_edit=BtnMenu(self,text='Edit',size=(8*YU,4*YU),border=False,
                item=['Undo','Redo','Copy','Cut','Paste'])
            self.btn_map=BtnMenu(self,text='Map',size=(8*YU,4*YU),border=False,
                item=['New..','Rename..','Save as..','Delete'])
            self.btn_model=BtnMenu(self,text='Model',size=(8*YU,4*YU),border=False,
                item=['New..','Rename..','Save as..','Delete'])
            self.btn_help=BtnMenu(self,text='Help',size=(8*YU,4*YU),border=False,
                item=['Help..','Read me..','About..'])
        if self.str_title:'todo'
        hbox=qt.QHBoxLayout(self)
        hbox.setContentsMargins(0,0,0,0)
        hbox.setSpacing(0)
        hbox.addWidget(self.btn_es)
        if self._flag_menu:
            hbox.addWidget(self.btn_sim)
            hbox.addWidget(self.btn_edit)
            hbox.addWidget(self.btn_map)
            hbox.addWidget(self.btn_model)
            hbox.addWidget(self.btn_help)
        if self.str_title:'todo'
        hbox.addStretch(1)
        hbox.addWidget(self.btn_ext)
        self.btn_es.clicked.connect(self.onClkEs)
        self.btn_ext.clicked.connect(self.onClkExt)
        return

    def onClkExt(self):
        self.parent().close()
        return
    def onClkEs(self):
        ESQTAPP.MAP_DIV.setFixedSize(500,500)
        return
    pass

from .gl import GLBox
