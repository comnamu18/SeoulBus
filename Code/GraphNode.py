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
    def busStopInfo(self, busstop) :
        ret = list(np.where(self.rawData['정류소번호'] == busstop)[0])
        return self.rawData.iloc[ret]



