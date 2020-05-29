import addPathToModules
import robotics as rb
import visualize as viz
import vision as vsn
import proj_geo_2d as proj2d
import matplotlib.pyplot as plt
import numpy as np


print("### Task 4a ### ")

fig, ax = plt.subplots(figsize = (6,6))
plt.grid('on')
plt.axis('equal')



xs = np.array([0, 1, 2, 3, 5, 5.5])
ys = np.array([1, 2, 3.1, 4.1, 5.5, 6.4])

ax.plot(xs, ys, 'ro')

xy = np.vstack((xs, ys))
xy = np.transpose(xy)
xy = np.hstack((xy, np.ones((len(xs), 1))))
print(xy)


U, S, VT = np.linalg.svd(xy)
V = np.transpose(VT)
print(VT)

L = V[:, 2]
L = L / -L[1]
print(L)

proj2d.plot_homg_line2d(ax, L, -1, 7)


#plt.show()


# Task 4b

# candidate solution: point 1 and 2
# find inliers outliers

fig2, ax2 = plt.subplots(figsize = (6,6))
plt.grid('on')
plt.axis('equal')

x1 = xy[0, :]
x2 = xy[1, :]
print("x1")
print(x1)
print("x2")
print(x2)

cand_L = np.cross(x1, x2)
print("candidate line")
print(cand_L)

proj2d.plot_homg_line2d(ax2, cand_L, -1, 7)

nrows, ncols = xy.shape
print(nrows)

delta = 0.1
n = cand_L[0:2]
len_n = np.linalg.norm(n)
print("normal vector")
print(n)
print("len n")
print(len_n)

for points in xy:
    dist = np.abs(np.dot(cand_L, points) / len_n)
    if dist < delta:
        ax2.plot(points[0], points[1], 'go')
    else:
        ax2.plot(points[0], points[1], 'rx')
        print("outlier:")
        print(points)
    

# Task 4c

#least square solution when inliers from b are used

fig3, ax3 = plt.subplots(figsize = (6,6))
plt.grid('on')
plt.axis('equal')

print(xy)

xy_wo_out = np.vstack((xy[0:4, :], xy[5, :]))
print(xy_wo_out)

U, S, VT  = np.linalg.svd(xy_wo_out)
V = np.transpose(VT)

print("V")
print(V)

L_wo_out = V[:, 2]
L_wo_out = L_wo_out / -L_wo_out[1]
print("new_line")
print(L_wo_out)
ax3.plot(xs, ys, 'rx')
proj2d.plot_homg_line2d(ax3, L_wo_out, -1, 7)
plt.show()