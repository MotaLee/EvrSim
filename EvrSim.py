''' ## EvrSim Main Program.
    ---
    ### Usage
    * Command 'python EvrSim.py app'. Para 'app' can be 'EST'/'Editor' or other user's app.
    ---
    Copyright 2020-2021 @Mota Lee.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''
import sys,os
cwd=os.getcwd()
PATHS=[cwd,cwd+'\\res\\lib',cwd+'\\res\\lib\\dll']
for path in PATHS:
    sys.path.append(path)
    os.environ['PATH']+=';'+path
# EvrSim global variable;
ES_VER='0.1.0'
EST_VER = '0.0.5'
EDITOR_VER='0.0.14'
ES_PY_VER_MIN='3.8.0'
ES_PY_VER_MAX='3.8.7'
ES_MOD=['AroCore','Dynamics','AroPlot','AroGame']
# Pip installation;
ES_LIBS=[
    'wxpython',
    'numpy',
    'pyopengl',
    'interval',
    'matplotlib',
    'pillow']

ES_INTERGRATED_LIBS=[
    'pyglm==1.99.1',
    'pybullet'
    'pyassimp'
]
global ESAPP
ESAPP=sys.argv[1]
if __name__ == "__main__":
    if ESAPP=='QTE':
        from app.QTE import ESMW,ESQTAPP
        ESMW.show()
        ESQTAPP.exec()
    elif ESAPP=='Editor':
        import wx
        import mod,app
        ESWXAPP=wx.App()
        from app.Editor import EvrSimEditor
        wxmw=EvrSimEditor()
        ESWXAPP.MainLoop()
    elif 'EST'==sys.argv[1]:
        from app.EST import ESTerminal
        # Main enterance;
        est=ESTerminal()
        est.running()
    elif 'setup'==sys.argv[1]:
        'todo'
        print('Setup completed, please rerun EvrSim.')
        exit()
    else:
        import wx
        import mod,app
        ESWXAPP=wx.App()
        from core import ESC,esui
        ESC.setApp(sys.argv[1])
        exec('import app.'+sys.argv[1]+'',globals(),locals())
        esui.UMR.ESMW.lauchApp()
        ESWXAPP.MainLoop()
