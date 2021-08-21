''' ## 智能被动双目焊缝跟踪系统'''
# App variable;
SWT_VER='0.0.3'     # Biocam Welding Tracking;
SWT_TITLE='智能被动双目焊缝跟踪系统'
SWT_PATH='app/Welding'
SWT_NAME='Welding'
SIM_NAME='swt'
ARO_INDEX=[]
ACP_INDEX=[]
MODEL_INDEX=[]

# Outer libs;
# EvrSim libs;
import wx
import numpy as np
# from core import esc,esui,esgl,estl,ESC
# from app.Welding.definition import FuncX3,MtImg
# from app.Welding.welding import StereoWelding
# from mod.AroCore import RunSimBtn,ResetMapBtn
# xu=esui.XU
# yu=esui.YU
# UMR=esui.UMR
# esui.COLOR_BACK='#ffffff'
# esui.COLOR_LBACK='#eeeeee'
# esui.COLOR_TEXT='#000000'
# esui.COLOR_FRONT='#66ccff'
# esui.COLOR_HOVER='#666699'
# esui.COLOR_DECRO='#996600'

# class AroPipe(esc.Aro):
#     def __init__(self):
#         super().__init__()
#         self.adp='app.Welding.AdpPipe'
#         self.pts=list()
#         self.edges=None
#         self.faces=list()
#         self.position=[0,0,0]
#         return
#     pass

# class AdpPipe(esgl.AroDrawPart):
#     def __init__(self, aroid):
#         super().__init__(aroid)
#         va=np.array(self.Aro.pts,dtype=np.float32)
#         ea=np.array(self.Aro.faces,dtype=np.uint32)
#         self.addMesh(draw_type=esgl.DT_QUAD,
#             layout=[esgl.VtxLayout('color')],
#             vertices=va,faces=ea)
#         self.updateAdp()
#         return

#     # def updateAdp(self):
#     #     super().updateAdp()
#     #     if len(self.Aro.pts)>len(self.list_mesh):
#     #         va=np.array(self.Aro.pts[-1],dtype=np.float32)
#     #         ea=np.array(self.Aro.faces[-1],dtype=np.uint32)
#     #         self.addMesh(draw_type=esgl.DT_QUAD,
#     #             layout=[esgl.VtxLayout('color')],
#     #             vertices=va,faces=ea)
#     #     self.flag_update=True
#     #     return
#     pass

# class PlotDiv(esui.Div):
#     def __init__(self,parent,**argkw):
#         super().__init__(parent,**argkw)
#         self.btn_sleeve=esui.TabBtn(self,style={'p':(0,0),'s':(8*yu,4*yu)},label='滑套')
#         self.btn_pistol=esui.TabBtn(self,style={'p':(8*yu,0),'s':(8*yu,4*yu)},label='活塞')
#         from mod.AroPlot import CanvasDiv
#         self.canvas=CanvasDiv(self,style={
#             'p':(yu,4*yu),'s':(self.Size.x-2*yu,self.Size.y-14*yu)})
#         self.canvas.initCanvas(title='仿真数据追踪',xlabel='T/s',ylabel='Displacement/mm')
#         self.canvas.drawCanvas()

#         esui.StaticText(self,(yu,self.Size.y-10*yu),(8*yu,4*yu),'显示选项：',align='left')

#         self.btn_x=esui.SltBtn(self,(yu,self.Size.y-5*yu),(4*yu,4*yu),'√',select=True)
#         self.txt_x=esui.StaticText(self,(5*yu,self.Size.y-5*yu),(8*yu,4*yu),'位移')

#         self.btn_v=esui.SltBtn(self,(13*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
#         self.txt_v=esui.StaticText(self,(17*yu,self.Size.y-5*yu),(8*yu,4*yu),'速度')

#         self.btn_a=esui.SltBtn(self,(26*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
#         self.txt_a=esui.StaticText(self,(30*yu,self.Size.y-5*yu),(8*yu,4*yu),'加速度')

#         self.btn_pip=esui.SltBtn(self,(39*yu,self.Size.y-5*yu),(4*yu,4*yu),'√')
#         self.txt_pip=esui.StaticText(self,(43*yu,self.Size.y-5*yu),(8*yu,4*yu),'管压')
#         self.updateStyle(style={'bgc':esui.COLOR_LBACK})
#         self.Bind(esui.EBIND_COMEVT,self.onPPComEvt)
#         return

#     def onPPComEvt(self,e):
#         etype=e.getEventArgs()
#         if etype==esui.ETYPE_STEP_SIM:
#             x=ESC.getAro('toe_sleeve').position[0]
#             t=ESC.getAcp(6,('SmartToeSleeve','SWT')).current.value
#             self.canvas.appendPoints({'x':[(t,x)]})
#         return
#     pass

# # Editor main window;
# class EvrSimSWT(esui.EsWindow):
#     def __init__(self):
#         super().__init__(title=SWT_TITLE)
#         UMR.bindIndex(self,'ESMW')
#         UMR.HEAD_DIV=estl.HeadBar(self,title=SWT_TITLE)
#         UMR.TOOL_DIV=estl.ToolDiv(self,style={'p':(0,4*yu),'s':(self.Size.x,11*yu)})
#         UMR.MAP_DIV=esgl.GLDiv(self,(0,15*yu),(50*xu,85*yu),bgc=(.5,.5,.5,1))
#         estl.AroToolbar()
#         # self.div_plot=PlotDiv(self,style={'p':(50*xu,15*yu),'s':(50*xu,85*yu)})
#         T=20
#         a=-4*np.pi/T**3
#         b=6*np.pi/T**2
#         self.sw=StereoWelding(ratio=1.5,speed=FuncX3(1/25,0,a,b))
#         self.sw.label_l.initLabel(wire=[675,400],src='app\\Welding\\vid\\blender-left.mp4',
#             wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=225)
#         self.sw.label_r.initLabel(wire=[180,400],src='app\\Welding\\vid\\blender-right.mp4',
#             wait=50,groove='gap',pool=False,clip=[5,5,0,0],radius=225)
#         self.timer=wx.Timer(self)
#         self.Bind(wx.EVT_TIMER,self.rebuildPipe,self.timer)

#         UMR.MAP_DIV.Show()
#         self.Show()
#         return

#     def lauchApp(self):
#         ESC.openSim(SWT_NAME)
#         UMR.TOOL_DIV.Show()
#         TP=UMR.TOOL_DIV.getModTab(SWT_NAME)
#         UMR.TOOL_DIV.toggleSingleMode(SWT_NAME)
#         TPY=TP.Size.y
#         # btn_run=RunSimBtn(TP,'','',style={'p':(yu,yu),'s':(9*yu,9*yu)},label='▶')
#         btn_rst=ResetMapBtn(TP,'','',style={'p':(yu,yu),'s':(8*yu,4*yu)},label='重置')
#         # txt_pip=esui.DivText(TP,style={'p':(20*yu,yu),'s':(10*yu,4*yu)},label='管内压力：')
#         # input_pip=estl.Input(TP,'',SIM_NAME,style={'p':(30*yu,yu),'s':(8*yu,4*yu)},hint='0')
#         # txt_mpa1=esui.DivText(TP,style={'p':(38*yu,yu),'s':(4*yu,4*yu)},label='MPa')
#         # txt_rdm=esui.DivText(TP,style={'p':(20*yu,6*yu),'s':(10*yu,4*yu)},label='随机波动：')
#         # input_rdm=estl.Input(TP,'',SIM_NAME,style={'p':(30*yu,6*yu),'s':(8*yu,4*yu)},hint='0')
#         # txt_mpa2=esui.DivText(TP,style={'p':(38*yu,6*yu),'s':(4*yu,4*yu)},label='MPa')

#         # bar1=estl.Bar(TP,'',SIM_NAME,style={'p':(43.5*yu,2*yu),'s':(yu/3,TPY-4*yu)})

#         # txt_ps=esui.DivText(TP,style={'p':(45*yu,yu),'s':(10*yu,4*yu)},label='启动压力：')
#         # input_ps=estl.Input(TP,'',SIM_NAME,style={'p':(55*yu,yu),'s':(8*yu,4*yu)},hint='75')
#         # txt_mpa3=esui.DivText(TP,style={'p':(63*yu,yu),'s':(4*yu,4*yu)},label='MPa')
#         # txt_pd=esui.DivText(TP,style={'p':(45*yu,6*yu),'s':(10*yu,4*yu)},label='延时压力：')
#         # input_pd=estl.Input(TP,'',SIM_NAME,style={'p':(55*yu,6*yu),'s':(8*yu,4*yu)},hint='105')
#         # txt_mpa4=esui.DivText(TP,style={'p':(63*yu,6*yu),'s':(4*yu,4*yu)},label='MPa')

#         # bar2=estl.Bar(TP,'',SIM_NAME,style={'p':(68.5*yu,2*yu),'s':(yu/3,TPY-4*yu)})

#         # txt_time=esui.DivText(TP,style={'p':(70*yu,yu),'s':(10*yu,4*yu)},label='延时时长：')
#         # input_rdm=estl.Input(TP,'',SIM_NAME,style={'p':(80*yu,yu),'s':(8*yu,4*yu)},hint='45')
#         # txt_min=esui.DivText(TP,style={'p':(88*yu,yu),'s':(4*yu,4*yu)},label='Min')

#         UMR.TOOL_DIV.toggleTab(SWT_NAME)
#         esgl.GLC.setProjMode(False)
#         esgl.GLC.lookAt([50,50,50],[0,0,0])
#         self.timer.Start(1/25)
#         return

#     def rebuildPipe(self,e):
#         pipe=ESC.getAro(1)
#         sw=self.sw
#         if sw.frame==500:
#             self.timer.Stop()
#             return
#         pts=sw.rebuildNextFrame()
#         edges,faces=sw.linkPoints(pts)
#         pipe.pts=pts
#         pipe.faces=faces
#         # pipe.pts.append(pts)
#         # pipe.faces.append(faces)
#         esgl.GLC.readMap(clear=True)

#         # self.timer.Start(1/25)
#         return
#     pass

# # Main enterance;
# ESMW=EvrSimSWT()
