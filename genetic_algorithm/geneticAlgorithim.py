#!/usr/bin/python
import sid_functionalizedAptamerBreeder as ab
import hairpins as hp
import mutate as mt
import sys
from keras.models import load_model

if len(sys.argv) < 6:
    print("how to use:")
    print("arg1 is the output file name")
    print("arg2 is the dereped fasta with 1st gen of aptamers")
    print("arg3 is the number of generations it runs for")
    print("arg4 is the cutoff % for top organisms for crossover")
    print("arg5 is the path to the ml model used to eval fitness scores")


# generation member: ['seq_1', 'asdasdasdasd', 45]
def runGeneticAlgorithim(aptamerData, generations):
    firstGen = ab.getAptamers(aptamerData)
    model = load_model(str(sys.argv[5])) #saved trained keras model
    for gen in range(generations):
        if gen == 0:
            lastGen = ab.breed(firstGen, gen, model, float(sys.argv[4]))
            for x in range(len(lastGen)):
                lastGen[x] = mt.mutate(lastGen[x], model)
        else:
            for x in range(len(lastGen)):
                lastGen[x] = mt.mutate(lastGen[x], model)
            lastGen = ab.breed(lastGen, gen, model, float(sys.argv[4]))
        for aptamer in lastGen:
            if hp.hairpin(aptamer[1]) == True:
                lastGen.remove(aptamer)
        print("Finished gen " + str(gen))
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
    with open(optFileName, 'w') as opt:
        opt.write('Input File\tGenerations\tCut-Off')
        opt.write(str(sys.argv[2]) + '\t' + str(sys.argv[3]) +'\t' + str(sys.argv[4]))
        opt.write('\t\t\t\tFirst Generation\t\t\t\t\t\t\t\t\t\tLast Generation\n')
        opt.write('Aptamer #\tAptamer Sequence\t\tFitness Score\tFitness Score\tAptamer Sequence\t\tAptamer #\n')
        for linum in range(min([len(x) for x in firstAndlast])):
            opt.write(firstAndlast[0][linum][0]+'\t'+firstAndlast[0][linum][1]+'\t'+str(firstAndlast[0][linum][2])+'\t\t\t'+str(firstAndlast[1][linum][2])+'\t\t\t'+firstAndlast[1][linum][1]+'\t'+firstAndlast[1][linum][0]+'\n')
    opt.close()

# potentialy useful statistics, but not sure where to output them, can add more if desired
#    totalApts = len(final_gen)
#    avgLength = average([len(x[0] for x in final_gen])
#    avgFitness = average([x[2] for x in final_gen])
    
#sys.argv[1,2,3] is ['outputfilename', aptamerData, number of generations, % cutoff for top scoring members in ab.breed]
runAndGetGAResults(sys.argv[1], sys.argv[2], int(sys.argv[3]))
