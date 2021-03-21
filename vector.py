# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# vec1 = np.array([4, 5 , -6])
# vec2 = np.array([-2, 3, -1])
# 
# Add = vec1 + vec2
# Minus = vec1 - vec2
# Dot = np.dot(vec1, vec2)
# Cross = np.cross(vec1, vec2)
# 
# =============================================================================


#反射ベクトルの計算

vec_n = np.array([1, 1, 1])
vec_in = np.array([1, 1, 0])

a = np.dot(-vec_in, vec_n)

vec_ref = vec_in + a * vec_n


# 面の定義

plane = np.array([[0, 0, 0],
                 [0, 10, 0],
                 [0, 10, 2],
                 [1, 0, 0], # 法線ベクトル
                 [0, 5, 0], # 反射点座標
                 [-1, 1, 0]]) # 反射ベクトル

m01 = np.array([[-10, 10, 0],
               [0, 10, 0],
               [0, 10, 2],
               [0, 1, 0],
               [-5, 10, 0],
               [-1, -1, 0]])

# 線分
lines = []
pair_x = [m01[4,0], plane[4,0]]
pair_y = [m01[4,1], plane[4,1]]
pair_z = [m01[4,2], plane[4,2]]
line = [pair_x, pair_y, pair_z]
lines.append(line)


import plotly.graph_objs as go

fig = go.Figure(data = [   
    go.Scatter3d(x=pair_x, y=pair_y, z=pair_z, name='RAY', mode='lines', line_color='blue', showlegend=True)
    ])
fig.write_html("test3D.html") # 単独HTMLファイルにぐりぐりできる状態で出力



