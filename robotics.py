import numpy as np

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