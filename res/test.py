import os,sys,ctypes,math,json
sys.path.append(os.getcwd()+'\\res\\lib')
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
os.add_dll_directory(os.getcwd()+'\\res\\lib')
import _pyassimp as ai
scene=ai.load('mod/Game/res/zhong.fbx')
for child in scene.rootnode.children:

    i=child.transformation
    print(i)
