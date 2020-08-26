# libs;
from core import ESC
from core import esui
from core import estool
# Mod-in import;
from mod.AroCore.tool import RunSimBtn,ResetMapBtn
from .aro import Mcu,ToeSleeve,Pipe,Pistol
# MOD INDEX
MOD_NAME='STS'
MOD_VER='0.0.1'
MOD_SETTING={}
ARO_INDEX=['Mcu','ToeSleeve','Pipe','Pistol']
ACP_INDEX=[]
TOOL_INDEX=['btn_run']
MODEL_INDEX=[]
# Tool preset;
# Tool variable name need to add to TOOL_INDEX;
yu=esui.YU
TP=esui.TOOL_PLC.getModTab('STS')
TPY=TP.Size.y
btn_run=RunSimBtn('btn_run',TP,(yu,yu),(9*yu,9*yu),'▶')
btn_rst=ResetMapBtn('btn_rst',TP,(11*yu,yu),(8*yu,4*yu),'重置')
txt_pip=estool.TextTool('txt_pip',TP,(20*yu,yu),(10*yu,4*yu),'管内压力：')
input_pip=estool.InputTool('',TP,(30*yu,yu),(8*yu,4*yu),'0')
txt_mpa1=estool.TextTool('txt_mpa1',TP,(38*yu,yu),(4*yu,4*yu),'MPa')
txt_rdm=estool.TextTool('txt_rdm',TP,(20*yu,6*yu),(10*yu,4*yu),'随机波动：')
input_rdm=estool.InputTool('',TP,(30*yu,6*yu),(8*yu,4*yu),'0')
txt_mpa2=estool.TextTool('txt_mpa2',TP,(38*yu,6*yu),(4*yu,4*yu),'MPa')

bar1=estool.BarTool('',TP,(43.5*yu,2*yu),(yu/3,TPY-4*yu))

txt_ps=estool.TextTool('txt_ps',TP,(45*yu,yu),(10*yu,4*yu),'启动压力：')
input_ps=estool.InputTool('',TP,(55*yu,yu),(8*yu,4*yu),'75')
txt_mpa3=estool.TextTool('txt_mpa3',TP,(63*yu,yu),(4*yu,4*yu),'MPa')
txt_pd=estool.TextTool('txt_pd',TP,(45*yu,6*yu),(10*yu,4*yu),'延时压力：')
input_pd=estool.InputTool('',TP,(55*yu,6*yu),(8*yu,4*yu),'105')
txt_mpa4=estool.TextTool('txt_mpa4',TP,(63*yu,6*yu),(4*yu,4*yu),'MPa')

bar2=estool.BarTool('',TP,(68.5*yu,2*yu),(yu/3,TPY-4*yu))

txt_time=estool.TextTool('txt_time',TP,(70*yu,yu),(10*yu,4*yu),'延时时长：')
input_rdm=estool.InputTool('',TP,(80*yu,yu),(8*yu,4*yu),'45')
txt_min=estool.TextTool('txt_min',TP,(88*yu,yu),(4*yu,4*yu),'Min')

pass
