# libs;
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from core import ESC
from core import esui
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = [esui.TEXT_FONT]
# Mod-in import;
pass
# MOD INDEX
MOD_NAME='AroPlot'
MOD_VER='0.0.1'
MOD_SETTING={}
AROCLASS_INDEX=[]
ACP_INDEX=[]
TOOL_INDEX=[]
MODEL_INDEX=[]

# Tool preset.
# Variable of tool name need to add to TOOL_INDEX, otherwise unable to be indexed;
class FigurePlc(esui.Plc):
    ''' Support argument keyword: xdata/ydata/title/xlabel/ylabel.'''
    def __init__(self,parent,p,s,**argkw):
        super().__init__(parent,p,s)
        xdata=argkw.get('xdata',range(1,11))
        ydata=argkw.get('ydata',[0]*10)
        self.title=argkw.get('title','')
        self.xlabel=argkw.get('xlabel','')
        self.ylabel=argkw.get('ylabel','')
        self.canvas=None
        self.point_dict=dict()  # {'label':[(x,y),..]}
        self.initFigure()
        self.drawFigure()
        return

    def appendPoints(self,pointdict):
        for label,points in pointdict.items():
            if label in self.point_dict:
                    self.point_dict[label]+=points
            else:self.point_dict[label]=points
        self.drawFigure()
        return

    def initFigure(self,**argkw):
        xdata=argkw.get('xdata',range(1,11))
        ydata=argkw.get('ydata',[0]*10)
        self.title=argkw.get('title',self.title)
        self.xlabel=argkw.get('xlabel',self.xlabel)
        self.ylabel=argkw.get('ylabel',self.ylabel)

        self.figure = Figure()

        self.figure.set_figwidth(self.Size[0]/100)
        self.figure.set_figheight(self.Size[1]/100)
        self.axes = self.figure.add_subplot(111)
        self.axes.axis([0,5,-3,1])
        self.axes.set_title(self.title)
        self.axes.grid(True)
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.canvas=FigureCanvas(self, -1, self.figure)
        return

    def drawFigure(self):
        # self.axes.cla()
        for label,points in self.point_dict.items():
            xdata=list()
            ydata=list()
            for p in points:
                xdata.append(p[0])
                ydata.append(p[1])
            # self.plot_data.set_xdata(xdata)
            # self.plot_data.set_ydata(ydata)
            self.axes.plot(xdata,ydata,'-',color='r')
        self.canvas.draw()
        return
    pass
