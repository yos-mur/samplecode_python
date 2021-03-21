# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:05:59 2021

@author: sukek
"""

# import plotly.offline as po
import plotly.graph_objs as go
import numpy as np

# 円柱状に座標を生成
grid = np.mgrid[0:16, 0:3]
grid_ang = grid[0].flatten()
grid_z = grid[1].flatten()
grid_x = 2*np.cos(2*grid_ang*np.pi/16)
grid_y = 2*np.sin(2*grid_ang*np.pi/16)
points = np.array(list(zip(grid_x, grid_y, grid_z)))

# プロットのためにxyzごとにリストに分解
xs = points[:,0]
ys = points[:,1]
zs = points[:,2]

data = []
# マーカー
data.append(go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode='markers',
        marker=dict(
            color='rgb(100,100,200)',
            size=2,
            opacity=0.8
        )
    ))
# 線分
for x, y, z in points:
    data.append(go.Scatter3d(
            x=[x, x+x/2],
            y=[y, y+y/2],
            z=[z, z],
            mode='lines',
            marker=dict(
                color='rgb(100,100,200)',
                size=5,
                opacity=0.8
            )
        ))
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    # xyz軸のスケールを統一
    scene=dict(aspectmode='cube'),
    showlegend=False,
)
fig = go.Figure(data=data, layout=layout)
# po.iplot(fig, filename='sample-vecs')
fig.write_html("sample-vecs.html") # 単独HTMLファイルにぐりぐりできる状態で出力