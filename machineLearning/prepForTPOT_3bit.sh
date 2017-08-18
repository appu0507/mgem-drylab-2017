#!/bin/bash
# $1 is a dereplicated fasta file, $2 it the organism and round number
# This version converts bases to 3 bits; need '000' to pad length??
python ./convertReadsToCSV.py $1 opt.tmp
cat opt.tmp | sed 's/A/001/g'| sed 's/G/010/g'| sed 's/C/011/g'| sed 's/T/100/g' > "$2""Binary.csv"
#rm opt.tmp
