# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import GraphNode as gn
import GraphEdge as ge
import csv
import json

class GraphTotal:
    G = nx.Graph()
    color_map = list()
    nodePos = dict()
    labelDict = dict()
    nodeData = list()
    def calDistance(self, itemA, itemB):
        ret = (self.nodeClass.busStopPositionX(itemB) - self.nodeClass.busStopPositionX(itemA))**2 + (self.nodeClass.busStopPositionY(itemB) - self.nodeClass.busStopPositionY(itemA))**2
        return ret**0.5

    def __init__(self, nodeFile, edgeFile, dayType, startTime, endTime, APP_KEY=None):
        self.dayType = dayType
        self.startTime = startTime
        self.endTime = endTime
        self.nodeClass = gn.GraphNode(nodeFile)
        self.edgeClass = ge.GraphEdge(edgeFile, dayType, startTime, endTime)

        rawNode = self.nodeClass.createNode().tolist()
        self.Edges = self.edgeClass.createEdge(APP_KEY)
        countNode = {key: 0 for key in rawNode}

        #Check Empty Nodes
        for busId, busPath in self.Edges.items():
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
                self.nodeClass.removeNode(key)

        #Create Datas
        nodeName = list()
        for item in rawNode:
            if not(item in self.nodeData):
                name = self.nodeClass.busStopName(item)
                nodeName.append(name)
                self.nodeData.append(item)
                self.nodePos[item] = (self.nodeClass.busStopPositionX(item), self.nodeClass.busStopPositionY(item))
                self.color_map.append('red')
        #Labeling
        self.labelDict = dict(zip(self.nodeData, nodeName))

        #Weight Calculating for count how many buspath passing
        weightL = dict()
        for busId, busPath in self.Edges.items():
            for itemL in busPath:
                if itemL in weightL:
                    weightL[itemL] = weightL[itemL] + self.edgeClass.busPathTime(str(busId))
                else:
                    if int(itemL[0]) in countNode and int(itemL[1]) in countNode:
                        weightL[itemL] = self.edgeClass.busPathTime(str(busId))
        #Weight Calculating for distance
        for busId, edge in self.Edges.items():
            for itemL in edge:
                if itemL in weightL:
                    weightL[itemL] = self.calDistance(int(itemL[0]), int(itemL[1])) / weightL[itemL]

        #Create Graph
        for n, v in self.nodePos.items():
            self.G.add_node(int(n), pos=v)
        for itemL, v in weightL.items():
            self.G.add_edge(int(itemL[0]), int(itemL[1]), weight=v)

    #draw graph with labels Coloring and positioning
    def drawGraph(self):
        nx.draw(self.G, node_color = self.color_map, pos=self.nodePos)
        plt.show()
    def checkListInPath(self, path):
        retId = -1
        ret = dict()
        print(path)
        for busId, busPath in self.Edges.items():
            chk = len(path)
            i = 0
            for itemL in busPath:
                if int(itemL[1]) in path:
                    chk = chk - 1
                if i == 0:
                    if int(itemL[0]) in path:
                        chk = chk - 1
                    i = 1
            if chk <= 0 :
                retId = int(busId)
        if retId == -1:
            ret[-1] = list()
        else:
            busRoute = self.Edges[str(retId)]
            answerRoute = list()
            i = 0
            start = 0
            chk = len(path)
            for itemL in busRoute:
                if int(itemL[1]) in path:
                    if chk <= 0 :
                        break
                    elif start == 0:
                        start = 1
                        answerRoute.append(itemL[1])
                        chk = chk - 1
                    elif start == 1:
                        answerRoute.append(itemL[1])
                        chk = chk - 1
                if i == 0:
                    if int(itemL[0]) in path:
                        start = 1
                        answerRoute.append(itemL[0])
                        chk = chk - 1
            ret[retId] = list(answerRoute)
        return ret