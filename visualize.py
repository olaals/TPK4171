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


def defaultAxisSetup(ax, xyz_lim = [0,10]):
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(xyz_lim)
    ax.set_ylim(xyz_lim)
    ax.set_zlim(xyz_lim)
    ax.view_init(elev=40, azim=40) 

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

def plotHomgPoint(ax, homg_point):
    ax.scatter(homg_point[0], homg_point[1], homg_point[2])

def drawPlane(ax, vstack_points, color = [0.5,0.5,0.5]):
    pol_col = Poly3DCollection([vstack_points])
    pol_col.set_color(colors.rgb2hex(color))
    pol_col.set_edgecolor('k')
    ax.add_collection3d(pol_col)