# -*- coding: UTF-8 -*-
'ESUI defination.'
import wx
# Globals variable;
cx,cy,cw,ch=wx.ClientDisplayRect()
XU=cw/100
YU=ch/100
# Colors;
COLOR_FRONT='#66ffcc'
COLOR_BLACK='#000000'
COLOR_BACK='#222222'
COLOR_LBACK='#333333'
COLOR_TEXT='#ffffff'
COLOR_ACTIVE='#555555'
COLOR_DECRO='#996600'

TEXT_FONT='Microsoft YaHei'

STL_DFT={'p':(0,0),'s':(0,0),'bgc':COLOR_BACK,'fgc':COLOR_FRONT,'text':COLOR_TEXT}
STL_BOX={'border':COLOR_FRONT}
STL_FILL={'bgc':COLOR_FRONT}

from .method import toggleWorkspace
from .window import EsWindow
# Panel container;
from .div import Div,ScrollDiv,Plc,ScrolledPlc
# Text ctrl;
from .textctrl import StaticText,TransText,InputText
from .textctrl import MultilineText,HintText
# Button;
from .btn import Btn,SltBtn,TabBtn

# Popup;
from .popup import PopupList
from .popup import MenuBtn
from .popup import BorderlessMenuBtn
from .popup import SelectMenuBtn

# EvrSim general dialog;
from .dialog import EsDialog
from .dialog import NewDialog
from .dialog import OpenDialog
from .dialog import SaveAsDialog
from .dialog import SettingDialog
from .dialog import ModDialog
from .dialog import MapDialog
from .dialog import ModelDialog

from .plc_Head import HeadPlc
from .plc_Head import HeadBar
from .div import CmdPlc
from .div import PopupPlc
from .plc_tree import TreeDiv,TreeItemDiv

from .tab import TabDiv,TabDivBtn

class ESFont(wx.Font):
    ''' Simple font class.
        * Para argkw: size.'''
    def __init__(self,**argkw):
        size=argkw.get('size',12)
        super().__init__(int(size),wx.MODERN,wx.NORMAL,wx.NORMAL,False,TEXT_FONT)
    pass

class Index(object):
    ''' ESUI binding index.'''
    def __init__(self) -> None:
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
            self.MAP_DIV:esgl.AroGlc=container
        elif label=='MDL_DIV':
            from core import estl
            self.MDL_DIV:estl.MdlDiv=container
        elif label=='CMD_DIV':
            self.CMD_DIV:CmdPlc=container
        elif label=='TOOL_DIV':
            from core import estl
            self.TOOL_DIV:estl.ToolDiv=container
        elif label=='SIDE_DIV':
            from core import estl
            self.SIDE_DIV:estl.SideDiv=container
        elif label=='HEAD_DIV':
            self.HEAD_DIV:HeadPlc=container
        return True

    def hasIndex(self,label):
        return hasattr(self,label)
    pass
IDX=Index()
