import os
os.environ['PATH']+=';'+os.getcwd()+'\\lib'
import assimp

scene=assimp.load('moment.obj')
print(1)
