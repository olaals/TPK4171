import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import utils
import math
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

utils.defaultAxisSetup(ax)

R = utils.roty(math.pi/2.0) @ utils.rotz(-math.pi/2.0)
print(R)


line1 = utils.Line(ax, [6,3,0], [6,3,2])
line2 = utils.Line(ax, [6,3,2], [7,4,2])
line3 = utils.Line(ax, [7,4,2], [7,4,0])
line4 = utils.Line(ax, [7,4,0], [6,3,0])


print(R)

t = np.array([1,3,1])

p1 = np.array([6.0, 4.0, 2.0, 1.0])
utils.plotHomgPoint(ax, p1)

intrinsic = np.array([[1500, 0, 640], [0, 1500, 512], [0,0,1]])

cam1 = utils.Camera(ax, R, t, intrinsic,name = "c")
cam1.drawBody()
cam1.takePicture([line1, line2, line3, line4])

#ax.scatter(2,2,2)

plt.show()

