import module_oa.robotics as rb
import module_oa.visualize as viz
import module_oa.vision as vsn
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)

a_1 = np.array([0,0,1])
m_1 = np.array([0,0,0])
L_1 = np.concatenate((a_1, m_1))
print(L_1)
#viz.plotHomgLine(ax, L_1)
q_1 = rb.skew(a_1) @m_1
print(q_1)

a_2 = np.array([0,0,1])
m_2 = np.array([1,0,0])
L_2 = np.concatenate((a_2, m_2))
print(L_2)
#viz.plotHomgLine(ax, L_2)
q_2 = rb.skew(a_2) @m_2
print(q_2)
viz.drawVector(ax, xx=[0,q_2[0]], yy=[0, q_2[1]], zz = [0, q_2[2]])


a_3 = np.array([1,0,0])
m_3 = np.array([0,0,-1])
L_3 = np.concatenate((a_3, m_3))
#viz.plotHomgLine(ax, L_3)
q_3 = rb.skew(a_3) @m_3




plt.show()