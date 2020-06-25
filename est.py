#!/usr/bin/python
# -*- coding: UTF-8 -*-
'EvrSim Core and Terminal;'
# system libs;
import sys
import os
import re
import shutil
# Terminal needed variable;
from core import EvrSimCore
EST_VER = '0.0.2'
EST_EXIT=False
EST_CONTINUE=None

# Terminal enterance;
# EvrSim Core and Terminal initilization;
print('EvrSim '+' Console '+EST_VER)
ESC=EvrSimCore()

# system main loop;
if len(sys.argv)!=1:
    # As subprogress of EvrSimWx;
    while not EST_EXIT:
        if EST_CONTINUE is None:
            com=sys.stdin.readline()
            if com is None:
                continue
        else:
            com=EST_CONTINUE
            EST_CONTINUE=None

        try:exec(com)
        except BaseException as e:print('E: ',e)
        sys.stdout.writelines('EOF\n')
        sys.stdout.flush()
else:
    # As standalone terminal;
    while not EST_EXIT:
        if EST_CONTINUE is None:
            com = input('EvrSim>>')
        else:
            com=EST_CONTINUE
            EST_CONTINUE=None

        try:exec(com)
        except BaseException as e:print('E: ',e)
exit()
