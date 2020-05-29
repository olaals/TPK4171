import robotics as rb
import plucker as plkr
import numpy as np
import matplotlib.pyplot as plt
import vision as vsn
import visualize as viz

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)


a_1 = np.array([1, 0, 0])
m_1 = np.array([0, 1, 0])

p_1 = np.array([1, -1, 0])
p_2 = np.array([1, 1, 0])

viz.plotLineFrom2Points(ax, p_1, p_2)

l_2 = plkr.homgLineFrom2Points(p_1, p_2)
a_2 = l_2[0:3]
m_2 = l_2[3:6]


plt.show()