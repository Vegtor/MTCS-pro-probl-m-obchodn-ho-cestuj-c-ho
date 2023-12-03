import numpy as np
from src import graf as gr, mcts
from anytree.exporter import DotExporter
from graphviz import Source
import networkx as nx
import matplotlib.pyplot as plt

adjacency = np.array([[0, 2, 1, 8, 5],
                      [2, 0, 3, 4, 7],
                      [1, 3, 0, 1, 3],
                      [8, 4, 1, 0, 2],
                      [5, 7, 3, 2, 0], ])


G = nx.from_numpy_array(np.array(adjacency))

pos = nx.spring_layout(G)
nx.draw(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

g = gr.Graf(adjacency)
A = mcts.MCTS(g)
A.alg(500)


def nodeattr(vrchol):
    temp = (
            'label = <<FONT POINT-SIZE ="12"> ' + str(vrchol.name) + '</FONT><BR/> <FONT POINT-SIZE="8">v = ' + str(
        vrchol.uzel.prum_uzel) + '</FONT> <BR/> <FONT POINT-SIZE="8">n = ' + str(round(vrchol.uzel.n, 2)) + '</FONT>>')
    return temp


DotExporter(A.koren.vrchol_vykresleni, nodeattrfunc=nodeattr).to_dotfile("udo.dot")
zdroj = Source.from_file('udo.dot')
zdroj.format = 'png'
zdroj.render()
