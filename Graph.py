import math
import copy

def getCartesianMatrix(city_coordinates):
	# input: [(0,0), (5,2), (3,4), (1,10), (10,15), (7,9), (8,4)]
	# Output: a matrix record the straight distance between coords.
	# Example:
	# For the input data, index of (0,0) is 0, and index of (3,4) is 2.
	# We save the distance of these 2 coords in our output matrix as: matrix[0,2]
	# print(matrix[0,2]) => you get 5

    matrix = {}
    for i,(x1, y1) in enumerate(city_coordinates):
        for j,(x2, y2) in enumerate(city_coordinates):
            dx, dy = (x1-x2), (y1-y2)
            dist = math.sqrt(dx*dx + dy*dy)
            matrix[i,j] = dist
    return matrix
    
def getTourPathDistance(disMatrix, tour):
	
	dis = 0
	for a in range(0, len(tour)-1):
		dis += disMatrix[tour[a],tour[a+1]]
	return dis

def getMSTCost(disMatrix, unvisitedCityList):
	targetCity = copy.deepcopy(unvisitedCityList)
	
	disList = []
	for a in targetCity:
		for b in targetCity:
			if a != b:
				dis = disMatrix[a, b]
				city = (a, b)
				disList.append((city, dis))
			
	disList = sorted(disList, key=lambda x: x[1])
	totalPath = 0
	for edge in disList:
		if edge[0][0] in targetCity or edge[0][1] in targetCity:
			totalPath += edge[1]
			if edge[0][0] in targetCity:
				targetCity.remove(edge[0][0])
			if edge[0][1] in targetCity:
				targetCity.remove(edge[0][1])
		if len(targetCity) == 0:
			break
	
	
	return totalPath
	