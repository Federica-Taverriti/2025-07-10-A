import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._products = []
        self._idMapP = {}
        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self, lun, start, end):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]
        self._ricorsione(parziale, lun, end)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, lun, end):
        #condizione di ottimalità e di terminazione: posso salvare una soluzione solo se lunga lun
        if len(parziale) == lun:
            if parziale[-1] == end and self._getScore(parziale)>self._bestScore:
                self._bestScore = self._getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun, end)
                parziale.pop()

    def _getScore(self, parziale):
        #somma dei pesi
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score




    def buildGraph(self, cat, date1, date2):
        self._graph.clear()
        self._products = DAO.getProductByCategory(cat)
        for p in self._products:
            self._idMapP[p.product_id] = p

        self._graph.add_nodes_from(self._products)

        allEdges = DAO.getAllEdges(cat, date1, date2, self._idMapP)
        for e in allEdges:
            self._graph.add_edge(e.p1, e.p2, weight= e.peso)

    def getNodiPiuProfittevoli(self):
        #per ogni nodo associare pesi archi uscenti ed entranti
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"] #aggiungo peso archi uscenti
            for e in self._graph.in_edges(n, data=True):
                score -= e[2]["weight"] #sottraggo peso archi entranti
            listNodesPesata.append((n, score))

        listNodesPesata.sort(key=lambda x: x[1], reverse=True)

        return listNodesPesata[:5]

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategorie()

    def getAllNodes(self):
        return list(self._graph.nodes)