import addPathToModules
import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)

p1 = np.array([4.0, 4.0, 1.0, 1.0])
p2 = np.array([3.0, 1.0, 1.0, 1.0])
p3 = np.array([2.0, 3.0, 1.0, 1.0])

viz.plotHomgPoints(ax, [p1,p2,p3])

homg_plane = rb.homgPlaneFrom3Points(p1, p2, p3)
print("homg_plane")
print(homg_plane)

viz.plotHomgPlane(ax, homg_plane, np.array([0,10]), np.array([0,10]), np.array([0,10]))



plt.show()
