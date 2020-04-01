import visualize as viz
import matplotlib.pyplot as plt
import numpy as np
import robotics as rb

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)

p1 = np.array([0.0,0.0,0.0, 1.0])
p2 = np.array([0.0,2.0,0.0, 1.0])

viz.plotHomgPoint(ax, p1)
viz.plotHomgPoint(ax, p2)

homg_line = rb.homgLineFrom2Points(p1, p2)

viz.plotHomgLine(ax, homg_line)

plt.show()