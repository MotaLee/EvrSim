# -*- coding: UTF-8 -*-
'ESUI defination, base on wx;'

# Globals variable;
XU=0
YU=0
WXMW=None
HEAD_PLC=None
MOD_PLC=None
COM_PLC=None
ARO_PLC=None
ACP_PLC=None
SIDE_PLC=None
COLOR_FRONT='#66ffcc'
COLOR_BLACK='#000000'
COLOR_BACK='#222222'
COLOR_LBACK='#333333'
COLOR_TEXT='#ffffff'
COLOR_SECOND='#555555'
TEXT_FONT='Microsoft YaHei'

# Text ctrl;
from .textctrl import Stc
from .textctrl import Ttc
from .textctrl import Tcc
from .textctrl import Mtc

# Panel container;
from .plc import Plc
from .plc import ScrolledPlc
from .plc import AroTreePlc

from .plc_HeadPlc import HeadPlc
from .plc_ModPlc import ModPlc
from .plc import ComPlc
from .plc_AcpPlc import AcpPlc
from .plc_SidePlc import SidePlc

# Popup;
from .popup import MenuBtn
from .popup import BorderlessMenuBtn
from .popup import SelectMenuBtn

# EvrSim general dialog;
from .esdialog import EsDialog
from .esdialog import NewDialog
from .esdialog import OpenDialog
from .esdialog import SaveAsDialog
from .esdialog import SettingDialog
from .esdialog import ModDialog

# Button;
from .btn import btn
from .btn import BorderlessBtn
from .btn import SelectBtn
from .btn import BlSelectBtn
from .btn import TabBtn


# Box;
from .box import ListBox
