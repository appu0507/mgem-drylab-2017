from __future__ import division
from random import randint, choice
from tqdm import tqdm

def sequence_generator(num_sequences):
    bases = ['1', '2', '3', '4']
    sequence_list = []
    print 'generating {} random sequences and calculating melting temp'.format(num_sequences)
    for i in tqdm(range(num_sequences)):
        sequence_length = randint(15,30)
        sequence = ''
        for j in range(sequence_length):
            sequence += choice(bases)
        A = sequence.count('1')
        C = sequence.count('2')
        G = sequence.count('3')
        T = sequence.count('4')
        melting_temp = (2 * (A + T)) + (4 * (C + G))
        fitness = 1 - abs((65 - melting_temp))/65 #added by sid
        sequence_list.append([sequence, fitness])
    print 'writing output csv'
    with open('training_set.txt', 'wb') as output:
        for sequence in tqdm(sequence_list):
            output.write('{},{}\n'.format(sequence[0], sequence[1]))

sequence_generator(50000)

print 'output file written'
