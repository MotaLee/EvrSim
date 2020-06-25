# -*- coding: UTF-8 -*-
# system libs;
import sys
import os
# import core as SC

# Outer libs;
import OpenGL.GL as gl
# from OpenGL.GL import *
# import OpenGL.GLUT as glut
# os.environ['LIBRARY']='./lib/glfw3.dll'
import glfw
# import numpy as np
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt

# system vars;
EVRSIMVER = '0.0.2'
WIN_WIDTH = 800
WIN_HEIGHT = 600
WIN_TITLE='EvrSim '+EVRSIMVER

# glfw GUI;
def framebuffer_size_callback(window, width, height):
    return

def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window,1)
    if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
        pass
    return

def main():
    glfw.init()
    # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    # glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT,gl.GL_TRUE)
    glfw.window_hint(glfw.RESIZABLE,gl.GL_FALSE)
    glfw.window_hint(glfw.DECORATED,gl.GL_FALSE)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    ESW=glfw.create_window(800,600, WIN_TITLE,None,None)  # EvrSim Window;
    if ESW == 0: glfw.terminate()
    glfw.maximize_window(ESW)
    glfw.make_context_current(ESW)

    # glfw.set_framebuffer_size_callback(ESW,framebuffer_size_callback)

    while not glfw.window_should_close(ESW):
        processInput(ESW)
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glViewport(0, 200, 200, 200)
        # glEnable(gl.GL_TEXTURE_2D)

        gl.glBegin(gl.GL_TRIANGLES)                # 开始绘制三角形（z轴负半区）
    
        gl.glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
        gl.glVertex3f(-0.5, -0.366, -0.5)       # 设置三角形顶点
        gl.glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
        gl.glVertex3f(0.5, -0.366, -0.5)        # 设置三角形顶点
        gl.glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
        gl.glVertex3f(0.0, 0.5, -0.5)           # 设置三角形顶点
        
        gl.glEnd()
        glfw.swap_buffers(ESW)
        glfw.poll_events()
    return

# Main enterance;
main()

# # system initilization;
# print('EvrSim Console '+EVRSIMVER)

# # system main enterance;
# while 1:
#     com = input('EvrSim>>')
#     exec(com)

# matplotlib test;
# x = [1,3,5,7]
# y = [4,9,6,8]
# plt.plot(x,y)
# plt.show()
