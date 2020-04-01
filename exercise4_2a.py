import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax, xyz_lim=[-5,5], show_axis = False)

E = np.matrix([[.0, -0.3420, .0], [-0.3420, .0, 0.9397], [.0, -0.9397, .0]])
print("Essential matrix:")
print(E)


R1, R2, t1, t2 = vsn.recoverFromEssential(E)

print("R1")
print(R1)
print("R2")
print(R2)
print("t1")
print(t1)
print("t2")
print(t2)

R = rb.roty(math.pi/2)

T = rb.makeTrans(R1,t1)
print("T")
print(T)

print("Norm of t:")
print(np.linalg.norm(t1))



cam1 = vsn.Camera(ax)
cam2 = vsn.Camera(ax, R2, t1)

s1 = np.array([0.0098, 0.1004, 1.0])
s2 = np.array([0.1920, 0.1078, 1.0])

line1 = np.concatenate((s1, np.array([.0, .0, .0])))

l2 = R2.transpose() @ s2
l2_dash = -R2.transpose() @ (np.cross(t1, s2))
print("l2")
print(l2)
print("l2 dash")
print(l2_dash)

line2 = np.hstack((l2, l2_dash))
print("line2 hstacked")
print(line2)

line2_0 = np.zeros((6))


for i in range(6):
    line2_0[i] = line2[0,i]
line2 = line2_0

print("line2")
print("  sad")
print(line2)


x_intersect = []

viz.plotHomgLine(ax, line1)
viz.plotHomgLine(ax, line2)

plt.show()