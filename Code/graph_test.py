import networkx as nx
import matplotlib.pyplot as plt

G = nx.MultiGraph()
G.add_nodes_from(['A','B','C','E1','E2','E3','E4'])
G.add_edges_from([('A','B'), ('A','D'), ('A', 'E1'), ('B','C'), ('B','E2'), ('B','E3'), ('B', 'E4'), ('C', 'E1'), ('C', 'E2'), ('C', 'E4')])
nx.draw(G)
plt.show()