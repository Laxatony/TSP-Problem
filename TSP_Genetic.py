import msvcrt
import sys
import copy
import numpy as np
from Graph import *
import random
import time
from heapq import heappush, heappop

myPQ_BestTour = [] # use heappush(myPQ_BestTour, (value, node))

class TourInfo:
	def __init__(self, visitedCity=[], totalPath=sys.maxsize):
		self.visitedCity = visitedCity
		self.totalPath = totalPath
		

def generateRandomTour(cityCoordinates, sampleNum):
	# return a random order of cities index
	result = []
	numOfCities = len(cityCoordinates)
	
	for count in range(sampleNum):
		randomed_tour = random.sample(range(0,numOfCities), numOfCities)
		randomed_tour.append(randomed_tour[0])
		result.append(randomed_tour)
		
	return result
	
def fitnessFunction(disMatrix, last_population):
	# fitness function is used for calculating the weight of each path
	# the shortest path has the highest weight
	
	global myPQ_BestTour
	
	distanceList = []
	for tour in last_population:
		distanceList.append(getTourPathDistance(disMatrix, tour))
	
	minDis = min(distanceList)
	maxDis = max(distanceList)
	
	totalDistance = sum(distanceList)
	ratioList = []
	for distance in distanceList:
		ratio = (totalDistance - distance) / totalDistance
		ratioList.append(ratio)
	totalRatioValue = sum(ratioList)
	for i, ratio in enumerate(ratioList):
		ratioList[i] = ratio / totalRatioValue
	
	bestTour = []
	for i, ratio in enumerate(ratioList):
		if ratio == max(ratioList):
			bestTour = copy.deepcopy(last_population[i])
			break
			
	minPath = getTourPathDistance(disMatrix, bestTour)

	heappush(myPQ_BestTour, (minPath, bestTour))

	'''
	print(" ============== fitnessFunction ============== ")
	print(bestTour)
	'''

	return bestTour, ratioList

def selectedPopulationByProb(last_population, ratioList):
	# This function is used for select the next generation.
	# The amount of next generation is the same as current generation
	# Each sample is selected with it's own probability
	
	#for a in last_population:
	#	print(a)
	
	numOfPopulation = len(last_population)
	selected_Indexs = np.random.choice(range(0,numOfPopulation), numOfPopulation, p=ratioList)
	
	selected_population = []
	for index in selected_Indexs:
		selected_population.append(last_population[index])

	#print("Now select new population by prob.:")
	#for a in selected_population:
	#	print(a)
	
	return selected_population
	
def random_pair(selected_population):
	# For crossover procedure, we pair the population by random
	'''
	for pair in selected_population:
		print(pair)
	print('\n')
	'''
	numOfPopulation = len(selected_population)
	pairOrder = random.sample(range(0,numOfPopulation), numOfPopulation)
	
	paired_population = []
	pairNum = int(numOfPopulation / 2)
	for count in range(pairNum):
		index = count*2
		pair1 = selected_population[pairOrder[index]]
		pair2 = selected_population[pairOrder[index+1]]
		paired_population.append([pair1, pair2])
	'''	
	for pair in paired_population:
		print(pair[0], " and ", pair[1])
	'''
	return paired_population
	
def random_crossover(paired_population):
	# input: [[A, B], [C, D], ....]
	# for each sublist, do crossover
	#
	# output: [A', B', C', D', ...]
	
	crossovered_population = []
	for pair in paired_population:
		A = pair[0]
		B = pair[1]
		lenOfList = len(A)
		crossoverPointIndex = random.randint(0, lenOfList-1)
		

		blankCount = lenOfList - (crossoverPointIndex+1)	
		crossover_A = A[0:crossoverPointIndex]
		for index in range(0, lenOfList-1):
			if not B[index] in crossover_A:
				crossover_A.append(B[index])
				blankCount -= 1
				if blankCount == 0:
					break
		crossover_A.append(crossover_A[0])
		
		blankCount = lenOfList - (crossoverPointIndex+1)
		crossover_B = B[0:crossoverPointIndex]
		for index in range(0, lenOfList-1):
			if not A[index] in crossover_B:
				crossover_B.append(A[index])
				blankCount -= 1
				if blankCount == 0:
					break
		crossover_B.append(crossover_B[0])
		

		crossovered_population.append(crossover_A)
		crossovered_population.append(crossover_B)	
		'''
		print("before crossover:")
		print("\t", A, " and ", B)
		print("after crossover:")
		print("\t", crossover_A, " and ", crossover_B)
		'''
	return crossovered_population		
	
def reproduction(selected_population):

	paired_population = random_pair(selected_population)

	reproduction_population = random_crossover(paired_population)
	
	return reproduction_population
	
def randomMutate(reproduction_population):
	
	mutated_population = copy.deepcopy(reproduction_population)

	for tour in mutated_population:
		lenOfTour = len(tour)
		mutateIndex1 = random.randint(1,lenOfTour-2)
		mutateIndex2 = random.randint(1,lenOfTour-2)
		
		#print("MutateIndex1: ", mutateIndex1, ", MutateIndex2: ", mutateIndex2)
		if not mutateIndex1 == mutateIndex2:
			#print("Before Random Mutate: ", tour)
			tmp = tour[mutateIndex1]
			tour[mutateIndex1] = tour[mutateIndex2]
			tour[mutateIndex2] = tmp
			#print(" After Random Mutate: ", tour)
			
	return mutated_population
		
	
def tsp_Genetic(disMatrix, cityCoordinates, sampleNum, generationCount=1):
	
	initial_population = generateRandomTour(cityCoordinates, sampleNum)
	
	last_population = copy.deepcopy(initial_population)
	bestTour, ratioList = fitnessFunction(disMatrix, last_population)
	'''
	print(" ============== Initioal population ============== ")
	for tour in last_population:
		print(tour)
	'''
	
	for count in range(generationCount):
		
		selected_population = selectedPopulationByProb(last_population, ratioList)
		'''
		print(" ============== selected_population ============== ")
		for tour in selected_population:
			print(tour)
		'''
		
		reproduction_population = reproduction(selected_population)
		'''
		print(" ============== reproduction_population ============== ")
		for tour in reproduction_population:
			print(tour)
		'''
		
		random_mutate_population = randomMutate(reproduction_population)
		'''
		print(" ============== random_mutate_population ============== ")
		for tour in random_mutate_population:
			print(tour)
		'''
		
		last_population = copy.deepcopy(random_mutate_population)
		bestTour, ratioList = fitnessFunction(disMatrix, last_population)
	
def main():
	global myPQ_BestTour
	
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
	
	f = open('TSP_result_Genetic.txt', 'w')
	for i, city_coordinates in enumerate(cityCoordsSet):
		print("Testing Case:", i+1 , " .....")
		start_time = time.time()
		
		distance_matrix = getCartesianMatrix(city_coordinates)
		#print("Cities Coordinates:\n\t", city_coordinates, '\n\n')

		sample = 200
		generation = 50
		tsp_Genetic(distance_matrix, city_coordinates, sample, generation)
	
		bestTour = myPQ_BestTour[0]	
		#print("Top path of each generations: ", len(myPQ_BestTour))
		#while not len(myPQ_BestTour) == 0:
		#	tour = heappop(myPQ_BestTour)
		#	print("Tour:", tour[1])
		#	print("Path:", tour[0])
	
		#print('\n')
		#print("Shoutest Tour:", bestTour[1])
		#print("Minimum Path:", bestTour[0])
		
		bestCost = bestTour[0]
		
		end_time = time.time()
		exTime = end_time - start_time
		exeLog = ""
		exeLog = str(i+1) + " Total Cost: " + str(bestCost) + " Executeion Time: " \
				 + str(exTime) + "\n"
		f.write(exeLog)
		
		myPQ_BestTour = []
	
	
if __name__ == '__main__':
	main()