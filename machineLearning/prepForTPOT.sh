#!/bin/bash
# $1 is a dereplicated fasta file, $2 it the organism and round number
python ./convertReadsToCSV.py $1 opt.tmp
cat opt.tmp | tr 'A' '00'| tr 'G' '01'| tr 'C' '10'| tr 'T' '11' > "$2""Binary.csv"
rm opt.tmp
