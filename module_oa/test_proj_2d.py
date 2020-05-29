import numpy as np
import matplotlib.pyplot as plt
import proj_geo_2d as proj2d

fig = plt.figure(figsize=(6,6))
plt.grid('on')
plt.axis('equal')
ax = fig.add_subplot(111)



l = np.array([3,-1,1])

proj2d.plot_homg_line2d(ax, l, -10, 10)

plt.show()