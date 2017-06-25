import sid_functionalizedAptamerBreeder as ab
import hairpins as hp
import mutate as mt

#Function List:
# mt.mutate(sequence)
# hp.hairpin(sequence, max_hp_len)
# hp.striplist(list, stripval)
# hp.create_hairpin_dict(txtfile)
# hp.inverted_repeat(sequence)
# ab.generateAptamer(length)
# ab.genPool(pool_size)
# ab.computeChildFitnes(parent1, parent2, child)
# ab.crossover(parent1, parent2)
# ab.breed(sortedAptamerList, topcutoff, offspring)
'''
Order of how to do thing:

create pool
[
breed pool
for p in pool:
    cutoff = getbestFitnessScoringMembers(poolP) # cutoff is top 10%, can be adjusted
    if isElite(p) == True: # elite is top 2%, can be adjusted
         new_pool.append(p)
    while len(new_pool) < len(pool):
         new_pool.append(crossover(cutoff[randint], cutoff[randint]))
    for member in new_pool:
          new_pool.append(mutate(cutoff[randint])) 
    new_pool = removeChildrenWithHairpins(new_pool)
pool = new_pool
]
repeat [...] for x generations

'''
# generation member: ['seq_1', 'asdasdasdasd', 45]
def runGeneticAlgorithim(populationsize, generations):
    firstGen = ab.genPool(populationsize)
    for gen in range(generations):
        if gen == 0:
            nextGen = ab.breed(firstGen)
        else:
            nextGen = ab.breed(nextGen)
        for x in range(len(nextGen)):
            if hp.hairpin(nextGen[x][1]) != 0:
                nextGen.remove(x)
        for aptamer in nextGen:
            aptamer[1] = mt.mutate(aptamer[1])
    return nextGen


# final_gen is a list where each element is in the format [offspring_1, 'asdasdasda', 69]
def simulateAptamerGA(optFileName, pop_size, gens):
    final_gen = runGeneticAlgorithim(pop_size, gens)
    with open(optFileName, 'w') as opt:
        opt.write('Aptamer #\tAptamer Sequence\tFitness Score\n')
        for aptamer in final_gen:
            opt.write(str(aptamer[0]) + '\t' + str(aptamer[1]) + '\t' + str(aptamer[2]) + '\n')
    opt.close()
# potentialy useful statistics, but not sure where to output them, can add more if desired
#    totalApts = len(final_gen)
#    avgLength = average([len(x[0] for x in final_gen])
#    avgFitness = average([x[2] for x in final_gen])
    

simulateAptamerGA('test.GA', 20, 10)








