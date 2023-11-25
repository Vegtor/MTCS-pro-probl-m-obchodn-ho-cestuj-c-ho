import numpy as np
from src import graf as gr, mcts
from src import uzel as uz
from anytree.exporter import DotExporter

adjacency = np.array([[0, 2, 4, 1, 5],
                      [2, 0, 3, 4, 3],
                      [4, 3, 0, 1, 9],
                      [1, 4, 1, 0, 8],
                      [5, 3, 9, 8, 0]])

g = gr.Graf(adjacency)
a = 5

A = mcts.MCTS(g)
A.alg(500)
s = 5


def nodenamefunc(vrchol):
    temp = (
        '<FONT POINT-SIZE ="12"> {vrchol.name}</FONT><BR/> <FONT POINT-SIZE="8">v = {vrchol.uzel.prum_uzel}</FONT> <BR/> <FONT POINT-SIZE="8">v = {vrchol.uzel.n}</FONT>')
    return temp


for line in DotExporter(A.koren.vrchol_vykresleni, graph="graph", nodenamefunc=nodenamefunc):
    print(line)
