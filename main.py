import numpy as np
from src import graf as gr, mcts
import networkx as nx
import matplotlib.pyplot as plt

adjacency = np.array([[0, 2, 1, 8],
                      [2, 0, 3, 4],
                      [1, 3, 0, 1],
                      [8, 4, 1, 0], ])

G = nx.from_numpy_array(np.array(adjacency))

pos = nx.spring_layout(G)
nx.draw(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

g = gr.Graf(adjacency)
A = mcts.MCTS(g)
A.alg(500)
