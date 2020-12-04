# -*- coding: UTF-8 -*-
'ESUI defination.'
import wx
# Globals variable;
WXAPP=wx.App()
cx,cy,cw,ch=wx.ClientDisplayRect()
XU=cw/100
YU=ch/100
APPNAME=''
WXMW=None
HEAD_PLC=None
TOOL_PLC=None
CMD_PLC=None
ARO_PLC=None
ACP_PLC=None
SIDE_PLC=None
COLOR_FRONT='#66ffcc'
COLOR_BLACK='#000000'
COLOR_BACK='#222222'
COLOR_LBACK='#333333'
COLOR_TEXT='#ffffff'
COLOR_ACTIVE='#555555'
COLOR_DECRO='#996600'
TEXT_FONT='Microsoft YaHei'

from .window import EsWindow
# Panel container;
from .plc import Plc
from .plc import ScrolledPlc

# Text ctrl;
from .textctrl import StaticText
from .textctrl import TransText
from .textctrl import InputText
from .textctrl import MultilineText
from .textctrl import HintText

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

# Button;
from .btn import Btn
from .btn import BorderlessBtn
from .btn import SelectBtn
from .btn import BlSelectBtn
from .btn import TabBtn

from .plc_Head import HeadPlc
from .plc_Head import HeadBar
from .plc import CmdPlc
from .plc import PopupPlc
from .plc_tree import TreePlc
from .plc_tree import SimTreePlc
from .plc_tree import MapTreePlc
from .plc_tree import ModelTreePlc

class ESFont(wx.Font):
    ''' Simple font class.

        Para argkw: size.'''
    def __init__(self,**argkw):
        size=argkw.get('size',12)
        super().__init__(int(size),wx.MODERN,wx.NORMAL,wx.NORMAL,False,TEXT_FONT)
    pass
