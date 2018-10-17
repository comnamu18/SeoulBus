import GraphNode as gn
import GraphEdge as ge
import GraphTotal as gt
import csv
import networkx as nx
from networkx.algorithms.connectivity import local_node_connectivity
import matplotlib.pyplot as plt
import itertools

#중간지점 리턴
def getMediumPoint(G, path):
    pathIter = iter(path)
    point = next(pathIter)
    weight = list()
    total = 0
    for i in pathIter:
        total = total + G[point][i]['weight']
        weight.append(total)
        point = i
    goal = int(getPathWeight(G, path) / 2)
    goalI = 0
    for i in range(len(weight)): 
        if weight[i] > goal:
            goalI = i
            break
    left = abs(goal - weight[goalI])
    right = abs(goal - weight[goalI - 1])
    if left > right:
        return path[goalI - 1]
    return path[goalI]
#경로의 weight값 리턴
def getPathWeight(G, path):
    ret = 0
    pathIter = iter(path)
    point = next(pathIter)
    for i in pathIter:
        ret = ret + G[int(point)][i]['weight']
        point = i
    return ret
#3점에서의 약속장소 리턴
def ThreePointShortestPath(G, pointList):
    mediumList = list()
    mediumList.append(nx.dijkstra_path(G, pointList[1], pointList[2], weight='weight'))
    mediumList.append(nx.dijkstra_path(G, pointList[0], pointList[2], weight='weight'))
    mediumList.append(nx.dijkstra_path(G, pointList[0], pointList[1], weight='weight'))
    mediumPoint = list()
    for i in mediumList:
        mediumPoint.append(getMediumPoint(G, i))
    point = -1
    weight = - 1
    for i in range(3):
        tmp = nx.dijkstra_path_length(G, mediumPoint[i], pointList[i], weight='weight')
        tmp = tmp + getPathWeight(G, mediumList[i])
        if weight == -1 or weight > tmp:
            weight = tmp
            point = i

    return getMediumPoint(G, nx.dijkstra_path(graph.G, mediumPoint[point], pointList[point], weight = 'weight'))
def chcekConnectivity(G, startNode):
    ret = None
    for u, v in itertools.combinations(startNode, 2):
        k = local_node_connectivity(G, u, v)
        if k == 0 :
            ret = False
    if ret is None:
        ret = True
    return ret

SERVICE_KEY = 'serviceKey=%2Fh7zZp%2BLhUwW4TEDZjcNrvHqMPgFlnqMl3ooLmM7Skaj6IGC6KiT55Xz%2FbbgyQ9aOBht90%2BvIvI4%2Bwq9Qa14Ww%3D%3D&'
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
    example = graph.nodeClass.busStopSearch(str(busStopName))
    if len(example) == 0 :
        print("정류소가 검색되지 않았습니다. 다른 정류소를 검색해 주세요")
        i = i -1
    else:
        for i in range(len(example)):
            print(str(i + 1) + ". " + example[i][0] + "(" + str(example[i][1]) + ")")
        selectNum = input("Please type number that you want to start : ")
        selectedItem = example[int(selectNum) - 1][1]
        startNode.append(int(selectedItem))
        graph.color_map[graph.nodeData.index(int(selectedItem))] = 'blue'

if not chcekConnectivity(graph.G, startNode):
    print("Nodes are not connected!")
else:
    ret = list()
    testingPath = graph.checkListInPath(startNode)
    if not(-1 in testingPath):
        busId = list(testingPath.keys())[0]
        print(str(busId) + "버스가 모든 목적지를 순회하고 있습니다.")
    else:
        if len(startNode) == 2:
            shortestPath = nx.dijkstra_path(graph.G, startNode[0], startNode[1], weight='weight')
            ret.append(getMediumPoint(graph.G, shortestPath))
        elif len(startNode) == 3:
            cal = ThreePointShortestPath(graph.G, startNode)
            ret.append(cal)
        else:
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
            cal = ThreePointShortestPath(graph.G, [i[0], i[1], i[2]])
            if ret == -1 or cal < ret:
                cal = ret
                way = list(i)
        graph.color_map[graph.nodeData.index(int(ret[0]))] = 'green'
        destId = ret[0]
        print(graph.nodeClass.busStopName(destId))
        weight = 0
        for i in startNode:
            pathW = nx.dijkstra_path(graph.G, i, destId, weight='weight')
            tmp = getPathWeight(graph.G, pathW)
            print(graph.labelDict[i] + " : " + str(tmp))
            weight = weight + tmp
        print("total weight is " + str(weight))

graph.drawGraph()
