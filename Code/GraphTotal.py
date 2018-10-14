# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import GraphNode as gn
import GraphEdge as ge
import csv
import json

class GraphTotal:
    G = nx.Graph()
    nodePos = dict()
    labelDict = dict()
    def calDistance(self, itemA, itemB):
        ret = (self.nodeClass.busStopPositionX(itemB) - self.nodeClass.busStopPositionX(itemA))**2 + (self.nodeClass.busStopPositionY(itemB) - self.nodeClass.busStopPositionY(itemA))**2
        return ret**0.5

    def __init__(self, nodeFile, edgeFile, dayType, startTime, endTime, APP_KEY):
        self.dayType = dayType
        self.startTime = startTime
        self.endTime = endTime
        self.nodeClass = gn.GraphNode(nodeFile)
        self.edgeClass = ge.GraphEdge(edgeFile, dayType, startTime, endTime)

        rawNode = self.nodeClass.createNode().tolist()
        Edges = self.edgeClass.createEdge(APP_KEY)
        countNode = {key: 0 for key in rawNode}

        #Check Empty Nodes
        for busId, busPath in Edges:
            i = 0
            for itemL in busPath:
                if int(itemL[1]) in countNode:
                    countNode[int(itemL[1])] = 1
                if i == 0:
                    if int(itemL[0]) in countNode:
                        countNode[int(itemL[0])] = 1
                    i = 1

        #Remove Empty Nodes
        for key, value in countNode.items():
            if value == 0:
                rawNode.remove(key)

        #Create Datas
        nodeName = list()
        nodeData = list()
        for item in rawNode:
            if not(item in nodeData):
                name = self.nodeClass.busStopName(item)
                nodeName.append(name)
                nodeData.append(item)
                self.nodePos[item] = (self.nodeClass.busStopPositionX(item), self.nodeClass.busStopPositionY(item))
        #Labeling
        self.labelDict = dict(zip(nodeData, nodeName))

        #Weight Calculating for count how many buspath passing
        weightL = dict()
        for busId, busPath in Edges:
            for itemL in busPath:
                if itemL in weightL:
                    weightL[itemL] = weightL[itemL] + self.edgeClass.busPathTime(busId)
                else:
                    if int(itemL[0]) in countNode and int(itemL[1]) in countNode:
                        weightL[itemL] = self.edgeClass.busPathTime(busId)
        #Weight Calculating for distance
        for edge in Edges:
            for itemL in edge:
                if itemL in weightL:
                    weightL[itemL] = weightL[itemL] / self.calDistance(int(itemL[0]), int(itemL[1]))

        #Create Graph
        for n, v in self.nodePos.items():
            self.G.add_node(int(n), pos=v)
        for itemL, v in weightL.items():
            self.G.add_edge(int(itemL[0]), int(itemL[1]), weight=v)
        d = nx.degree(self.G)
        print(d)

    #draw graph with labels problem with encoding
    #nx.draw(G, pos=nodePos, labels=labelDict, with_labels=True)
    def drawGraph(self):
        nx.draw(self.G, pos=self.nodePos)
        plt.show()



