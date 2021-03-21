# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:05:59 2021

@author: sukek
"""

# import plotly.offline as po
import plotly.graph_objs as go
import numpy as np

# 格子状に座標を生成
grid = np.mgrid[0:10, 0:20]
grid_x = grid[0].flatten()
grid_y = grid[1].flatten()
grid_z = grid_x + grid_y
points = np.array(list(zip(grid_x, grid_y, grid_z)))

# プロットのためにxyzごとのリストに分解
xs = points[:,0]
ys = points[:,1]
zs = points[:,2]

# traceを作成
trace = go.Scatter3d(
    x=xs,
    y=ys,
    z=zs,
    mode='markers',
    marker=dict(
        color='rgb(100,100,200)',
        size=5,
        opacity=0.8
    )
)
# layoutを作成
layout = go.Layout(
    # デフォルトでは描画領域が狭いのでmarginを0に
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    # xyz軸のスケールを統一
    scene=dict(aspectmode='cube'),
)
# traceとlayoutからfigureを作成
fig = go.Figure(data=[trace], layout=layout)
# プロット
# po.iplot(fig, filename='sample-verts')
fig.write_html("sample-verts.html") # 単独HTMLファイルにぐりぐりできる状態で出力