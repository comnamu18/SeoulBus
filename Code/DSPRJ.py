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
def getPathWeight(G, path):
    ret = 0
    pathIter = iter(path)
    point = next(pathIter)
    for i in pathIter:
        ret = ret + G[point][i]['weight']
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
    example = graph.nodeClass.busStopSearch(str(busStopName))
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
    if len(startNode) == 2:
        ret.append(nx.dijkstra_path(graph.G, startNode[0], startNode[1], weight='weight'))
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

graph.drawGraph()
