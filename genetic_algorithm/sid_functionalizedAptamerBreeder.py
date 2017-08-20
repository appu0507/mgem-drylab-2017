from __future__ import division
from random import randint, choice
from numpy import mean
from difflib import SequenceMatcher
#made by sid for gluedtogether.py

def getAptamers(readfile):
    with open(readfile,"r") as input_sequences:
        sequences = input_sequences.readlines()
        aptamers = []
        for i in range(0,len(sequences)):
            try:
# FIGURE OUT HOW TO NORMALIZE THESE FITNESS SCORES, BEFORE CREATING POPULATION MEMBERS
                if '>' in sequences[i]:
                    size = (sequences[i].split('=')[1]).strip('\n;')
                    aptamers.append([sequences[i].strip('\n;'),sequences[i+1].strip('\n;'),int(size)])
            except IndexError:
                continue
    return aptamers

#DEPRECIATED
#generates a random aptamer for testing purposes 
def generateAptamer(length=20): # function to generate a random aptamer length nucleotides long
     aptamer = ""
     bases = ['A', 'G', 'C', 'T']
     for i in range(0,length):
         aptamer += choice(bases)
     return aptamer
#      n = randint(0,3)
#      if n == 0:
#         aptamer += "A"
#      elif n == 1:
#         aptamer += "C"
#      elif n == 2:
#         aptamer += "G"
#      else:
#         aptamer += "T"

def getFitness(sequence):
     # this is a placehodler function, it is going to be replaced by our trained ML model
     # IF THIS IS NORMALIZED, THEN MUST NORMALIZE SCORES IN FIRST GEN FOR THE getAptamers() function
     return (sequence.count('A')/len(sequence))*100

#DEPRECIATED
# generates a random pool of aptamers using the generateAptamer function
def genPool(pool_size, apt_size=20):
     aptamerList = []
     for i in range(1,pool_size):
         seq = generateAptamer(apt_size)
         aptamerList.append(['aptamer_' + str(i), seq, getFitness(seq)])
     return sorted(aptamerList, key=lambda x: x[2], reverse=True) 



##uses difflib string distance to compute child fitness from parents
## parent1 and parent 2 are in the format [aptamer_1, 'asdasdasdasdasda', 47]
## child is just a string, 'asdasdasdasdasdasdasd'
#def computeChildFitness(parent1=None, parent2=None, child=None):
#    #take distance to parent1, divide by len(child), then multiply by parent1 fitness. repeat for parent 2 and add the fitness values. ???????????????
#    if parent1 == None and parent2 == None:
#        raise ValueError('Need at least on valid parent')
#    elif parent1 == None:
#        return parent2[2]
#    elif parent2 == None:
#        return parent1[2]
#    elif parent1 != None and parent2 != None and child != None:
#        #TODO compute child fintess
#        # fitness function can be based on parents, needs to be only based on the sequence
#        # THIS IS A MADE UP PLACE HOLDER IT IS NOT INTENDED FOR FINAL USE
#        # return mean([parent1[2], parent2[2]])*mean([SequenceMatcher(None, parent1[1], child).ratio(), SequenceMatcher(None, parent2[1], child).ratio()])
#        return  
#    else:
#        raise ValueError('Invalid paramaters, need parent1, parent2 and child to all not be None')



# parent1 and parent 2 are in the format [aptamer_1, 'asdasdasdasdasda', 47]
def crossover(parent1, parent2, idnum, gennum):
    max_pos = min([len(parent1), len(parent2)])   
    crossOverPos = randint(1,max_pos-2) # random nucleotide postion along the max_pos bp aptamer, except not the 
    if crossOverPos%2 == 0:
        # if crossOverpos is even, first half of the child is from parent1, if not first half of child is from parent2
        childseq = parent1[1][:crossOverPos] + parent2[1][crossOverPos:]
        child = ["gen_" + str(gennum) + "_offspring_" + str(idnum), childseq, getFitness(childseq)]
    else:
        childseq = parent2[1][:crossOverPos] + parent1[1][crossOverPos:]
        child = ["gen_" + str(gennum) + "_offspring_" + str(idnum), childseq, getFitness(childseq)]
    return child
#   if crossOverPos == 0:
#      # just returns parent 1 since not acutally a crossover
#      child = ["offspring_" + str(i), sortedAptamerList[parent1][1], computeChildFitness(parent1)]
#   elif crossOverPos == max_pos-1:
#      child = ["offspring_" + str(i), sortedAptamerList[parent2][1], computeChildFitness(parent2)]
#   else:



#aptamer list format: [['aptamer_1, 'asdasdasdasd', 45], ['aptamer_2', 'asdasasdasd', 78]]
#the two highest scoring aptamers are randomly crossed over to generate a specified number of offspring
#assumed all aptamers are the same length
def breed(aptamers, gennum, top_cutoff=0.10):
    # sortedAptamerList should already be sorted but just because im paranoid im going to sort it again
    sortedAptamerList = sorted(aptamers, key=lambda x: x[2], reverse=True) 
    # list initialization
    bred_aptamers = []
    #elites is top 2%
    for elite in range(0, int(len(sortedAptamerList)*0.02)):
        bred_aptamers.append(sortedAptamerList[elite])
    # creates a list of the top 10% of of the sortedAptamerList based on fitness score
    top_parents = sortedAptamerList[:int(len(sortedAptamerList)*0.10)]
    # crossover parents randomly untill you get to population size
    for child in range(len(sortedAptamerList) - int(len(sortedAptamerList)*0.02)):
        bred_aptamers.append(crossover(choice(top_parents), choice(top_parents), child, gennum))
    return bred_aptamers
