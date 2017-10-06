import msvcrt
import sys
import copy
import random
import time
from Graph import *

class TourInfo:
	def __init__(self, visitedCity=[], totalPath=sys.maxsize):
		self.visitedCity = visitedCity
		self.totalPath = totalPath
		
def tsp_HillClimbing(disMatrix, cityCoordinates, startedCityIndex):
	# Keep go to the nearest city until no unvisited city exists.
	# Return to started city from the last visited city
	visitedCity = []
	curCityIndex = startedCityIndex
	visitedCity.append(curCityIndex)
	
	while len(visitedCity) < len(cityCoordinates):
		minDistance = sys.maxsize
		# Get available city list
		for cityIndex in range(len(cityCoordinates)):
			if (cityIndex != curCityIndex) and (not cityIndex in visitedCity):
				if disMatrix[curCityIndex, cityIndex] < minDistance:
					minDistance = disMatrix[curCityIndex, cityIndex]
				
		for cityIndex in range(len(cityCoordinates)):
			if disMatrix[curCityIndex, cityIndex] == minDistance and \
			   not cityIndex in visitedCity:
				visitedCity.append(cityIndex)
				curCityIndex = cityIndex
				break
				
	
	visitedCity.append(startedCityIndex)
	totalPath = getTourPathDistance(disMatrix, visitedCity)
	
	tourInfo = TourInfo(visitedCity, totalPath)
	
	return tourInfo
	
def main():
	
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
	
	f = open('TSP_result_HillClimbing.txt', 'w')
	for i, city_coordinates in enumerate(cityCoordsSet):
		print("Testing Case:", i+1 , " .....")
		start_time = time.time()
	
		distance_matrix = getCartesianMatrix(city_coordinates)
		#print("Cities Coordinates:\n\t", city_coordinates, '\n\n')
		tmpCityIndex = range(0,len(city_coordinates))
		rand_initialCityIndex = random.sample(tmpCityIndex, int(len(tmpCityIndex)))  
		#initialCityIndex = random.randint(0, len(city_coordinates)-1)
	
		bestInfo = TourInfo()
		count = 0
		for initialCityIndex in rand_initialCityIndex:
			#print("==============================================")
			#print("Random Tour Solution %d:" % count)
			#print("Coordinate of start city:\n\t", city_coordinates[initialCityIndex])
	
			tourInfo = tsp_HillClimbing(distance_matrix, city_coordinates, initialCityIndex)
		
			#print("Tour Path:\n\t", end = '')
			#for cityIndex in tourInfo.visitedCity:
			#	print(city_coordinates[cityIndex], ' ', end = '')
	
			#print("\nPath Cost:")
			#print('\t', tourInfo.totalPath, '\n\n')
		
			if tourInfo.totalPath < bestInfo.totalPath:
				bestInfo.visitedCity = copy.deepcopy(tourInfo.visitedCity)
				bestInfo.totalPath = tourInfo.totalPath
			count += 1
	
		# print best choice
		#print("==============================================")
		#print("Best Tour Path:\n\t", end = '')
		#for cityIndex in bestInfo.visitedCity:
		#	print(city_coordinates[cityIndex], ' ', end = '')
		
		bestCost = bestInfo.totalPath
		end_time = time.time()
		exTime = end_time - start_time
		exeLog = ""
		exeLog = str(i+1) + " Total Cost: " + str(bestCost) + " Executeion Time: " \
				 + str(exTime) + "\n"
		f.write(exeLog)
	
if __name__ == '__main__':
	main()