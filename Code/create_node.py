# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

class GraphNode:
    fileName = 'NodeData.csv'
    rawData = pd.read_csv(fileName)
    def __init__(self, name):
        self.name = name
    #return bus stop's nummber
    def createNode() :
        return pd.Series(GraphNode.rawData['정류소번호'])
    #return bus stop's info by station number
    def busStopInfo(busstop) :
        ret = list(np.where(GraphNode.rawData['정류소번호'] == busstop)[0])
        return GraphNode.rawData.iloc[ret]

#Just For Testing
print(GraphNode.rawData)
print(GraphNode.createNode())
print(GraphNode.busStopInfo(25760))


