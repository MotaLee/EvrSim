'ESUI defination.'
import wx
cx,cy,cw,ch=wx.ClientDisplayRect()
XU=cw/100
YU=ch/100
COLOR_FRONT='#66ffcc'
COLOR_BLACK='#000000'
COLOR_BACK='#222222'
COLOR_LBACK='#333333'
COLOR_TEXT='#ffffff'
COLOR_HOVER='#555555'
COLOR_DECRO='#996600'
TEXT_FONT='Microsoft YaHei'

STL_DFT={'p':(0,0),'s':(0,0),'bgc':COLOR_BACK}
STL_BOX={'border':COLOR_FRONT}
STL_FILL={'bgc':COLOR_FRONT}
ICON={'normal':'res/img/aro.png'}

from .method import *
from .evt import *
from .window import EsWindow
# Panel container;
from .div import Div,ScrollDiv,ComboPopDiv,ComboDiv,IndePopupDiv,MenuBtnDiv

# Text ctrl;
from .text import DivText,MultilineText,HintText
from .text import StaticText,TransText,InputText
# Button;
from .btn import Btn,SltBtn,DivBtn,TglBtn

# Popup;

# EvrSim general dialog;
from .dialog import EsDialog
from .dialog import NewDialog
from .dialog import OpenDialog
from .dialog import SaveAsDialog
from .dialog import SettingDialog
from .dialog import ModDialog
from .dialog import MapDialog
from .dialog import ModelDialog

from .tree import TreeDiv,TreeItemDiv

from .tab import TabDiv,TabBtn

class ESFont(wx.Font):
    def __init__(self,**argkw):
        ''' Simple font class.
            * Argkw size: Font size. 12 default;'''
        size=argkw.get('size',12)
        super().__init__(int(size),wx.MODERN,wx.NORMAL,wx.NORMAL,False,TEXT_FONT)
    pass

class UIManager(object):
    ''' ESUI binding index.'''
    def __init__(self) -> None:
        self.dict_bitimg=dict()
        self.dict_cursor=dict()
        return

    def bindIndex(self,container,label):
        ''' Reserved label:
            * ESMW/MAP_DIV/MDL_DIV/CMD_DIV;
            * TOOL_DIV/SIDE_DIV/HEAD_DIV;'''
        if hasattr(self,label):return False
        if label=='ESMW':
            self.ESMW:EsWindow=container
        if label=='MAP_DIV':
            from core import esgl
            self.MAP_DIV:esgl.GLDiv=container
        elif label=='MDL_DIV':
            from core import estl
            self.MDL_DIV:estl.MdlDiv=container
        elif label=='CMD_DIV':
            from core import estl
            self.CMD_DIV:estl.CmdDiv=container
        elif label=='TOOL_DIV':
            from core import estl
            self.TOOL_DIV:estl.ToolDiv=container
        elif label=='SIDE_DIV':
            from core import estl
            self.SIDE_DIV:estl.SideDiv=container
        elif label=='HEAD_DIV':
            from core import estl
            self.HEAD_DIV:estl.HeadDiv=container
        return True

    def hasIndex(self,label):
        return hasattr(self,label)

    def loadImg(self,**argkw):
        ''' Load iamge into manager.
            * Argkw path: Path of image;
            * Argkw manage: Add loaded image to manager, True defalut;
            * Argkw w: width of image, non-set for original;
            * Argkw h: height of image, non-set for original;
            '''
        path=argkw.get('path','')
        img=wx.Image(path,type=wx.BITMAP_TYPE_PNG)
        w=argkw.get('w',img.Width)
        h=argkw.get('h',img.Height)
        img=img.Scale(w,h).ConvertToBitmap()
        if argkw.get('manage',True):
            self.dict_bitimg[path]=img
        return img

    def getImg(self,**argkw):
        ''' Get iamge from manager.
            * Argkw path: Path key of image;
            * Argkw load: Load image if not found. True defalut;
            * Other argkw: For loadImg;
            '''
        path=argkw.get('path','')
        if path in self.dict_bitimg:
            return self.dict_bitimg[path]
        else:
            if argkw.get('load',True):
                return self.loadImg(**argkw)
        return

    def getCursor(self,**argkw):
        ''' Get Cursor from manager.
            * Argkw path: Path key of cursor image;
            * Argkw load: Load image if not found. True defalut;
            '''
        path=argkw.get('path')
        if path in self.dict_cursor:
            out:wx.Cursor=self.dict_cursor[path]
            return out
        else:
            if argkw.get('load',True):
                img=wx.Image(path,type=wx.BITMAP_TYPE_PNG)
                cursor=wx.Cursor(img)
                self.dict_cursor[path]=cursor
                return cursor
        return
    pass
UMR=UIManager()
