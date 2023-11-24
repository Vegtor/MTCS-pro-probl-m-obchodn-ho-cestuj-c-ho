import numpy as np
import networkx as nx


class Graf:
    def __init__(self, matice_vah):
        self.pocet_uzlu = len(matice_vah)
        self.matice_vah = matice_vah
        self.graf = nx.from_numpy_array(np.array(matice_vah))
        self.sousednost = []
        for i in range(0, self.pocet_uzlu):
            self.sousednost.append(list(np.where(matice_vah[i] > 0)[0]))
