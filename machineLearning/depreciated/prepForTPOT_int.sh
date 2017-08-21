#!/bin/bash
# $1 is a dereplicated fasta file, $2 it the organism and round number
# This version converts bases to 3 bits; need '000' to pad length??
python ./convertReadsToCSV.py $1 opt.tmp
cat opt.tmp | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' > "$2""int.csv"
rm opt.tmp
