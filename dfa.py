from collections import defaultdict
from disjoint_set import DisjointSet

import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Source


class DFA(object):

    def __init__(self, estados_or_nomeArquivo, terminals=None, estado_inicial=None, transicoes=None, estados_finais=None):

        if terminals is None:
            print("entrou no if do terminals none")
            self._lerArquivo(estados_or_nomeArquivo)

        else:

            assert isinstance(estados_or_nomeArquivo, list) or isinstance(estados_or_nomeArquivo, tuple)
            self.estados = estados_or_nomeArquivo

            assert isinstance(terminals, list) or isinstance(terminals, tuple)
            self.terminals = terminals

            assert isinstance(estado_inicial, str)
            self.estado_inicial = estado_inicial

            assert isinstance(transicoes, dict)
            self.transicoes = transicoes

            assert isinstance(estados_finais, list) or isinstance(estados_finais, tuple)
            self.estados_finais = estados_finais

    def _remove_estados_inalcancaveis(self):
        """
		Removes estados that are unreachable from the start state
		"""

        g = defaultdict(list)

        for k, v in self.transicoes.items():
            g[k[0]].append(v)

        # do DFS
        stack = [self.estado_inicial]

        reachable_estados = set()

        while stack:
            state = stack.pop()

            if state not in reachable_estados:
                stack += g[state]

            reachable_estados.add(state)

        self.estados = [state for state in self.estados if state in reachable_estados]

        self.estados_finais = [state for state in self.estados_finais if state in reachable_estados]

        self.transicoes = {k: v for k, v in self.transicoes.items() if k[0] in reachable_estados}

    def minizimar(self):

        self._remove_estados_inalcancaveis()

        def order_tuple(a, b):
            return (a, b) if a < b else (b, a)

        table = {}

        sorted_estados = sorted(self.estados)

        # initialize the table
        for i, item in enumerate(sorted_estados):
            for item_2 in sorted_estados[i + 1:]:
                table[(item, item_2)] = (item in self.estados_finais) != (item_2 in self.estados_finais)

        flag = True

        # table filling method
        while flag:
            flag = False

            for i, item in enumerate(sorted_estados):
                for item_2 in sorted_estados[i + 1:]:

                    if table[(item, item_2)]:
                        continue

                    # check if the estados are distinguishable
                    for w in self.terminals:
                        t1 = self.transicoes.get((item, w), None)
                        t2 = self.transicoes.get((item_2, w), None)

                        if t1 is not None and t2 is not None and t1 != t2:
                            marked = table[order_tuple(t1, t2)]
                            flag = flag or marked
                            table[(item, item_2)] = marked

                            if marked:
                                break

        d = DisjointSet(self.estados)

        # form new estados
        for k, v in table.items():
            if not v:
                d.union(k[0], k[1])

        self.estados = [str(x) for x in range(1, 1 + len(d.get()))]
        new_estados_finais = []
        self.estado_inicial = str(d.find_set(self.estado_inicial))

        for s in d.get():
            for item in s:
                if item in self.estados_finais:
                    new_estados_finais.append(str(d.find_set(item)))
                    break

        self.transicoes = {(str(d.find_set(k[0])), k[1]): str(d.find_set(v))
                            for k, v in self.transicoes.items()}

        self.estados_finais = new_estados_finais

    def imprimeInfo(self):
        """
		String representation
		"""
        num_of_state = len(self.estados)
        estado_inicial = self.estado_inicial
        num_of_final = len(self.estados_finais)

        print("Quantidade de estados:")
        print(len(self.estados))
        print("Estados:" )
        print(self.estados)
        print("Estados Iniciais")
        print(self.estado_inicial)
        print("Estados Finais")
        print(self.estados_finais)
        print("Transições:")
        print(self.transicoes)

    def _lerArquivo(self, nomeArquivo):
        """
		Load the graph from file
		"""

        with open(nomeArquivo, 'r') as f:

            try:

                lines = f.readlines()
              #  for line in lines:
              #      print(line)
                estados, terminals, estado_inicial, estados_finais = lines[:4]
               # print(estados)
                if estados:
                    self.estados = estados[:-1].split()
                    print(estados)

                else:
                    raise Exception('Invalid file format: cannot read estados')

                if terminals:
                    self.terminals = terminals[:-1].split()
                else:
                    raise Exception('Invalid file format: cannot read terminals')

                if estado_inicial:
                    self.estado_inicial = estado_inicial[:-1]
                else:
                    raise Exception('Invalid file format: cannot read start state')

                if estados_finais:
                    self.estados_finais = estados_finais[:-1].split()
                else:
                    raise Exception('Invalid file format: cannot read final estados')

                lines = lines[4:]

                self.transicoes = {}

                for line in lines:
                    current_state, terminal, next_state = line[:-1].split()
                 #   print("Estado atual: " + current_state)
                 #   print(terminal)
                 #   print("Proximo estado: " + next_state)
                    self.transicoes[(current_state, terminal)] = next_state
                #    print(self.transicoes)
            except Exception as e:
                print("ERROR: ", e)
