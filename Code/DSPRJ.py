import GraphNode as gn
import GraphEdge as ge
import GraphTotal as gt
import csv
import networkx as nx
import matplotlib.pyplot as plt
#중간지점 리턴
def getMediumPoint(path):
    pathIter = iter(path)
    point = next(pathIter)
    weight = list()
    total = 0
    for i in pathIter:
        total = total + graph.G[point][i]['weight']
        weight.append(total)
        point = i
    goal = int(getPathWeight(path) / 2)
    goalI = 0
    for i in range(weight):
        if weight[i] > goal:
            goalI = i
            break
    left = abs(goal - weight[goalI])
    right = abs(goal - weight[goalI - 1])
    if left > right:
        return path[goalI - 1]
    return path[goalI]
#경로의 weight값 리턴
def getPathWeight(path):
    ret = 0
    pathIter = iter(path)
    point = next(pathIter)
    for i in pathIter:
        ret = ret + graph.G[point][i]['weight']
    return ret
#3점에서의 약속장소 리턴
def ThreePointShortestPath(pointList):
    mediumList = list()
    mediumList.append(nx.dijkstra_path(graph.G, pointList[1], pointList[2], weight='weight'))
    mediumList.append(nx.dijkstra_path(graph.G, pointList[0], pointList[2], weight='weight'))
    mediumList.append(nx.dijkstra_path(graph.G, pointList[0], pointList[1], weight='weight'))
    mediumPoint = list()
    for i in mediumList:
        mediumPoint.append(getMediumPoint(i))
    
    point = -1
    weight = - 1
    for i in range(3):
        tmp = nx.dijkstra_path_length(graph.G, mediumPoint[i], pointList[i], weight='weight')
        tmp = tmp + getPathWeight(mediumList[i])
        if weight == -1 or weight > tmp:
            weight = tmp
            point = i

    return getMediumPoint(nx.dijkstra_path(graph.G, mediumPoint[point], pointList[point], weight = 'weight'))


SERVICE_KEY = 'serviceKey=5CQ9SA5qWhO0FwqcEFZDa%2BBreOSi1VBRXxQcGgpQQw%2FghXivHoiMgMRzzblvToQ00GoZuqIStC%2Ft0zxZiyyYlw%3D%3D&'
APP_KEY = input("Plese type Admin Key : ")
graph = None
#In Service, this part will be represent as Server
if APP_KEY == SERVICE_KEY:
    graph = gt.GraphTotal('NodeData.csv', 'BusRoute1807.csv', 1, 500, 2330, APP_KEY)

TotalUser = input("Please type total user num : ")
TotalUser = int(TotalUser)

startNode = list()
for i in range(TotalUser):
    busStopName = input("Please type busstop Name : ")
    example = graph.nodeClass.busStopSearch(busStopName)
    print(example)
    selectNum = input("Please type number that you want to start : ")
    startNode.append(graph.nodeClass.busNumSearch(example[selectNum]))

if nx.all_pairs_node_connectivity(graph.G, startNode) is None:
    print("Nodes are not connected!")
else:
    ret = list()
    if len(startNode) == 2:
        ret.append(nx.dijkstra_path(graph.G, startNode[0], startNode[1], weight='weight'))
    else:
        #이부분 다시..
        threePointList = list()
        for i in startNode:
            tmpList = list(startNode)
            tmpList.remove(i)
            for j in tmpList:
                mediumList = list(startNode)
                mediumList.remove(j)
                for k in mediumList:
                    item = [i, j, k]
                    threePointList.append(item)
        ret = -1
        way = list()
        for i in threePointList:
            cal = ThreePointShortestPath([i[0], i[1], i[2]])
            if ret == -1 or cal < ret:
                cal = ret
                way = list(i)

graph.drawGraph()
