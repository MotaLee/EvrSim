import os
os.environ['PATH']+=';'+os.getcwd()+'\\res\\lib'
import assimp_py
# import pyassimp
process_flags = (
    assimp_py.Process_Triangulate | assimp_py.Process_CalcTangentSpace
)
# scene=assimp.load('res/raw/bl20201013.fbx')
scene=assimp_py.ImportFile('mod/Dynamics/res/moment.blend', process_flags)
print(1)
