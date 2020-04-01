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
import visualize as viz

def recoverFromEssential(E):
    W = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [.0, .0, 1.0]])
    print("W")
    print(W)
    Z = np.array([[.0, 1.0, .0], [-1.0, .0, .0], [.0, .0, .0]])
    print("Z")
    print(Z)

    U, S, VT = np.linalg.svd(E)
    print("U")
    print(U)
    print("S")
    S = np.diag(S)
    print(S)
    print("VT")
    print(VT)

    R1 = U @ W @ VT
    R2 = U @ np.transpose(W) @ VT

    if np.linalg.det(R1) < 0:
        R1 = -R1
    
    if np.linalg.det(R2) < 0:
        R2 = -R2

    print("R1")
    print(R1)

    print("R2")
    print(R2)

    tc = U @ Z @ np.transpose(U)
    print("tc")
    print(tc)

    t1 = np.array([tc[2,1], tc[0,2], tc[1,0]])
    print("t1")
    print(t1)
    t2 = -t1

    return R1, R2, t1, t2

class Line:
    def __init__(self, ax, start, end, color = np.array([255,0,0])):
        self.color = color
        self.start = start
        self.end = end
        color = color/255.0
        ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color = color)

class Frame2D:
    def __init__(self, ax, R, t):
        pass

    def drawFrame(self, ax):
        pass



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
        
        viz.drawVector(ax, xx, xy, xz, color = 'r')

        yx = np.array([0, R[0,1]])*scale + np.array([t[0], t[0]])
        yy = np.array([0, R[1,1]])*scale + np.array([t[1], t[1]])
        yz = np.array([0, R[2,1]])*scale + np.array([t[2], t[2]])

        viz.drawVector(ax, yx, yy, yz, color = 'g')

        zx = np.array([0, R[0,2]])*scale + np.array([t[0], t[0]])
        zy = np.array([0, R[1,2]])*scale + np.array([t[1], t[1]])
        zz = np.array([0, R[2,2]])*scale + np.array([t[2], t[2]])

        viz.drawVector(ax, zx, zy, zz, color = 'b')

        
class Camera(Frame):
    def __init__(self, ax, R = np.diag(np.ones((3))), t = np.zeros((3)), intrinsic = np.ones((3,3)), name = ""):
        Frame.__init__(self, ax, R, t, name)
        self.K = intrinsic
        self.inv_K = self.invert_intrinsic(intrinsic)
        self.ax = ax
        self.img_width = self.K[0, 2] * 2
        self.img_height = self.K[1, 2] * 2
        self.drawBody()

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
                img[py,px] = line.color

                
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow( "pic", img)




    def getPixelOfPoint(self, point):
        T_oc = self.T
        T_co = rb.invertTrans(T_oc)
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

    def showNormalizedImagePlane(self, ax):
        p1 = self.T @ np.array([1.0, 1.0, 1.0, 1.0])
        p2 = self.T @ np.array([1.0, -1.0, 1.0, 1.0])
        p3 = self.T @ np.array([-1.0, -1.0, 1.0, 1.0])
        p4 = self.T @ np.array([-1.0, 1.0, 1.0, 1.0])

        viz.plotPlaneFrom4Points(ax, p1, p2, p3, p4, color = 'r')

    

    def drawBody(self):
        ax = self.ax

        p1 = np.array([0.5, 0.5, 0.0, 1.0])
        p2 = np.array([0.5, -0.5, 0.0, 1.0])
        p3 = np.array([-0.5, -0.5, 0.0, 1.0])
        p4 = np.array([-0.5, 0.5, 0.0, 1.0])
        
        p5 = np.array([0.5, 0.5, -1.0, 1.0])
        p6 = np.array([0.5, -0.5, -1.0, 1.0])
        p7 = np.array([-0.5, -0.5, -1.0, 1.0])
        p8 = np.array([-0.5, 0.5, -1.0, 1.0])

        p9 = np.array([0.0, 0.0, 0.0, 1.0])
        p10 = np.array([0.5, 0.5, 0.5, 1.0])
        p11 = np.array([0.5, -0.5, 0.5, 1.0])
        p12 = np.array([-0.5, -0.5, 0.5, 1.0])
        p13 = np.array([-0.5, 0.5, 0.5, 1.0])


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
        
        viz.drawPlane(ax, top)
        viz.drawPlane(ax, bot)
        viz.drawPlane(ax, side1)
        viz.drawPlane(ax, side2)
        viz.drawPlane(ax, side3)
        viz.drawPlane(ax, side4)
        #drawPlane(ax, front)
        viz.drawPlane(ax, cside1)
        viz.drawPlane(ax, cside2)
        viz.drawPlane(ax, cside3)
        viz.drawPlane(ax, cside4)