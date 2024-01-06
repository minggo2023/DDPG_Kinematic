import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import time 
import pandas as pd 

# 真风速度 初始条件
Tw = 0.5 
Tm = 0.05
alpha_tw = - np.pi  # degree
dtw = 0 
dtw_max = (1/9) * np.pi 

# 帆船相关参数
L = 12  # （m）
Delta = 2 * L
t = 0    # current time 
ts = 0.1 # sample time 
x = -20  # 船的初始坐标
y = 0
psi =  np.pi / 4  # 当前船头朝向
U = 5      # 当前船速

yb1 = 50
yb2 = 20

# 标志位
flag = deque(maxlen=2)
flag.append(0)
flag.append(0)

# 控制器参数
kup = 0.1
kpsi = 0.1

def sgn(number):

    if number >= 0:
        y = 1
    else:
        y = -1
    return y 

x_real = [x]
y_real = [y] 
io = 0 
i = 0 

psi_d = []

action_l = []
r = []
heading_angle = []
dd = []

for i in range(2000):

    ye = np.cos(0) * (y - 2.5) - np.sin(0) * (x - 2.5)

    action = - np.arctan(ye / Delta)

    psid = 0 + action      # 理想航向角 LOS

    dd.append(psid)

    action_l.append(psid * 180 / np.pi)

    if psid > np.pi:
        psid = psid - 2 * np.pi
    elif psid < -np.pi:
        psid = psid + 2 * np.pi
        
    psi_d.append(psid)

    if i == 0:
        dpsid = 0
    elif abs(psi_d[-1] - psi_d[-2]) >= np.pi:
        dpsid = dpsid 
    else:
        dpsid = (psi_d[-1] - psi_d[-2]) / ts
    
    psic = psid - psi        # 误差

    if psic > np.pi:
        psic = psic - 2 * np.pi
    elif psic < - np.pi:
        psic = psic + 2 * np.pi
    
    alphar  = dpsid + kpsi * psic  

    r.append(alphar)

    #    运动学方程

    x = x + ts * U * np.cos(psi)  # x 坐标
    y = y + ts * U * np.sin(psi)  # y 坐标
    psi = psi + ts * alphar            # 朝向角

    heading_angle.append(psi)

    

    x_real.append(x)
    y_real.append(y)

t = np.arange(0, 2000, 1)
# plt.plot(x_real, y_real)
plt.plot(x_real, y_real)
plt.show()