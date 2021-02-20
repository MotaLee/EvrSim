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
# EvrSim global variable;
ES_VER='0.0.13'
EST_VER = '0.0.4'
ES_UPDATE=20201204
ES_PY_VER_MIN='3.8.0'
ES_PY_VER_MIN='3.8.7'
ES_MOD=['AroCore','Dynamics','AroPlot','STS']
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
    if 'Editor' in sys.argv:
        ESAPP=wx.App()
        from app.Editor import EvrSimEditor
        # Main enterance;
        wxmw=EvrSimEditor()
        ESAPP.MainLoop()
    elif 'EST' in sys.argv:pass
