# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 23:41:44 2021

@author: sukek
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d

# 始点ベクトル情報
point_start = np.array([-2, -1.5, 0.0])
vec_in = np.array([1,0,0])
    
# 球情報
point_sp_c = np.array([1,0,0])
r = 2.0
n1 = 1.0
n2 = 1.6

# 関数　球との交点を求める
def calc_crosspoint_s(point_start, vec_in, point_sp_c, r):

    point_s = point_start
    point_s_t = point_start - point_sp_c
    
    point_s_t_norm = np.linalg.norm(point_s_t, ord=2) 
    
    vec_in = vec_in / np.linalg.norm(vec_in, ord=2) # vec_in normalize
    vec_in_norm = 1.0
    
    a = (vec_in_norm)**2
    b = 2 * np.dot(point_s_t, vec_in)
    c = (point_s_t_norm)**2 - r**2
    
    d = b**2 - 4 * a * c
    
    if abs(d) < 1.0E-12:
       d = 0.0
       
    if d < 0:
        print('線と球は交差しない: point = point_s　として処理')
        # point_sp_0 = None
        vec_n = None
        point = point_s
    else:
        t1 = (-b + (d)**0.5) / (2 * a)
        t2 = (-b - (d)**0.5) / (2 * a)
        if (t1 > 0) and (t2 > 0): # どちらも正の場合
            if t1 < t2:
                t = t1
            else:
                t = t2
        elif(t1 < 0): # t1が負の場合
            t = t2
        elif(t2 <= 0): # t2が負/0の場合
            t = t1
        else:
            print('不明なエラー：t value')
            
        point_sp_0 = point_s_t + t * vec_in
        point = point_sp_0 + point_sp_c
        vec_n = point_sp_0 / r # 交点における球の法線（大きさ1）
        # if d == 0:
        #     print('球の接線')
        # elif (t1 > 0) and (t2 > 0):
        #     print('始点は球の外側')
        # else:
        #     print('始点は球の内側')
        # print(point)

    return(point, vec_n)


# 屈折計算
# def calc_refracted(vec_in, vec_n, n1, n2, d):
def calc_refracted(vec_in, vec_n, n1, n2):
    ratio_n = n1 / n2    
    # if (vec_n is None) or (d == 0):
    if (vec_n is None):
        print('交点なし: vec_ref = vec_in　として処理')
        vec_ref = vec_in
    else:
        vin_dot_vn = np.dot(vec_in, vec_n)
        
        if vin_dot_vn > 0: # 法線判定
            vec_n = -vec_n
            vin_dot_vn = np.dot(vec_in, vec_n)
        c_ref = 1 - ratio_n**2 * ( 1 - vin_dot_vn**2)
        
        if abs(c_ref) < 1.0E-12:
            c_ref = 0.0
        
        # 全反射判定
        # if (d <= 0):
        #     print('接線')
        #     vec_ref = vec_in
        if (c_ref) < 0:
            # print('反射')
            vec_ref = vec_in - 2 * vin_dot_vn * vec_n #　全反射の場合
        else:
            # print('屈折')
            vec_ref = ratio_n * (vec_in - vin_dot_vn * vec_n) - c_ref**0.5 * vec_n # 屈折
        
    return vec_ref
    # return vec_ref, c_ref

result = calc_crosspoint_s(point_start, vec_in, point_sp_c, r)
point = result[0]
vec_n = result[1]
# d = result[2]

# result_1 = calc_refracted(vec_in, vec_n, n1, n2, d)
result_1 = calc_refracted(vec_in, vec_n, n1, n2)
vec_ref = result_1
# vec_ref = result_1[0]
# c_ref = result_1[1]



# 描画用
def draw(point_sp_c, r, point_start, point, vec_ref):
    color_sp = 'skyblue'
    color_line = 'r'
    range_x = (-5, 5)
    range_y = range_x
    range_z = range_x
    
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = point_sp_c[0] + r * np.outer(np.cos(u), np.sin(v))
    y = point_sp_c[1] + r * np.outer(np.sin(u), np.sin(v))
    z = point_sp_c[2] + r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # line
    p_s = point_start
    p_r = point
    p_e = p_r + vec_ref * 5
    lines = np.stack((p_s,p_r,p_e), 0).T
    # line_x = lines[0]
    # line_y = lines[1]
    # line_z = lines[2]
    
    fig = plt.figure(figsize=plt.figaspect(1.))
    
    # 3D
    ax = fig.add_subplot(222, projection='3d')
    ax.set_box_aspect((1,1,1))
    ax.set(xlabel='X', ylabel='Y', zlabel='Z')
    ax.set(xlim = range_x, ylim = range_x, zlim = range_z)
    # ax.set_zlim(-5, 5)
    
    # 球の描画
    # Plot the surface
    # ax.plot_surface(x, y, z, color=color_sp,rcount=100, ccount=100, antialiased=False)
    ax.plot_wireframe(x, y, z, color=color_sp, linewidth=0.5)
    # 線の描画
    line= art3d.Line3D(lines[0], lines[1], lines[2], color=color_line)
    ax.add_line(line)
    ax.plot(p_s[0], p_s[1], p_s[2], color=color_line, marker='o')
    ax.plot(p_r[0], p_r[1], p_r[2], color=color_line, marker='x')
    
    
    # 2D
    class Fig2d:
        def __init__(self, num_subplot, label0, label1, range0, range1, sph0, sph1, i, j):
            self.num_subplot = num_subplot
            self.label0 = label0
            self.label1 = label1
            self.range0 = range0
            self.range1 = range1
            self.sph0 = sph0
            self.sph1 = sph1
            self.i = i
            self.j = j
    
    f2d = [Fig2d(221, 'X', 'Y', range_x, range_y, sph0=x, sph1=y, i=0, j=1),
           Fig2d(223, 'X', 'Z', range_x, range_z, x, z, 0, 2),
           Fig2d(224, 'Y', 'Z', range_y, range_z, y, z, 1, 2)]
    
    for num in range(len(f2d)):
        ax = fig.add_subplot(f2d[num].num_subplot)
        ax.grid(True)
        ax.set(xlabel = f2d[num].label0, ylabel = f2d[num].label1)
        ax.set(xlim = f2d[num].range0, ylim = f2d[num].range1)
        ax.plot(f2d[num].sph0, f2d[num].sph1, color=color_sp, linewidth=0.5) #球
        ax.plot(lines[f2d[num].i], lines[f2d[num].j], color=color_line) #光線
        ax.plot(p_s[f2d[num].i], p_s[f2d[num].j], color=color_line, marker='o') #始点
        ax.plot(p_r[f2d[num].i], p_r[f2d[num].j], color=color_line, marker='x') #屈折点
    
    
    # # x-y
    # ax = fig.add_subplot(221)
    # ax.grid(True)
    # ax.set(xlabel='x', ylabel='y')
    # ax.set(xlim = xrange, ylim = yrange)
    # ax.plot(x, y, color=color_sp, linewidth=0.5)
    # ax.plot(line_x, line_y, color=color_line)
    # ax.plot(p_s[0], p_s[1], color=color_line, marker='o')
    # ax.plot(p_r[0], p_r[1], color=color_line, marker='x')
    
    # # x-z
    # ax = fig.add_subplot(223)
    # ax.grid(True)
    # ax.set(xlabel='x', ylabel='z')
    # ax.set(xlim = xrange, ylim = yrange)
    # ax.plot(x, z, color=color_sp, linewidth=0.5)
    # ax.plot(line_x, line_z, color=color_line)
    # ax.plot(p_s[0], p_s[2], color=color_line, marker='o')
    # ax.plot(p_r[0], p_r[2], color=color_line, marker='x')
    
    # # y-z
    # ax = fig.add_subplot(224)
    # ax.grid(True)
    # ax.set(xlabel='y', ylabel='z')
    # ax.set(xlim = xrange, ylim = yrange)
    # ax.plot(y, z, color=color_sp, linewidth=0.5)
    # ax.plot(line_y, line_z, color=color_line)
    # ax.plot(p_s[1], p_s[2], color=color_line, marker='o')
    # ax.plot(p_r[1], p_r[2], color=color_line, marker='x')
    
    # plt.savefig("3d_ball.jpg",dpi=120)
    plt.show()

draw(point_sp_c, r, point_start, point, vec_ref)