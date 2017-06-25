from random import randint
import random
#Population is assumed to be a list, can be modified
def pickRandomPair(population):
	pick1 = randint(0,len(population)-1)
	pick2 = randint(0,len(population)-1)
	
	#makes sure same member isnt picked twice
	while pick1 == pick2:
		pick2 = randint(0,len(population)-1)
	return (population[pick1], population[pick2])

#pair is assumed to be a tuple of len 2, with each element being a sequence
def crossoverPair(pair):
	#position where the crossover will occur
	crossloc = randint(0,min([len(pair[0]), len(pair[1])])-1)
	cross1 = pair[0][:crossloc] + pair[1][crossloc:]
	cross2 = pair[1][:crossloc] + pair[0][crossloc:]
	return (cross1, cross2)

#For testing purposes only
seq1 = 'aaaabaaaabaaaabaaaab'
seq2 = 'abcdfabcdfabcdfabcdf'
seq3 = 'vvvvvvvvvvvvv'
seq4 = 'qweqweqweqweqweqweqweqweqweqwe'
seqPair = (seq1, seq2)
testpop = [seq1, seq2, seq3, seq4]
random.seed(101)

#print pickRandomPair(testpop) #works 
#print type(pickRandomPair(testpop)) #works (returns tuple)

#print(crossoverPair(seqPair)) #works
#print(crossoverPair(pickRandomPair(testpop)))
