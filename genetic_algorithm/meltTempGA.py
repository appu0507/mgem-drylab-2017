#!/usr/bin/python
import numpy as np
import meltAptamerBreeder as ab
#import hairpins as hp
import meltMutate as mt
import sys
from tabulate import tabulate


if len(sys.argv) < 6:
    print("how to use:")
    print("arg1 is the output file name")
    print("arg2 is a csv file with dna seqs and fitness scores") 
    print("arg3 is the number of generations it runs for")
    print("arg4 is the cutoff % for top organisms for crossover")
    print("arg5 is the path to the ml model used to eval fitness scores")

from keras.models import load_model

# generation member: ['seq_1', 'asdasdasdasd', 45]
def runGeneticAlgorithim(aptamerData, generations):
    firstGen = ab.readMeltCSV(aptamerData)
    model = load_model(str(sys.argv[5])) #saved trained keras model
    lastGen = ab.breed(firstGen, 1, model, float(sys.argv[4]))
    print("finished breeding")
    for x in range(len(lastGen)):
        lastGen[x] = mt.mutate(lastGen[x], model)
    print("finished mutating")
    print("Finished gen 1")
    for gen in range(generations-1):
        for x in range(len(lastGen)):
            lastGen[x] = mt.mutate(lastGen[x], model)
        print("finished mutating")
        lastGen = ab.breed(lastGen, gen, model, float(sys.argv[4]))
        print("finished breeding")
#        for aptamer in lastGen:
#            if hp.hairpin(aptamer[1]) == True:
#                lastGen.remove(aptamer)
        print("Finished gen " + str(gen+2))
    return [firstGen, lastGen] 


#is a list where each element is in the format [offspring_1, 'asdasdasda', 69]
def runAndGetGAResults(optFileName, aptamer_data, gens):
    firstAndlast = runGeneticAlgorithim(aptamer_data, gens) 
    for gen in range(len(firstAndlast)):
        sorting = firstAndlast[gen]
        tmp = []
        for aptamer in sorting:
            tmp.append([aptamer[0], aptamer[1], aptamer[2]])
        tmp = sorted(tmp, key=lambda x: x[2], reverse=True)
        firstAndlast[gen] = tmp

    actualfitness = []
    for memb in firstAndlast[1]: #last generation
        seq = str(memb[1])
        A = seq.count('A')
        C = seq.count('C')
        G = seq.count('G')
        T = seq.count('D')
        melting_temp = (2 * (A + T)) + (4 * (C + G))
        fitness = 1 - abs((65 - melting_temp))/65 # get actualy fitness of optimized sequences 
        actualfitness.append(fitness)
    firstAndlast.append(actualfitness) 

    table = [] 
    table.append(['Input File','Generations','Cut-Off'])
    table.append([str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4])])
    table.append([''])
    table.append(['First Generation', '', 'Last Generation'])
    table.append(['Average Fitness', '', 'Average Fitness'])
    table.append([str(np.mean([x[2] for x in firstAndlast[0]])),'',str(np.mean([x[2] for x in firstAndlast[1]]))])
    table.append([''])
    table.append(['Aptamer Sequence','Fitness Score','Predicted Fitness','Actual Fitness','Fitness Error','Aptamer Sequence'])
    for linum in range(min([len(x) for x in firstAndlast])):
        table.append([str(firstAndlast[0][linum][1]),str(firstAndlast[0][linum][2]),str(firstAndlast[1][linum][2]),str(firstAndlast[2][linum]),str(abs(firstAndlast[1][linum][2]-firstAndlast[2][linum])),str(firstAndlast[1][linum][1])])
   
    with open(optFileName, 'w') as opt:
        opt.write(tabulate(table))
#    print(tabulate(table))

runAndGetGAResults(sys.argv[1], sys.argv[2], int(sys.argv[3]))


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
