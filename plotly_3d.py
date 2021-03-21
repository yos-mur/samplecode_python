# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 14:23:20 2021

@author: sukek
"""

# import plotly.offline as po
import plotly.graph_objs as go
import sys, os, json
# from docopt import docopt

# モデルクラス
class Model:
    def __init__(self, nodes, beams):
        self.Nodes = nodes
        self.Beams = beams

# 節点クラス
class Node:
    def __init__(self, name, x, y, z):
        self.Name = name
        self.X = float(x)
        self.Y = float(y)
        self.Z = float(z)

# 部材クラス
class Beam:
    def __init__(self, name, node_i, node_j):
        self.Name = name
        self.INode = node_i
        self.JNode = node_j

# モデルを生成する
def create_model(path):
    nodes = []
    beams = []
    dic_nodes= {}
    with open(path) as f:
        df = json.load(f)
    # 節点
    for item in df['Node']:
        node = Node(item['Name'], item['X'], item['Y'], item['Z'])
        nodes.append(node)
        dic_nodes[node.Name] = node
    # 部材
    for item in df['Beam']:
        name = item['Name']
        node_i = dic_nodes[item['INode']]
        node_j = dic_nodes[item['JNode']]
        beam = Beam(item['Name'], node_i, node_j)
        beams.append(beam)
    return Model(nodes, beams)

# 部材の描画用オブジェクトを取得する
def get_trace_beam(beam):
    pair_x = [beam.INode.X, beam.JNode.X]
    pair_y = [beam.INode.Y, beam.JNode.Y]
    pair_z = [beam.INode.Z, beam.JNode.Z]
    return go.Scatter3d(x=pair_x, y=pair_y, z=pair_z, name=beam.Name, mode='lines', line_color='blue', showlegend=True)

# 節点の描画用オブジェクトを取得する
def get_trace_node(node):
    x = node.X
    y = node.Y
    z = node.Z
    return go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', marker_color='blue', marker_size=2, name=node.Name, showlegend=True)

# 描画用オブジェクトを取得する
def get_traces(model):
    traces = []
    # Beam
    for beam in model.Beams:
        traces.append(get_trace_beam(beam))
    # Node
    for node in model.Nodes:
        traces.append(get_trace_node(node))
    return traces

# モデルを描画する
def view_model(model, out_file_name):
    traces = get_traces(model)
    fig = go.Figure(data=traces)
    fig['layout']['scene'].update(go.layout.Scene(aspectmode='data'))
    # po.plot(fig, filename=out_file_name, auto_open=True)
    fig.write_html(out_file_name + "_3d.html") # 単独HTMLファイルにぐりぐりできる状態で出力

# メイン
def main(path, out_file_name):
    model = create_model(path)
    view_model(model, out_file_name)

if __name__ == "__main__":
    # __doc__ = """
    # Usage:
    #     model_viewer.py 
    #     model_viewer.py -h | --help
    # Options:
    #     -h --help  show this help message and exit
    # """
    # args = docopt(__doc__)
    # model_data_file_path = args[' ']
    model_data_file_path = 'sample.json'
    out_file_name = os.path.splitext(os.path.basename(model_data_file_path))[0]
    main(model_data_file_path, out_file_name)