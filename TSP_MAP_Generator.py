import random

f = open('testTSP.txt', 'w')
for dataCount in range(0,10):	
	data = []
	numCount = 0
	while numCount < 8:	
		coords = (random.randint(0,100), random.randint(0,100))
		if not coords in data:
			data.append(coords)
			outputStr = str(coords[0]) + ", " + str(coords[1]) + "\n"
			f.write(outputStr)
			numCount += 1
	f.write("\n")
f.close()
