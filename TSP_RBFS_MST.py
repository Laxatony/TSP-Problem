import random
import math
import time
from Graph import *
from heapq import heappush, heappop

g_disMatrix = []
g_totalCityNum = 0
g_BestPath = []

g_totalCreatedNode = 0
g_totalStep = 0

def generateRandomTour(cityCoordinates, sampleNum):
	#calculate the Manhattn Distance of each tiles from current state to goal state

	result = []
	numOfCities = len(cityCoordinates)
	
	for count in range(sampleNum):
		randomed_tour = random.sample(range(0,numOfCities), numOfCities)
		randomed_tour.append(randomed_tour[0])
		result.append(randomed_tour)
		
	return result

class stateNode:
	global g_disMatrix
	global g_totalCityNum
	
	def __init__(self, visitedCityList):
		self.visitedCityList = copy.deepcopy(visitedCityList)
		self.gCost = getTourPathDistance(g_disMatrix, visitedCityList)
		self.hCost = 0
		
		#set unVisitedCityList
		self.unVisitedCityList = []
		for cityIndex in range(0, g_totalCityNum):
			if not cityIndex in self.visitedCityList:
				self.unVisitedCityList.append(cityIndex)
				
		#set hCost( min(curCity to MST) + (MST Cost) + min(MST to root) )
		self.hCost = 0
		rootCityIndex =  self.visitedCityList[0]
		curCityIndex = self.visitedCityList[len(self.visitedCityList)-1]
		if len(self.unVisitedCityList) != 0:	
			minCurToMST = math.inf
			for city in self.unVisitedCityList:
				if minCurToMST > g_disMatrix[curCityIndex, city]:
					minCurToMST = g_disMatrix[curCityIndex, city]
		
			mstCost = getMSTCost(g_disMatrix, self.unVisitedCityList)

			minMSTToRoot = math.inf
			for city in self.unVisitedCityList:
				if minMSTToRoot > g_disMatrix[rootCityIndex, city]:
					minMSTToRoot = g_disMatrix[rootCityIndex, city]
				
			self.hCost = minCurToMST + mstCost + minMSTToRoot
		else: # no unvisited City(no MST), hCost is (curCity to startCity)
			self.hCost = g_disMatrix[curCityIndex, rootCityIndex]
			
			
		#setfCost
		self.fCost = self.gCost + self.hCost
		
		
		self.alternativeCost = 0
		
	def getGCost(self):
		return self.gCost
	
	def setAlternativeCost(self, cost):
		self.alternativeCost = cost
	def getAlternativeCost(self, cost):
		return self.alternativeCost

def expendAvailabelStateNode(curStateNode):
	# This function is used for expend next candidate states.
	# The state will be put into a priority queue is it hasn't be generated before. 
	
	global g_totalCreatedNode
	successors = []
	
	pastVisitedCityList = curStateNode.visitedCityList
	unVisitedCityList = copy.deepcopy(curStateNode.unVisitedCityList)
	
	for cityIndex in unVisitedCityList:
		visitedCityList = copy.deepcopy(pastVisitedCityList)
		visitedCityList.append(cityIndex)

		nextStateNode = stateNode(visitedCityList)
		heappush(successors, (nextStateNode.fCost, nextStateNode.gCost, nextStateNode.hCost,visitedCityList, nextStateNode))
		g_totalCreatedNode += 1
		
	return successors
	
def RBFS_Algorithm(curStateNode, fLimit):
	global g_totalCityNum
	global g_BestPath
	global g_totalStep
	global g_totalCreatedNode
	
	if len(curStateNode.visitedCityList) == g_totalCityNum:
		g_BestPath = copy.deepcopy(curStateNode.visitedCityList)
		return True, curStateNode.fCost
		
	successors_PQ = expendAvailabelStateNode(curStateNode)
	if len(successors_PQ) == 0:
		return False, math.inf
		
	isTrue = False
	while not isTrue:
		bestSuccessor_PQ = heappop(successors_PQ)
		g_totalStep += 1
		bestSuccessor = bestSuccessor_PQ[4]
		bestCost = bestSuccessor.fCost
		if bestCost > fLimit:
			return False, bestCost
			
		if len(successors_PQ) > 0:
			secondSuccessor_PQ = successors_PQ[0]
			secondSuccessor = secondSuccessor_PQ[4]
			bestSuccessor.alternativeCost = secondSuccessor.fCost
		else:
			bestSuccessor.alternativeCost = math.inf
			
		isTrue, bestCost = RBFS_Algorithm(bestSuccessor, min(fLimit, bestSuccessor.alternativeCost))
		bestSuccessor.fCost = bestCost
		heappush(successors_PQ, (bestSuccessor.fCost, bestSuccessor.hCost, bestSuccessor.gCost, bestSuccessor.visitedCityList, bestSuccessor))
		g_totalCreatedNode += 1
		
		if isTrue:			
			return True, bestCost

def main():
	# read test puzzles from disk
	# run each puzzle and save the performance result into a txt file 
	global g_disMatrix
	global g_totalCityNum
	global g_BestPath
	
	global g_totalCreatedNode
	global g_totalStep
	
	cityCoordsSet = []
	f = open('testTSP.txt', 'r')
	data = []
	for line in f:
		line = line[:-1]
		if len(line) > 2:
			line = line.split(', ')
			data.append( (int(line[0]), int(line[1])) )
		else:
			if len(data) > 0:
				pushData = copy.deepcopy(data)
				cityCoordsSet.append(pushData)
				data = []
	f.close()
	
	f = open('TSP_result_RBFS.txt', 'w')
	for i, city_coordinates in enumerate(cityCoordsSet):
		print("Testing Case:", i+1 , " .....")
		start_time = time.time()
		
		g_disMatrix = getCartesianMatrix(city_coordinates)
		g_totalCityNum = len(city_coordinates)
	
		visitedCityList = [0]
		initialStateNode = stateNode(visitedCityList);
			
		result, bestCost = RBFS_Algorithm(initialStateNode, math.inf)
	
		g_BestPath.append(g_BestPath[0])
		end_time = time.time()
		exTime = end_time - start_time
		exeLog = ""
		exeLog = str(i+1) + " Total Cost: " + str(bestCost) + " Executeion Time: " \
				 + str(exTime) + " NodeCreated: " + str(g_totalCreatedNode) + " Steps: " + str(g_totalStep) + "\n"
		f.write(exeLog)
		
		g_disMatrix = []
		g_totalCityNum = 0
		g_BestPath = []
		g_totalCreatedNode = 0
		g_totalStep = 0
	f.close()
	print("Done")
	
if __name__ == '__main__':
	main()