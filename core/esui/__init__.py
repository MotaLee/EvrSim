# -*- coding: UTF-8 -*-
'ESUI defination, base on wx;'
# Libs;
# import core
import sys
import os
import math
import time
import wx
sys.path.append(os.getcwd())

# Global module variable;
class GMV:
    XU=0
    YU=0
    COLOR_Front='#66ffcc'
    COLOR_Back='#222222'
    COLOR_Text='#ffffff'
    COLOR_Second='#555555'
    pass
gmv=GMV()

# Text ctrl;
from .textctrl import Stc
from .textctrl import Ttc
from .textctrl import Tcc

# Panel container;
from .plc import Plc
from .plc import ComPlc
from .plc import SidePlc
from .plc import ModPlc
from .plc import AcpPlc

# Move bar;
from.movebar import MoveBar

# Tab btn;
from .estab import TabBtn
from .estab import ModTab
from .estab import SideTab
from .estab import AroSideTab
from .estab import AroveSideTab
from .estab import AcpSideTab

# Menu btn;
from .menubtn import MenuBtn
from .menubtn import BorderlessMenuBtn

# EvrSim general dialog;
from .esdialog import EsDialog
from .esdialog import NewDialog
from .esdialog import OpenDialog
from .esdialog import ModDialog

# Button;
from .btn import btn
from .btn import BorderlessBtn
from .btn import SelectBtn

# Box;
from .box import ListBox
