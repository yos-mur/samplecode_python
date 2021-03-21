# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:47:19 2021

@author: sukek
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d


# classレンズ　機能　始点と入射ベクトルを入れた際に出射点と屈折ベクトルを出力

# レンズ情報（2枚張り合わせまでを想定）
# 境界面の数（最大3）、半径（最大3）、センタ位置（最大3）、屈折率（外、レンズ1、レンズ2） 交点計算は最低2回
# 入出力はリストとし、内部はndarrayで計算

class Lens:
    def __init__(self, point_start, vec_in, r0, r1, point_sc0, point_sc1, n0, n1, 
                 num_planes=1, r2=None, point_sc2=[None,None,None], n2=None):
        # 変数初期化
               
        # レンズ情報
        self.r = [r0, r1, r2] #曲面の半径　入射面, 出射面, 出射面2（張り合わせ用）
        self.point_sc = np.stack((np.array(point_sc0), np.array(point_sc1), np.array(point_sc2, dtype = float)), 
                                 axis = 0,) 
        #半径中心の座標　入射面, 出射面, 出射面2（張り合わせ用）
        self.n = [n0, n1, n2] #屈折率　環境, レンズ1, レンズ2（張り合わせ用）
        self.num_planes = num_planes # 出口面の枚数

        # 屈折用計算情報
        # self.point_start = np.array(point_start, dtype = float)
        # self.vec_in = np.array(vec_in, dtype = float)

        self.point_start_calc = np.full((3,3), None, dtype = float)
        self.point_start_calc[0] = np.array(point_start )
        self.vec_in_calc = np.full((3,3), None, dtype = float)
        self.vec_in_calc[0] = np.array(vec_in )
        
        self.point_ref = np.full((3,3), None, dtype = float)
        self.vec_n = np.full((3,3), None, dtype = float)
        self.vec_ref = np.full((3,3), None, dtype = float)
        self.num = 0
        self.point_out = []
        self.vec_out = []

    # 関数　球との交点を求める
    # def calc_crosspoint_s(point_start, vec_in, point_sp_c, r):
    def calc_crosspoint_s(self):
        point_s = self.point_start_calc[self.num]
        vec_in = self.vec_in_calc[self.num]
        point_sp_c = self.point_sc[self.num]
        r = self.r[self.num]
        
        point_s_t = point_s - point_sp_c
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
    
        self.point_ref[self.num] = point
        self.vec_n[self.num] = vec_n
        # return(point, vec_n)
    

    # 屈折計算
    # def calc_refracted(vec_in, vec_n, n1, n2, d):
    def calc_refracted(self):
        vec_in = self.vec_in_calc[self.num]
        vec_n = self.vec_n[self.num]
        
        n1 = self.n[self.num]
        if ((self.num_planes == 1) and (self.num == 1)):
            n2 = self.n[0]
        elif (self.num_planes == 2) and (self.num == 2):
            n2 = self.n[0]
        else:
            n2 = self.n[self.num + 1] 
        
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
        vec_ref = vec_ref / np.linalg.norm(vec_ref, ord=2)
            
        self.vec_ref[self.num] = vec_ref
        # return vec_ref

    def calc_output(self):
        # num_planes の値で繰り返し
        for self.num in range(self.num_planes + 1):
            self.calc_crosspoint_s()
            self.calc_refracted()
            
            if self.num < 2:
                self.point_start_calc[self.num + 1] = self.point_ref[self.num]
                self.vec_in_calc[self.num + 1] = self.vec_ref[self.num]
        
        self.point_out = self.point_ref[self.num_planes].tolist()
        self.vec_out = self.vec_ref[self.num_planes].tolist()

        
# 関数　描画用
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



# 始点ベクトル情報
point_start = [-2, -1, 0.0]
vec_in = [1,0,0]
# 球情報
# point_sp_c = np.array([1,0,0])
# r = 2.0
# n1 = 1.0
# n2 = 1.6

lens1 = Lens(point_start=point_start, vec_in=vec_in, 
             r0=2, r1=2, point_sc0=[1,0,0], point_sc1=[1,0,0], n0=1.0, n1=1.5)

# lens1.point_start = np.array([-2, -1, 0.0])
# lens1.vec_in = np.array([1,0,0])
lens1.calc_output()

print('lens1.point_out =', lens1.point_out)
print('lens1.vec_out =', lens1.vec_out)

point_start = lens1.point_start_calc[1]
point = np.array(lens1.point_out)
vec_ref = np.array(lens1.vec_out)
draw(lens1.point_sc[1], lens1.r[1], point_start, point, vec_ref)