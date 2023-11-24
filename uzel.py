import copy
import math
import string

from anytree import Node

class Uzel:
    def __init__(self, predek: 'Uzel', potomci: list['Uzel'], oznaceni: int, nezarazene: list[int], cesta: 'Uzel', nazev_vykresleni: string, predek_vykresleni: Node):
        self.prum_uzel = 0
        self.n = 0
        self.predek = predek
        self.potomci = potomci
        self.uct = 0
        self.oznaceni = oznaceni
        self.akum_cesta = 0
        self.nezarazene = nezarazene
        self.cesta = cesta
        self.celkova_cena = 0
        self.vrchol_vykresleni = Node(nazev_vykresleni, parent=predek_vykresleni)
        self.mozne_cesty = nezarazene.copy()

    def uct_skore(self, celkovy_pocet: int, vaha_c: float):
        self.uct = self.prum_uzel - 2 * vaha_c * math.sqrt(2 * math.log(celkovy_pocet) / self.n)

    def nej_uct_potomek(self):
        index = 0
        for i in range(0,len(self.potomci)):
            if self.potomci[i].uct < self.potomci[index].uct:
                index = i
        return self.potomci[index]

    def prepocitat_prumer(self):
        self.prum_uzel = self.celkova_cena/self.n
