# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import GraphNode as gn
import GraphEdge as ge
import csv

def calDistance(itemA, itemB):
    ret = (nodeClass.busStopPositionX(itemB) - nodeClass.busStopPositionX(itemA))**2 + (nodeClass.busStopPositionY(itemB) - nodeClass.busStopPositionY(itemA))**2
    return ret**0.5

#Basic Settings
nodeClass = gn.GraphNode('NodeData.csv')
edgeClass = ge.GraphEdge("test.csv", 1)

rawNode = nodeClass.createNode().tolist()
Edges = edgeClass.createEdge()
countNode = {key: 0 for key in rawNode}

#Check Empty Nodes
for edge in Edges:
    i = 0
    for itemL in edge:
        countNode[int(itemL[1])] = countNode[int(itemL[1])] + 1
        if i == 0:
            countNode[int(itemL[0])] = countNode[int(itemL[0])] + 1
        i = i + 1

#Remove Empty Nodes
for key, value in countNode.items():
    if value == 0:
        rawNode.remove(key)

#Create Datas
nodeName = list()
nodeData = list()
nodePos = dict()
for item in rawNode:
    if not(item in nodeData):
        name = nodeClass.busStopName(item)
        nodeName.append(name)
        nodeData.append(item)
        nodePos[item] = (nodeClass.busStopPositionX(item), nodeClass.busStopPositionY(item))
#Labeling
labelDict = dict(zip(nodeData, nodeName))

#Weight Calculating
weightL = dict()
for edge in Edges:
    for itemL in edge:
        duplicateChk = (itemL[1], itemL[0])
        if itemL in weightL:
            weightL[itemL] = weightL[itemL] + 1
        elif duplicateChk in weightL:
            weightL[duplicateChk] = weightL[duplicateChk] + 1
        else:
            weightL[itemL] = 1
for edge in Edges:
    for itemL in edge:
        weightL[itemL] = weightL[itemL] / calDistance(int(itemL[0]), int(itemL[1]))

#Create Graph
G = nx.Graph()
for n, v in nodePos.items():
    G.add_node(int(n), pos=v)
for itemL, v in weightL.items():
    G.add_edge(int(itemL[0]), int(itemL[1]), weight=v)
d = nx.degree(G)

#draw graph with labels problem with encoding
#nx.draw(G, pos=nodePos, labels=labelDict, with_labels=True)
nx.draw(G, pos=nodePos)
plt.show()

