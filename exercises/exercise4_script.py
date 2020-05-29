import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)

b = np.array([0.0,1.0,0.0])

l, l_dash = np.zeros((3)), b
print(l)
print(l_dash)
#homg_line = np.concatenate((l,l_dash))
homg_plane = np.concatenate((b, np.array([0])))
print(homg_plane)

viz.plotHomgPlane(ax, homg_plane, np.array([0,3]), np.array([0,3]), np.array([0,3]))




plt.show()