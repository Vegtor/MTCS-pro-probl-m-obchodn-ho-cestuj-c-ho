import random
from src import uzel as uz
from src import graf as gr
from anytree import RenderTree
import numpy as np


class MCTS:
    def __init__(self, graf: gr.Graf):
        self.koren = uz.Uzel(None, [], 0, list(range(1, graf.pocet_uzlu)), None, "0", None)
        self.graf = graf
        self.celkovy_pocet = 0
        self.C = np.sqrt(2)

    @staticmethod
    def vrchol_list(vrchol: uz.Uzel):
        if (vrchol.potomci == []) and ((vrchol.nezarazene is None) or (len(vrchol.nezarazene) == 0)):
            return True
        else:
            return False

    def rozsireni_stromu(self, vrchol: uz.Uzel):
        temp: int = vrchol.nezarazene.pop()
        temp_mozne_cesty = vrchol.mozne_cesty.copy()
        temp_mozne_cesty.remove(temp)
        vrchol.potomci.append(
            uz.Uzel(vrchol, [], temp, temp_mozne_cesty, None, vrchol.vrchol_vykresleni.name + str(temp),
                    vrchol.vrchol_vykresleni))
        vrchol.potomci[-1].n = 1
        return vrchol.potomci[-1]

    def pravidla_stromu(self, vrchol: uz.Uzel):
        while not self.vrchol_list(vrchol):
            if (vrchol.nezarazene is None) or (len(vrchol.nezarazene) == 0):
                temp = vrchol.nej_uct_potomek()
                temp.akum_cesta += self.graf.matice_vah[vrchol.oznaceni][temp.oznaceni]
                temp.n += 1
                vrchol = temp
            else:
                return self.rozsireni_stromu(vrchol)
        return vrchol

    def obecne_pravidlo(self, vrchol: uz.Uzel):
        while not self.vrchol_list(vrchol):
            if len(vrchol.nezarazene) != 1:
                rand_index = random.randrange(0, len(vrchol.nezarazene) - 1)
            else:
                rand_index = 0
            temp_index = vrchol.nezarazene[rand_index]
            temp_nezarazene = vrchol.nezarazene.copy()
            temp_nezarazene.remove(temp_index)
            vrchol.cesta = uz.Uzel(vrchol, [], temp_index, temp_nezarazene.copy(), None,
                                   str(temp_index) + "n", vrchol.vrchol_vykresleni)
            vrchol = vrchol.cesta
        return vrchol

    def backup(self, v0: uz.Uzel, vl: uz.Uzel):
        v0.akum_cesta += self.graf.matice_vah[vl.oznaceni][0]
        while v0.predek is not None:
            while vl != v0:
                v0.akum_cesta += self.graf.matice_vah[v0.oznaceni][vl.oznaceni]
                if str(vl.vrchol_vykresleni.name).__contains__("n"):
                    vl.vrchol_vykresleni.parent = None
                vl = vl.predek
                vl.cesta = []
            v0.cesta = []
            v0.vrchol_vykresleni.parent = v0.predek.vrchol_vykresleni
            v0.celkova_cena += v0.akum_cesta
            v0.prepocitat_prumer()
            v0.uct_skore(self.celkovy_pocet, self.C)
            v0.predek.akum_cesta = v0.akum_cesta
            v0 = v0.predek

    def vykresleni(self):
        for pre, fill, node in RenderTree(self.koren.vrchol_vykresleni):
            print("%s%s" % (pre, node.name))

    def alg(self, pocet_iteraci: int):
        for i in range(0, pocet_iteraci):
            self.celkovy_pocet += 1
            v0 = self.pravidla_stromu(self.koren)
            vl = self.obecne_pravidlo(v0)
            #print("Pred Backup")
            #self.vykresleni()
            self.backup(v0, vl)
            #print("Po Backup")
            #self.vykresleni()
