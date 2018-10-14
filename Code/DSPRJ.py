import GraphNode as gn
import GraphEdge as ge
import GraphTotal as gt
import csv
import networkx as nx
import matplotlib.pyplot as plt

SERVICE_KEY = 'serviceKey=5CQ9SA5qWhO0FwqcEFZDa%2BBreOSi1VBRXxQcGgpQQw%2FghXivHoiMgMRzzblvToQ00GoZuqIStC%2Ft0zxZiyyYlw%3D%3D&'
APP_KEY = input("Plese type Admin Key : ")
graph = None
#In Service, this part will be represent as Server
if APP_KEY == SERVICE_KEY:
    graph = gt.GraphTotal('NodeData.csv', 'BusRoute1807.csv', 1, 500, 2330, APP_KEY)

TotalUser = input("Please type total user num : ")
while not(TotalUser.isdigit()):
    TotalUser = input("Please type total user num as integer type : ")
while int(TotalUser) > 20:
    TotalUser = input("Please type total user num below 20 : ")
while int(TotalUser) < 1:
    TotalUser = input("Please type total user num above 1 : ")
TotalUser = int(TotalUser)

startNode = list()
for i in range(TotalUser):
    busStopName = input("Please type busstop Name : ")
    while not(type(busstopName) is str):
            busstopName = input("Please type busstop Name as string : ")
    example = graph.nodeClass.busStopSearch(busStopName)
    print(example)
    selectNum = input("Please type number that you want to start : ")
    while not(type(selectNum) is int):
        selectNum = input("Please type number as int : ")
    while selectNum < len(example):
        selectNum = input("Please type number that can be selected : ")
    startNode.append(graph.nodeClass.busNumSearch(example[selectNum]))

print(startNode)

userList = list()
graph.drawGraph()
