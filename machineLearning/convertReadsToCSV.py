#!/usr/bin/python
from __future__ import division
import sys, csv, pysam
'''
Convert this into a csv where records are [header, reads, sequence]

>M00719:298:000000000-AP41H:1:2104:20966:14893:2;size=3;
CAAGCATGGACAATACCGAGCCCGCACGTAATGCCCGAGGTTTGGTCCTGGGTTGCTGATCTTGTCATCGGAGGCTTAGA
GATCGGAAGAGCACACGTCTGAACTCCAGTCACGGCTACATCTCGTATGCCGTCTTCTGCTTGAAAAAAAACGGCGACCA
CCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCTCAAGCATGGACAATACCGAGCCCGCACGTAATGCCCGA
GGTTTGGTCCTGGGTTGCTGATCTTGTCATCGGAGGCTTAG
'''

fasta_file = pysam.FastaFile(sys.argv[1])

with open(sys.argv[2], 'wb') as csvf:
    fasta_writer = csv.writer(csvf, delimiter=',')
    fasta_writer.writerow(['reads', 'sequence'])
    maxfit = max([int(str(ref).split('=')[1].strip('\n;')) for ref in fasta_file.references])
    for ref in fasta_file.references:
        fasta_writer.writerow([int((str(ref).split('=')[1]).strip('\n;'))/maxfit, fasta_file.fetch(ref)])

