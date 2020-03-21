import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy as sp
import matplotlib.colors as colors
import cv2

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


def rotx(rad):
    R = np.array([[1, 0, 0], [0, np.cos(rad), -np.sin(rad)], [0, np.sin(rad), np.cos(rad)]])
    R = np.round(R, 10)
    return R

def roty(rad):
    R = np.array([[np.cos(rad), 0, np.sin(rad)], [0, 1, 0], [-np.sin(rad), 0, np.cos(rad)]])
    R = np.round(R, 10)
    return R

def rotz(rad):
    R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0,0,1]])
    R = np.round(R,10)
    return R

def plotPoint(ax, x, y, z):
    ax.scatter(x, y, z)

def plotHomgPoint(ax, homg_point):
    ax.scatter(homg_point[0], homg_point[1], homg_point[2])

def drawPlane(ax, vstack_points, color = [0.5,0.5,0.5]):
    pol_col = Poly3DCollection([vstack_points])
    pol_col.set_color(colors.rgb2hex(color))
    pol_col.set_edgecolor('k')
    ax.add_collection3d(pol_col)

def invertTrans(T):
    R = T[0:3, 0:3]
    t = T[0:3, 3]
    R_inv = R.transpose()
    t_inv = -R_inv@t
    T_inv = np.zeros((4,4))
    T_inv[0:3,0:3] = R_inv
    T_inv[0:3, 3] = t_inv

    T_inv[3,3] = 1.0
    return T_inv

class Line:
    def __init__(self, ax, start, end):
        self.start = start
        self.end = end
        ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]])


class Frame:
    def __init__(self, ax, R, t = np.array([0,0,0]), name = "", draw_frame = True):
        self.R = R
        self.t = t
        if draw_frame: self.drawFrame(ax)
        T = np.zeros((4,4))
        T[:3,:3] = R
        T[0:3, 3] = t
        self.T = T

        ax.text(t[0], t[1], t[2], name)
        
    def drawFrame(self, ax):
        t = self.t
        R = self.R

        scale = 3

        xx = np.array([0, R[0,0]]) * scale + np.array([t[0], t[0]])
        print("xx", xx)
        xy = np.array([0, R[1,0]]) *scale+ np.array([t[1],  t[1]])
        xz = np.array([0, R[2,0]]) *scale + np.array([t[2],  t[2]])
        
        drawVector(ax, xx, xy, xz, color = 'r')

        yx = np.array([0, R[0,1]])*scale + np.array([t[0], t[0]])
        yy = np.array([0, R[1,1]])*scale + np.array([t[1], t[1]])
        yz = np.array([0, R[2,1]])*scale + np.array([t[2], t[2]])

        drawVector(ax, yx, yy, yz, color = 'g')

        zx = np.array([0, R[0,2]])*scale + np.array([t[0], t[0]])
        zy = np.array([0, R[1,2]])*scale + np.array([t[1], t[1]])
        zz = np.array([0, R[2,2]])*scale + np.array([t[2], t[2]])

        drawVector(ax, zx, zy, zz, color = 'b')

        
class Camera(Frame):
    def __init__(self, ax, R, t, intrinsic, name = ""):
        Frame.__init__(self, ax, R, t, name)
        self.K = intrinsic
        self.inv_K = self.invert_intrinsic(intrinsic)
        self.ax = ax
        self.img_width = self.K[0, 2] * 2
        self.img_height = self.K[1, 2] * 2


    def takePicture(self, lines):
        width = self.K[0, 2] * 2
        height = self.K[1, 2] * 2
        
        img = np.ones((height,width,3), np.uint8)
        img[:] = (255,255,255)

        for line in lines:
            self.drawLineToImg(line, img)
        

        

    def drawLineToImg(self, line, img):
        print(line.start)
        print(line.end)

        s = line.start
        e = line.end

        res = 1000

        xs = np.linspace(s[0], e[0], res)
        ys = np.linspace(s[1], e[1], res)
        zs = np.linspace(s[2], e[2], res)

        for i in range(res):
            point = np.array([xs[i], ys[i], zs[i], 1.0])
            (py, px) = self.getPixelOfPoint(point)
            if(py>=0 and py < self.img_height and px >= 0 and px < self.img_width):
                img[py,px,:] = 0
                
        
        cv2.imshow( "pic", img)




    def getPixelOfPoint(self, point):
        T_oc = self.T
        T_co = invertTrans(T_oc)
        #print("T_co: ", T_co)
        p_c_cp = T_co @ point
        #print("p_c_cp", p_c_cp)
        s = 1/p_c_cp[2]*p_c_cp[0:3]
        #print("s:\n", s)
        p = self.K@s
        #print("p:\n", p)

        py = int(p[1])
        px = int(p[0])
        return (py, px)

    def invert_intrinsic(self, K):
        inv_K = np.zeros((3,3))
        inv_K[0,0] = 1.0/K[0,0]
        inv_K[1,1] = 1.0/K[1,1]
        inv_K[0,2] = -K[0,2]
        inv_K[1,2] = -K[1,2]
        return inv_K

    def drawBody(self):
        ax = self.ax

        p1 = np.array([0.5, 0.5, 0.5, 1.0])
        p2 = np.array([0.5, -0.5, 0.5, 1.0])
        p3 = np.array([-0.5, -0.5, 0.5, 1.0])
        p4 = np.array([-0.5, 0.5, 0.5, 1.0])
        
        p5 = np.array([0.5, 0.5, -0.5, 1.0])
        p6 = np.array([0.5, -0.5, -0.5, 1.0])
        p7 = np.array([-0.5, -0.5, -0.5, 1.0])
        p8 = np.array([-0.5, 0.5, -0.5, 1.0])

        p9 = np.array([0.0, 0.0, 0.5, 1.0])
        p10 = np.array([0.5, 0.5, 1.0, 1.0])
        p11 = np.array([0.5, -0.5, 1.0, 1.0])
        p12 = np.array([-0.5, -0.5, 1.0, 1.0])
        p13 = np.array([-0.5, 0.5, 1.0, 1.0])


        p1_s = self.T @ p1
        p2_s = self.T @ p2
        p3_s = self.T @ p3
        p4_s = self.T @ p4

        p5_s = self.T @ p5
        p6_s = self.T @ p6
        p7_s = self.T @ p7
        p8_s = self.T @ p8

        p9_s = self.T @ p9
        p10_s = self.T @ p10
        p11_s = self.T @ p11
        p12_s = self.T @ p12
        p13_s = self.T @ p13

        top = np.vstack((p1_s[0:3], p2_s[0:3], p3_s[0:3], p4_s[0:3]))
        bot = np.vstack((p5_s[0:3], p6_s[0:3], p7_s[0:3], p8_s[0:3]))
        side1 = np.vstack((p1_s[0:3], p2_s[0:3], p6_s[0:3], p5_s[0:3]))
        side2 = np.vstack((p2_s[0:3], p3_s[0:3], p7_s[0:3], p6_s[0:3]))
        side3 = np.vstack((p3_s[0:3], p4_s[0:3], p8_s[0:3], p7_s[0:3]))
        side4 = np.vstack((p4_s[0:3], p1_s[0:3], p5_s[0:3], p8_s[0:3]))

        front = np.vstack((p10_s[0:3], p11_s[0:3], p12_s[0:3], p13_s[0:3]))
        cside1 = np.vstack((p9_s[0:3], p10_s[0:3], p11_s[0:3]))
        cside2 = np.vstack((p9_s[0:3], p11_s[0:3], p12_s[0:3]))
        cside3 = np.vstack((p9_s[0:3], p12_s[0:3], p13_s[0:3]))
        cside4 = np.vstack((p9_s[0:3], p13_s[0:3], p10_s[0:3]))
        
        drawPlane(ax, top)
        drawPlane(ax, bot)
        drawPlane(ax, side1)
        drawPlane(ax, side2)
        drawPlane(ax, side3)
        drawPlane(ax, side4)
        #drawPlane(ax, front)
        drawPlane(ax, cside1)
        drawPlane(ax, cside2)
        drawPlane(ax, cside3)
        drawPlane(ax, cside4)