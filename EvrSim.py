'Copyright 2020 Mota Lee'
''' This program is free software: you can redistribute it and/or modify
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
import wx
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\res\\lib')
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
sys.path.append(os.getcwd()+'\\res\\lib\\dll')
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib\\dll'
# EvrSim global variable;
ES_VER='0.0.14'
EST_VER = '0.0.5'
ES_UPDATE=20201204
ES_PY_VER_MIN='3.8.0'
ES_PY_VER_MAX='3.8.7'
ES_MOD=['AroCore','Dynamics','AroPlot']
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

if __name__ == "__main__":
    ESAPP=wx.App()
    if 'Editor'==sys.argv[1]:
        from app.Editor import EvrSimEditor
        # Main enterance;
        wxmw=EvrSimEditor(es_ver=ES_VER)
        ESAPP.MainLoop()
    elif 'EST'==sys.argv[1]:
        from app.EST import ESTerminal
        # Main enterance;
        est=ESTerminal()
        est.running()
    else:
        ESAPP=wx.App()
        # _local=locals()
        exec('from app.'+sys.argv[1]+' import ESMW')
        # ESMW=_local['ESMW']
        ESAPP.MainLoop()
