# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

class GraphNode:
    fileName = str()
    rawData = None
    def __init__(self, fileName):
        self.fileName = fileName
        self.rawData = pd.read_csv(fileName)
    #return bus stop's nummber
    def createNode(self) :
        return pd.Series(self.rawData['정류소번호'])
    #return bus stop's info by station number
    def busStopName(self, busstop) :
        ret = np.where(self.rawData['정류소번호'] == busstop)[0]
        return self.rawData.loc[ret]['정류소명'].item()
    #rturn bus stop's postion by station number
    def busStopPositionX(self, busstop) :
        ret = np.where(self.rawData['정류소번호'] == busstop)[0]
        return self.rawData['X좌표'].iloc[ret].item()
    def busStopPositionY(self, busstop) :
        ret = np.where(self.rawData['정류소번호'] == busstop)[0]
        return self.rawData['Y좌표'].iloc[ret].item()
    #To search exact bus stop name
    def busStopSearch(self, busstopName) :
        searchingName = self.rawData['정류소명']
        searchingNum = self.rawData['정류소번호']
        ret = list()
        retItem = tuple()
        for i in range(len(searchingName)):
            if busstopName in searchingName[i]:
                ret.append((searchingName[i], searchingNum[i]))
        return ret
    def removeNode(self, busstop) :
        findIndex = np.where(self.rawData['정류소번호'] == busstop)[0]
        if findIndex[0].size != 0:
            self.rawData = self.rawData.drop(findIndex)

