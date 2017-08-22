#!/bin/bash
# "${@: -2:1} is a dereplicated fasta file, "${@: -1}" it the organism and round number
python ./convertReadsToCSV.py "${@: -1}" opt.tmp #converts fasta file to csv

if [ $# -lt 3 ] # checks if any flags, if not use default behaviour
then 
        cat opt.tmp | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' 
        # translates each base to an integer
else
    while getopts 'k:b' opt ; do 
        case $opt in
            k) cat opt.tmp |  perl -pe "s/.{$OPTARG}(?=.*,)/$&,/g" | sed 's/,,/,/g' | sed 's/,\./\./g' | sed 's/\.,/\./g' | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' ;;
            # split file into kmers of size  $OPTARG, so there is a , in the csv file every $OPTARG characters in the sequence
            b) cat opt.tmp | perl -pe 's/A/00/g'| perl -pe 's/C/01/g' | perl -pe 's/G/10/g' | perl -pe 's/T/11/g' ;;
            # translates bases to binary instead of numeric
        esac
    done
fi   

rm opt.tmp
