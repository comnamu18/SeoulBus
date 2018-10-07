# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import GraphNode as gn
import GraphEdge as ge

#Create Graph
G = nx.MultiGraph()
Node = gn.GraphNode('NodeData.csv')
Edge = ge.GraphEdge("BusRoute1807.csv", 1)
G.add_nodes_from(Node.createNode)
G.add_edges_from(Edge.createEdge)

nx.draw(G)
plt.show()