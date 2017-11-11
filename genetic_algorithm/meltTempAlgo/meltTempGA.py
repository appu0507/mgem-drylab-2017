#!/usr/bin/python
from __future__ import division
import numpy as np
import meltAptamerBreeder as ab
import meltTempHairpin as hp
import meltMutate as mt
import sys
from tabulate import tabulate

# bash command to run model with a bunch of different generation numbers
# for  in {1..30}; do python meltTempGA.py unneeded ../../machineLearning/aptamerdata.csv $i 0.05 ../../machineLearning/savedmodels/meltb35e550.h5 > $i'GenLowStartingfitness.out' ; done
# 1 and 30 can be vaired, as well as all the normal parameters for running the genetic algorithim

#if len(sys.argv) < 6:
if len(sys.argv) < 5:
    print("how to use:")
#    print("arg1 is the output file name")
    print("arg1 is a csv file with dna seqs and fitness scores") 
    print("arg2 is the number of generations it runs for")
    print("arg3 is the cutoff % for top organisms for crossover")
    print("arg4 is the path to the ml model used to eval fitness scores")
    raise ValueError("Not enough arguments")

from keras.models import load_model

print("This program prints results to STDOUT, to save to a file, redirect to a txt file using > in bash")

# generation member: ['seq_1', 'asdasdasdasd', 45]
def runGeneticAlgorithim(aptamerData, generations):
    firstGen = ab.readMeltCSV(aptamerData) #gets data out of csv
    model = load_model(str(sys.argv[4])) #load trained keras model
    lastGen = ab.breed(firstGen, 1, model, float(sys.argv[3])) #breed generation once
#    print("finished breeding")
    for x in range(len(lastGen)): # for each member of gen2
        lastGen[x] = mt.mutate(lastGen[x], model) #mutate that sequence
#    print("finished mutating")
#    print("Finished gen 1")
    for gen in range(generations-1): # for x-1 number of generations
        lastGen = ab.breed(lastGen, gen, model, float(sys.argv[3])) #breed all members 
#        print("finished breeding")
        for x in range(len(lastGen)): # for each member of that generation
            lastGen[x] = mt.mutate(lastGen[x], model) #mutate member
#        print("finished mutating")
        for aptamer in lastGen: # for member in generation 
            if hp.hairpin(aptamer[1]) == True: # if there is a hairpin
                lastGen.remove(aptamer) # remove aptamer from generation
#        print("Finished removing hairpins")
#        print("Finished gen " + str(gen+2))
    return [firstGen, lastGen] # return the first and last generations


#is a list where each element is in the format [offspring_1, 'asdasdasda', 69]
def runAndGetGAResults( aptamer_data, gens):
    firstAndlast = runGeneticAlgorithim(aptamer_data, gens) #run algorithim to get first and last generation
    for gen in range(len(firstAndlast)): # the first and last generation
        sorting = firstAndlast[gen]
        tmp = []
        for aptamer in sorting: # for each aptamer in the generation
            tmp.append([aptamer[0], aptamer[1], aptamer[2]]) # add aptamer to tmp
        tmp = sorted(tmp, key=lambda x: x[2], reverse=True) # sort aptamers by fitness (high to low)
        firstAndlast[gen] = tmp #replace generation with sorted generation

    actualfitness = []
    for memb in firstAndlast[1]: #for aptamer in last generation
        seq = str(memb[1]) # get sequence
        A = seq.count('A')
        C = seq.count('C')
        G = seq.count('G')
        T = seq.count('D')
        melting_temp = (2 * (A + T)) + (4 * (C + G)) #calculate melting temperature
        fitness = 1 - abs((65 - melting_temp))/65 # convert melting temp to fitness
        actualfitness.append(fitness) # create list of all actuall fitness values for last generation
    firstAndlast.append(actualfitness) 

    table = [] 
    table.append(['Input File','Generations','Cut-Off'])
    table.append([str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])]) # add paramater info
    table.append([''])
    table.append(['First Generation', '', 'Last Generation'])
    table.append(['Average Fitness', '', 'Average Fitness'])
    table.append([str(np.mean([x[2] for x in firstAndlast[0]])),'',str(np.mean([x[2] for x in firstAndlast[1]]))]) #print average fitness for first and last generation
    table.append([''])
    

#    for x in predictedFits:
#        for y in actualFit:
#            errorFit.append(abs(x-y)*100/y)

    table.append([''])
    table.append(['Aptamer Sequence','Fitness Score','Predicted Fitness','Actual Fitness','Fitness Error','Aptamer Sequence'])
    errorFit = []
    for linum in range(min([len(x) for x in firstAndlast])): #print all data as specified in header
        errorFit.append(abs(firstAndlast[1][linum][2]-firstAndlast[2][linum])*100/firstAndlast[1][linum][2])
        table.append([str(firstAndlast[0][linum][1]),str(firstAndlast[0][linum][2]),str(firstAndlast[1][linum][2]),str(firstAndlast[2][linum]),str(abs(firstAndlast[1][linum][2]-firstAndlast[2][linum])),str(firstAndlast[1][linum][1])])
   
#    with open(optFileName, 'w') as opt: #write to output file
#        opt.write(tabulate(table)) #format using tabulate libraryi
    table.append(['Average Prediction Error', str(np.mean(errorFit))])
    print(tabulate(table))

runAndGetGAResults(sys.argv[1], int(sys.argv[2])) # funcition call




















# old crap, not being used 

#    with open(optFileName, 'w') as opt:
#        opt.write('Input File\tGenerations\tCut-Off\n')
#        opt.write(str(sys.argv[2]) + '\t' + str(sys.argv[3]) +'\t' + str(sys.argv[4]) + '\n')
#        opt.write('\t\tFirst Generation\t\t\t\t\t\tLast Generation\n')
#        opt.write('\t\tAverage Fitness \t\t\t\t\t\tAverage Fitness\n')
#        opt.write('\t\t'+str(np.mean([x[2] for x in firstAndlast[0]]))+'  \t\t\t\t\t\t'+str(np.mean([x[2] for x in firstAndlast[1]]))+'\n')
#        opt.write('Aptamer Sequence\t\tFitness Score\tPredicted Fitness\tActual Fitness\tFitness Error\tAptamer Sequence\n')
#        for linum in range(min([len(x) for x in firstAndlast])):
#            opt.writei(str(firstAndlast[0][linum][1])+'\t\t'+str(firstAndlast[0][linum][2])+'\t'+str(firstAndlast[1][linum][2])+'\t'+str(firstAndlast[2][linum])+'\t'+str(abs(firstAndlast[1][linum][2]-firstAndlast[2][linum]))+'\t'+str(firstAndlast[1][linum][1])+'\n')
#        
#
#        opt.write('Aptamer #\tAptamer Sequence\tFitness Score\tPredicted Fitness Score\tActual Fitness Score\tFitness Error \tAptamer Sequence\tAptamer #\n')
#        for linum in range(min([len(x) for x in firstAndlast])):
#            opt.write(str(firstAndlast[0][linum][0])+'\t'+str(firstAndlast[0][linum][1])+'\t'+str(firstAndlast[0][linum][2])+'\t'+str(firstAndlast[1][linum][2])+'\t'+str(firstAndlast[2][linum])+'\t'+str(abs(firstAndlast[1][linum][2]-firstAndlast[2][linum]))+'\t'+str(firstAndlast[1][linum][1])+'\t'+str(firstAndlast[1][linum][0])+'\n')
#    opt.close()

# potentialy useful statistics, but not sure where to output them, can add more if desired
#    totalApts = len(final_gen)
#    avgLength = average([len(x[0] for x in final_gen])
#    avgFitness = average([x[2] for x in final_gen])
    
#sys.argv[1,2,3] is ['outputfilename', aptamerData, number of generations, % cutoff for top scoring members in ab.breed]
