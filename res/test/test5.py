import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI)    # or p.DIRECT for non-graphical version
src=pybullet_data.getDataPath()
print(src)
p.setAdditionalSearchPath(src)  # optionally

p.setGravity(0, 0, -10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0, 0, 1]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)

useRealTimeSimulation = 0

if (useRealTimeSimulation):
  p.setRealTimeSimulation(1)

while 1:
  if (useRealTimeSimulation):
    p.setGravity(0, 0, -10)
    sleep(0.01)  # Time in seconds.
  else:
    p.stepSimulation()
