import random
import string
import os

from src import uzel as uz
from src import graf as gr
#from anytree import RenderTree
from anytree.exporter import DotExporter
import networkx as nx


class MCTS:
    def __init__(self, graf: gr.Graf):
        self.koren = uz.Uzel(None, [], 0, list(range(1, graf.pocet_uzlu)),
                             None, "0", None)
        self.graf = graf  # uložení instance třídy nadstavby NetworkX
        self.celkovy_pocet = 0
        self.C = nx.minimum_spanning_tree(self.graf.graf).size(weight="weight")
        # Konstanta - hodnota minimální kostry grafu
        #self.pocet_obr = 0


    @staticmethod
    def vrchol_list(vrchol: uz.Uzel):
        # statická metoda pro ověření, zda už jsem v listové vrstvě (v rámci MCTS konec hry)
        if (vrchol.potomci == []) and ((vrchol.nezarazene is None) or (len(vrchol.nezarazene) == 0)):
            return True
        else:
            return False

    def rozsireni_stromu(self, vrchol: uz.Uzel):
        # přidání vrcholu do stromu, vrací referenci na námi nově vytvořený vrchol
        temp = vrchol.nezarazene.pop()
        temp_mozne_cesty = vrchol.mozne_cesty.copy()
        temp_mozne_cesty.remove(temp)
        vrchol.potomci.append(
            uz.Uzel(vrchol, [], temp, temp_mozne_cesty, None, vrchol.vrchol_vykresleni.name + str(temp),
                    vrchol.vrchol_vykresleni))
        vrchol.potomci[-1].n = 1
        return vrchol.potomci[-1]

    def prepocitat_uct(self, potomci: list[uz.Uzel]):
        # přepočítání UCT skóré pro všechny vrcholy ve stromu, spouští se po každé iteraci
        for i in range(0, len(potomci)):
            potomci[i].uct_skore(self.celkovy_pocet, self.C)

    def pravidla_stromu(self, vrchol: uz.Uzel):
        # rozšiřování stromu se děje vždy po jednom vrcholu, tato funkce buďto vytvoří vrchol ze seznamu nezařazených
        # nebo provede výběr vrcholu stromu, ze kterého se tvoří cesta (v rámci obecného MCTS se jedná vrchol,
        # ze které se odehrává simulace dalších tahů hry)
        while not self.vrchol_list(vrchol):
            if (vrchol.nezarazene is None) or (len(vrchol.nezarazene) == 0):
                self.prepocitat_uct(vrchol.potomci)
                temp = vrchol.nej_uct_potomek()
                temp.akum_cesta += self.graf.matice_vah[vrchol.oznaceni][temp.oznaceni]
                # přičtení hodnoty cesty z předka do tohoto uzlu, aby při simulaci jsem měli již velikost cesty skrz strom
                temp.n += 1
                vrchol = temp
            else:
                return self.rozsireni_stromu(vrchol)
        return vrchol

    def obecne_pravidlo(self, vrchol: uz.Uzel):
        # funkce ze které probíhá simulace cesty, ta se vybírá náhodně z rovnoměrného rozdělení
        while not self.vrchol_list(vrchol):
            if len(vrchol.nezarazene) != 1:
                rand_index = random.randrange(0, len(vrchol.nezarazene) - 1)
            else:
                rand_index = 0
            # přidáná podmínka jelikož randrange funkce není definováná pro pouze jedno číslo
            temp_index = vrchol.nezarazene[rand_index]
            temp_nezarazene = vrchol.nezarazene.copy()
            temp_nezarazene.remove(temp_index)
            vrchol.cesta = uz.Uzel(vrchol, [], temp_index,
                                   temp_nezarazene.copy(), None,
                                   str(temp_index) + "n",
                                   vrchol.vrchol_vykresleni)
            vrchol = vrchol.cesta
        return vrchol

    def backup(self, v0: uz.Uzel, vl: uz.Uzel):
        # funckce pro zpětný průchod stromem a přepočítání jednotlivých vlastností vrcholů
        v0.akum_cesta += self.graf.matice_vah[vl.oznaceni][0]
        while vl != v0:
            # procházení simulace a výpočet cesty která byla náhodně vybrána
            v0.akum_cesta += self.graf.matice_vah[v0.oznaceni][vl.oznaceni]
            if str(vl.vrchol_vykresleni.name).__contains__("n"):
                vl.vrchol_vykresleni.parent = None
            vl = vl.predek
            vl.cesta = []
        while v0.predek is not None:
            # procházení stromu kde se přepočítávají hodnoty na základě simulace
            v0.cesta = []
            v0.vrchol_vykresleni.parent = v0.predek.vrchol_vykresleni
            v0.celkova_cena += v0.akum_cesta
            v0.prepocitat_prumer()
            v0.predek.akum_cesta = v0.akum_cesta
            v0.akum_cesta = 0
            v0 = v0.predek

    ############ Pomocná funkce pro vykreslení stromu do konzole ################
    #    def vykresleni(self):
    #        for pre, fill, node in RenderTree(self.koren.vrchol_vykresleni):
    #            print("%s%s" % (pre, node.name))
    #############################################################################

    def generovat_dot(self, nazev: string):
        def nodeattr(vrchol):
            temp = 'label = <<FONT POINT-SIZE ="18"> ' + str(
                vrchol.uzel.vrchol_vykresleni.name) + '</FONT><BR/> <FONT POINT-SIZE="16">v = ' + str(
                round(vrchol.uzel.prum_uzel, 2)) + '</FONT> <BR/> <FONT POINT-SIZE="16">n = ' + str(
                vrchol.uzel.n) + '</FONT>>'
            if vrchol.uzel.vrchol_vykresleni.name.__contains__("n"):
                temp += " shape=diamond"
            return temp
        DotExporter(self.koren.vrchol_vykresleni, nodeattrfunc=nodeattr).to_dotfile(nazev+".dot")

    def generovat_dot_2(self, nazev: string):
        def nodeattr(vrchol):
            if vrchol == self.koren:
                temp = 'label = <<FONT POINT-SIZE ="18"> ' + str(
                    vrchol.uzel.vrchol_vykresleni.name) + '</FONT>>'
            elif vrchol.uzel.vrchol_vykresleni.name.__contains__("n"):
                temp = temp = 'label = <<FONT POINT-SIZE ="18"> ' + str(
                vrchol.uzel.vrchol_vykresleni.name) + '</FONT>>'
                temp += " shape=diamond"
            else:
                temp = 'label = <<FONT POINT-SIZE ="18"> ' + str(
                vrchol.uzel.vrchol_vykresleni.name) + '</FONT><BR/> <FONT POINT-SIZE="16">v = ' + str(
                round(vrchol.uzel.prum_uzel, 2)) + '</FONT> <BR/> <FONT POINT-SIZE="16">n = ' + str(
                vrchol.uzel.n) + '</FONT>>'
            return temp
        DotExporter(self.koren.vrchol_vykresleni, nodeattrfunc=nodeattr).to_dotfile(nazev+".dot")

    def generovat_png(self, nazev: string):
        self.generovat_dot_2("temporary")
        os.system('cmd /c dot -Tpng -o ' + nazev + '.png -Gdpi=600 temporary.dot')
        os.remove("temporary.dot")

    def alg(self, pocet_iteraci: int):
        # samotný algoritmus, omezený na počet kroků
        for i in range(0, pocet_iteraci):
            self.celkovy_pocet += 1
            v0 = self.pravidla_stromu(self.koren)
            vl = self.obecne_pravidlo(v0)
            self.backup(v0, vl)

    def cesta(self):
        cela_cesta = "0"
        vrchol = self.koren
        while len(vrchol.potomci) != 0:
            temp = vrchol.potomci[0]
            for i in range(0, len(vrchol.potomci)):
                if temp.prum_uzel > vrchol.potomci[i].prum_uzel:
                    temp = vrchol.potomci[i]
            cela_cesta = cela_cesta + str(temp.oznaceni)
            vrchol = temp
        return cela_cesta + "0"
