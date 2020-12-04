from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from core import ESC,esui
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = [esui.TEXT_FONT]
class CanvasPlc(esui.Plc):
    ''' Support argument keyword: xdata/ydata/title/xlabel/ylabel.'''
    def __init__(self,parent,p,s):
        super().__init__(parent,p,s)
        # xdata=argkw.get('xdata',range(1,11))
        # ydata=argkw.get('ydata',[0]*10)
        self.title=''
        self.xlabel=''
        self.ylabel=''
        self.canvas=None
        self.figure = Figure()
        self.line_dict=dict()  # {'label':[(x,y),..]}
        self.drawed_lines=dict()    # {'label':Line,..}
        # self.initFigure()
        # self.drawFigure()
        return

    def appendPoints(self,pointdict):
        for label,points in pointdict.items():
            if label in self.line_dict:
                    self.line_dict[label]+=points
            else:self.line_dict[label]=points
        self.drawCanvas()
        return

    def clearPoints(self):
        self.line_dict=dict()
        self.drawed_lines=dict()
        self.drawCanvas()
        return

    def initCanvas(self,**argkw):
        # xdata=argkw.get('xdata',range(1,11))
        # ydata=argkw.get('ydata',[0]*10)
        self.title=argkw.get('title',self.title)
        self.xlabel=argkw.get('xlabel',self.xlabel)
        self.ylabel=argkw.get('ylabel',self.ylabel)

        self.figure.set_figwidth(self.Size[0]/100)
        self.figure.set_figheight(self.Size[1]/100)
        self.axes = self.figure.add_subplot(111)
        self.axes.axis([0,10,-3,1])
        self.axes.set_title(self.title)
        self.axes.grid(True)
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.canvas=FigureCanvas(self,-1,self.figure)
        return

    def drawCanvas(self):
        if len(self.line_dict)==0:
            for line in self.drawed_lines:
                line
        for label,points in self.line_dict.items():
            xdata=list()
            ydata=list()
            for p in points:
                xdata.append(p[0])
                ydata.append(p[1])
            if label in self.drawed_lines:
                line=self.drawed_lines[label][0]
                line.set_xdata(xdata)
                line.set_ydata(ydata)
            else:
                self.drawed_lines[label]=self.axes.plot(xdata,ydata,'-',color='r')
        self.canvas.draw()
        return
    pass
