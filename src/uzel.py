import copy
import math
import string

from anytree import NodeMixin, Node


class Uzel_vykresleni(NodeMixin):
    # vlastní rozšíření pro knihovnu AnyTree, pouze pro grafické znázornění
    def __init__(self, name, uzel, parent=None, children=None):
        super(Uzel_vykresleni, self).__init__()
        self.name = name
        # jménem pro vykreslení je cesta do tohoto uzlu, např. 0251 = cesta z kořene přes vrcholy 2 a 5 do 1
        self.uzel = uzel
        self.parent = parent
        if children:
            self.children = children


class Uzel:
    # třída pro vrchol stromu
    def __init__(self, predek: 'Uzel', potomci: list['Uzel'], oznaceni: int, nezarazene: list[int], cesta: 'Uzel',
                 nazev_vykresleni: string, predek_vykresleni: Node):
        self.prum_uzel = 0
        # průměrná cena celé cesty (celého okruho z počátku a zpátky)
        self.n = 0
        # počet průchodů algoritmu tímto uzlem
        self.predek = predek
        # reference na předka
        self.potomci = potomci
        # list referencí na potomky
        self.uct = 0
        # UCT skóre
        self.oznaceni = oznaceni
        # název vrcholu, definováné jako čísla, kde kořen je 0,
        self.akum_cesta = 0
        # akumulace cesty v jedné iteraci, respektive její cena
        self.nezarazene = nezarazene
        # používané při simulaci, list vrcholů, které může simulace "vygenerovat" (náhodně vybrat a vytvořit)
        self.cesta = cesta
        # atribut, do které ukládáme kroky simulace
        self.celkova_cena = 0
        # nasčítáná cesta přes všechny iterace, ve kterých se daný uzel nacházel, pro výpočet průměru
        self.vrchol_vykresleni = Uzel_vykresleni(nazev_vykresleni, self, parent=predek_vykresleni)
        # atribut pro vykreslení
        self.mozne_cesty = nezarazene.copy()
        # list všech vrcholů ze stavového prostoru (vrcholy které jsem ještě neprošli a nejsou potomkem/předkem daného uzlu)

    def uct_skore(self, celkovy_pocet: int, vaha_c: float):
        # výpočet UCT skóre
        self.uct = self.prum_uzel - 2 * vaha_c * math.sqrt(2 * math.log(celkovy_pocet) / self.n)

    def nej_uct_potomek(self):
        # vrátí potomka s nejmenší hodnotou UCT
        index = 0
        for i in range(0, len(self.potomci)):
            if self.potomci[i].uct < self.potomci[index].uct:
                index = i
        return self.potomci[index]

    def prepocitat_prumer(self):
        self.prum_uzel = self.celkova_cena / self.n
