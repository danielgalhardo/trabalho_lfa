from dfa import DFA

import networkx as nx
import matplotlib.pyplot as plt


filename = 'grafo'
#a_file = open(filename)
#lines = a_file.readlines()
#for line in lines:
  #  print(line)
dfa = DFA(filename)
dfa.imprimeInfo()
dfa.minizimar()
dfa.imprimeInfo()
#dfa.draw()