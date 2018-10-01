# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

fileName = 'NodeData.csv'
rawData = pd.read_csv(fileName)

#return bus stop's nummber
def createNode() :
    return pd.Series(rawData['정류소번호'])
#return bus stop's info by station number
def busStopInfo(busstop) :
    ret = list(np.where(rawData['정류소번호'] == busstop)[0])
    return rawData.iloc[ret]

#Just For Testing
print(rawData)
print(createNode())
print(busStopInfo(25760))