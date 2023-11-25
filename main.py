import numpy as np
from src import graf as gr, mcts
from src import uzel as uz
from anytree.exporter import DotExporter
from graphviz import Source, render

adjacency = np.array([[0, 2, 4, 1],
                      [2, 0, 3, 4],
                      [4, 3, 0, 1],
                      [1, 4, 1, 0],])

g = gr.Graf(adjacency)
a = 5

A = mcts.MCTS(g)
A.alg(500)
s = 5


def nodeattr(vrchol):
    temp = (
            'label = <<FONT POINT-SIZE ="12"> ' + str(vrchol.name) + '</FONT><BR/> <FONT POINT-SIZE="8">v = ' + str(vrchol.uzel.prum_uzel) + '</FONT> <BR/> <FONT POINT-SIZE="8">n = ' + str(vrchol.uzel.n) + '</FONT>>')
    return temp


DotExporter(A.koren.vrchol_vykresleni, nodeattrfunc=nodeattr).to_dotfile("udo.dot")
zdroj = Source.from_file('udo.dot')
zdroj.format = 'png'
zdroj.render()
