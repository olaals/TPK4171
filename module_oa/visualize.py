import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy as sp
import matplotlib.colors as colors
import cv2
import robotics as rb



class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def defaultAxisSetup(ax, xyz_lim = [0,10], show_axis = True):
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(xyz_lim)
    ax.set_ylim(xyz_lim)
    ax.set_zlim(xyz_lim)
    ax.view_init(elev=40, azim=40) 
    
    if show_axis:
        vec_len = (xyz_lim[1] - xyz_lim[0])/3.0
        drawVector(ax, xx = [0, vec_len], color = 'r')
        drawVector(ax, yy = [0, vec_len], color = 'g')
        drawVector(ax, zz = [0, vec_len], color = 'b')

        ax.text(1.1*vec_len,0,0, "x", color='r')
        ax.text(0, 1.1*vec_len, 0, "y", color = 'g')
        ax.text(0,0,1.1*vec_len, "z", color= 'b')    


def drawVector(ax, xx = [0,0], yy = [0,0], zz = [0,0], color = "black", ms = 15, lw = 2):
    vec = Arrow3D(xx, yy, 
                zz, mutation_scale=ms,
                lw=lw, arrowstyle="-|>", color=color)
    ax.add_artist(vec)




def plotPoint(ax, x, y, z):
    ax.scatter(x, y, z)

def plotHomgPoint(ax, homg_point, color = 'r'):
    ax.scatter(homg_point[0], homg_point[1], homg_point[2], c=color)

def plotHomgPoints(ax, homg_point_list, color = 'r'):
    for point in homg_point_list:
        plotHomgPoint(ax, point, color)

def plotPlaneFrom4Points(ax, p1, p2, p3, p4, color = 'b', alpha = 0.4):
    point_list = [p1, p2, p3, p4]
    print(point_list)
    """
    sorted = False
    while not sorted:
        sorted = True
        for i in range(3):
            edge = (point_list[i+1][i] - point_list[i][i])*(point_list[i+1][i+1] + point_list[i][i+1])
            print(edge)
            if(edge < 0):
                sorted = False
                temp = point_list[i]
                point_list[i] = point_list[i+1]
                point_list[i+1] = temp
    print(point_list)
    temp = point_list[1]
    point_list[1] = point_list[0]
    point_list[0] = temp
    """

    vstacked = np.vstack((point_list[0][0:3], point_list[1][0:3], point_list[2][0:3], point_list[3][0:3]))

    print(vstacked)
    pol_col = Poly3DCollection([vstacked])
    pol_col.set_color(color)
    pol_col.set_edgecolor(color)
    pol_col.set_alpha(alpha)
    ax.add_collection3d(pol_col)



def plotHomgPlane(ax, homg_plane, x_range, y_range, z_range = np.array([-10, 10]), alpha = 0.4, color = 'b'):
    A = np.round(homg_plane[0], 3)
    B = np.round(homg_plane[1], 3)
    C = np.round(homg_plane[2], 3)
    u4 = homg_plane[3]


    if C != 0.0:
        x_range = np.linspace(x_range[0], x_range[1], 2)
        y_range = np.linspace(y_range[0], y_range[1], 2)
        x, y = np.meshgrid(x_range, y_range)
        z = -1.0/C*(A*x + B*y + u4)
    elif B != 0:
        x_range = np.linspace(x_range[0], x_range[1], 2)
        z_range = np.linspace(z_range[0], z_range[1], 2)
        x, z = np.meshgrid(x_range, z_range)
        y = -1.0/B*(A*x + C*z + u4)
    elif A != 0:
        y_range = np.linspace(y_range[0], y_range[1], 2)
        z_range = np.linspace(z_range[0], z_range[1], 2)
        y, z = np.meshgrid(y_range, z_range)
        x = -1.0/A*(B*y + C*z + u4)

    
    ax.plot_surface(x,y,z, alpha = alpha, color = color)

def plotLineFrom2Points(ax, p1, p2):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]])

def plotHomgLine(ax, homg_line):
    #vector from origo to line
    print(homg_line)


    l = homg_line[0:3]
    l_dash = homg_line[3:6]

    print(l)
    print(l_dash)

    q = np.cross(l, l_dash) / np.linalg.norm(l)**2
    print(q)

    lambda1 = 5.0
    lambda2 = -5.0

    p1 = q + lambda1*l
    p2 = q + lambda2*l

    plotLineFrom2Points(ax, p1, p2)


def drawPlane(ax, vstack_points, color = [0.5,0.5,0.5]):
    pol_col = Poly3DCollection([vstack_points])
    pol_col.set_color(colors.rgb2hex(color))
    pol_col.set_edgecolor('k')
    ax.add_collection3d(pol_col)
