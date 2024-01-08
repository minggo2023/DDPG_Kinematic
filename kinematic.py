import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import time 
import pandas as pd 
from speed_polar import pole

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
x = 0  # 船的初始坐标
y = 25
psi =  np.pi / 3  # 当前船头朝向
# U = 5      # 当前船速

yb1 = 50
yb2 = 20

# 标志位
flag = deque(maxlen=2)
flag.append(0)
flag.append(0)

# 控制器参数
kup = 0.1
kpsi = 0.1

x_real = [x]
y_real = [y] 
io = 0 
i = 0 

psi_d = []

action_l = []
r = []
heading_angle = []
dd = []

speed = []

psiz_l = []

def sgn(number):

    if number >= 0:
        y = 1
    else:
        y = -1
    return y 

for i in range(1000):
    
    """
    增添代码 
    模型此处出错
    """
    if alpha_tw < 0 :  
        psi_tw2 = alpha_tw + np.pi
    else:
        psi_tw2 = alpha_tw - np.pi
    
    psiz = psi - psi_tw2

    if psiz > np.pi:
        psiz = psiz - 2 * np.pi
    elif psiz < - np.pi:
        psiz = psiz+ 2 * np.pi

    U = pole(psiz)

    # if U < 1:
    #     U = 1

    # speed.append(U)
    # psiz_l.append(psiz * 180 / np.pi)

    ye = np.cos( np.pi / 4) * (y - 2.5) - np.sin(np.pi / 4 ) * (x - 2.5)

    action = - np.arctan(ye / (0.9 * L))

    psid = np.pi / 4 + action      # 理想航向角 LOS

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


    if x >= 100:
        break

    heading_angle.append(psi)

    

    x_real.append(x)
    y_real.append(y)
# f = open("Los_slope.txt","w")
# f.writelines(str(x_real)+'\n')
# f.writelines(str(y_real))
# f.close()
t = np.arange(0, 1000, 1)
print(ye)
plt.plot([2.5, 100], [2.5, 100],'--')
plt.plot(y_real, x_real)
# plt.xlabel("x")
# plt.ylabel("y")
plt.show()