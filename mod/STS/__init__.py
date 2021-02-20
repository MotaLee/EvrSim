# libs;
from core import ESC,esui,estl
# Mod-in import;
from mod.AroCore.atl import RunSimBtn,ResetMapBtn
from .aro import Mcu,ToeSleeve,Pipe,Pistol
# MOD INDEX
MOD_NAME='STS'
MOD_VER='0.0.2'
MOD_PERF={}
ARO_INDEX=['Mcu','ToeSleeve','Pipe','Pistol']
ACP_INDEX=[]
MODEL_INDEX=[]
# Tool preset;
yu=esui.YU
TP=esui.TOOL_PLC.getTab('STS')
TPY=TP.Size.y
btn_run=RunSimBtn('btn_run',TP,(yu,yu),(9*yu,9*yu),'▶')
btn_rst=ResetMapBtn('btn_rst',TP,(11*yu,yu),(8*yu,4*yu),'重置')
txt_pip=estl.TextTool('txt_pip',TP,(20*yu,yu),(10*yu,4*yu),'管内压力：')
input_pip=estl.InputTool('',TP,(30*yu,yu),(8*yu,4*yu),'0')
txt_mpa1=estl.TextTool('txt_mpa1',TP,(38*yu,yu),(4*yu,4*yu),'MPa')
txt_rdm=estl.TextTool('txt_rdm',TP,(20*yu,6*yu),(10*yu,4*yu),'随机波动：')
input_rdm=estl.InputTool('',TP,(30*yu,6*yu),(8*yu,4*yu),'0')
txt_mpa2=estl.TextTool('txt_mpa2',TP,(38*yu,6*yu),(4*yu,4*yu),'MPa')

bar1=estl.BarTool('',TP,(43.5*yu,2*yu),(yu/3,TPY-4*yu))

txt_ps=estl.TextTool('txt_ps',TP,(45*yu,yu),(10*yu,4*yu),'启动压力：')
input_ps=estl.InputTool('',TP,(55*yu,yu),(8*yu,4*yu),'75')
txt_mpa3=estl.TextTool('txt_mpa3',TP,(63*yu,yu),(4*yu,4*yu),'MPa')
txt_pd=estl.TextTool('txt_pd',TP,(45*yu,6*yu),(10*yu,4*yu),'延时压力：')
input_pd=estl.InputTool('',TP,(55*yu,6*yu),(8*yu,4*yu),'105')
txt_mpa4=estl.TextTool('txt_mpa4',TP,(63*yu,6*yu),(4*yu,4*yu),'MPa')

bar2=estl.BarTool('',TP,(68.5*yu,2*yu),(yu/3,TPY-4*yu))

txt_time=estl.TextTool('txt_time',TP,(70*yu,yu),(10*yu,4*yu),'延时时长：')
input_rdm=estl.InputTool('',TP,(80*yu,yu),(8*yu,4*yu),'45')
txt_min=estl.TextTool('txt_min',TP,(88*yu,yu),(4*yu,4*yu),'Min')

pass
