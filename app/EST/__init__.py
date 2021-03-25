#!/usr/bin/python
# -*- coding: UTF-8 -*-
'### EvrSim Terminal'
# system libs;
import EvrSim
from core import ESC

'todo: As subprogress of EvrSimWx;'

class ESTerminal(object):
    def __init__(self) -> None:
        ''' As standalone terminal process.'''
        super().__init__()
        self.FLAG_EXIT=False
        self.COM_NEXT=''
        ESC.setApp('EST')
        print('EvrSim Terminal '+EvrSim.EST_VER)
        return

    def running(self):
        self.testCommand()
        while not self.FLAG_EXIT:
            if not self.COM_NEXT:
                com = input('EvrSim>>')
            else:
                com=str(self.COM_NEXT)
                self.COM_NEXT=''

            try:exec(com)
            except BaseException as e:ESC.err(e)
        return

    def testCommand(self):
        'Write TEST command here, those will execute at the start of running.'
        # ESC.openSim('t')
        # ESC.compileModel()
        # ESC.runCompiledSim()
        return
    pass
