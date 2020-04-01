import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


viz.defaultAxisSetup(ax)


p1 = np.array([2.0, 4.0, 2.0, 1.0])
p2 = np.array([2.0, 1.0, 2.0, 1.0])
p4 = np.array([2.0, 4.0, 1.0, 1.0])
p3 = np.array([2.0, 1.0, 1.0, 1.0])


viz.plotPlaneFrom4Points(ax, p1, p2, p3, p4)

plt.show()