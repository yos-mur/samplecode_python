# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 12:06:11 2021

@author: sukek
"""

import numpy as np
xs = np.linspace(0, 10, 100)
sins = np.sin(xs)
randoms = np.random.rand(100)

import plotly.graph_objects as go


fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=sins, name="sin"))
fig.add_trace(go.Scatter(x=xs, y=randoms, name="random"))
#  # 上と同じ結果
# fig = go.Figure(data=[
#     go.Scatter(x=xs, y=sins, name="sin"),
#     go.Scatter(x=xs, y=randoms, name="random"),
# ])

# 全体の設定
fig.update_xaxes(title="x") # X軸タイトルを指定
fig.update_yaxes(title="y") # Y軸タイトルを指定

fig.update_xaxes(range=(1,3)) # X軸の最大最小値を指定
fig.update_xaxes(rangeslider={"visible":True}) # X軸に range slider を表示（下図参照）

fig.update_yaxes(scaleanchor="x", scaleratio=1) # Y軸のスケールをX軸と同じに（plt.axis("equal")）

fig.update_layout(title="Title") # グラフタイトルを設定
fig.update_layout(font={"family":"Meiryo", "size":20}) # フォントファミリとフォントサイズを指定
fig.update_layout(showlegend=True) # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
fig.update_layout(xaxis_type="linear", yaxis_type="log") # X軸はリニアスケール、Y軸はログスケールに
fig.update_layout(width=800, height=600) # 図の高さを幅を指定
fig.update_layout(template="plotly_white") # 白背景のテーマに変更

# 系列の設定
fig.add_trace(go.Scatter(x=xs, y=sins, name="lines", mode="lines")) # 線だけ
fig.add_trace(go.Scatter(x=xs, y=sins + 1, name="markers", mode="markers")) # マーカだけ
fig.add_trace(go.Scatter(x=xs, y=sins + 2, name="lines+markers", mode="lines+markers")) # 線とマーカ

from plotly.subplots import make_subplots

# # 重ねてプロット
# fig = make_subplots(specs=[[{"secondary_y": True}]])
# fig.add_trace(go.Scatter(x=xs, y=sins, name="sin"), secondary_y=False)
# fig.add_trace(go.Scatter(x=xs, y=randoms, name="random"), secondary_y=True)

# fig.update_yaxes(title_text="y1", secondary_y=False)
# fig.update_yaxes(title_text="y2", secondary_y=True) 

# # 複数プロット
# fig = make_subplots(rows=1, cols=2)
# fig.add_trace(go.Scatter(x=xs, y=sins, name="sin"), row=1, col=1)
# fig.add_trace(go.Scatter(x=xs, y=randoms, name="random"), row=1, col=2)


# fig.show()
fig.write_html("2d.html") # 単独HTMLファイルにぐりぐりできる状態で出力
# fig.write_image("a.png") # 画像に出力（グラフ上のアイコンの"download as a png"でもOK）