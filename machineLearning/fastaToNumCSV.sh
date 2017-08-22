#!/bin/bash
# "${@: -2:1} is a dereplicated fasta file, "${@: -1}" it the organism and round number
python ./convertReadsToCSV.py "${@: -2:1}" opt.tmp

#case "${@: -2:1}" in
#    "-b") 
#        cat opt.tmp | tr 'A' '00'| tr 'G' '01'| tr 'C' '10'| tr 'T' '11' > "${@: -1}""Binary.csv"
#        ;;
#    *)
#        cat opt.tmp | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' > "${@: -1}""int.csv"
#esac

if [ $# -lt 3 ]
then 
        cat opt.tmp | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' > "${@: -1}""int.csv"
else
    while getopts 'k:b' opt ; do
        case $opt in
            k) cat opt.tmp |  perl -pe "s/.{$OPTARG}(?=.*,)/$&,/g" | sed 's/,,/,/g' | sed 's/,\./\./g' | sed 's/\.,/\./g' | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' > "${@: -1}""int.csv" ;;
            b) cat opt.tmp | tr 'A' '00'| tr 'G' '01'| tr 'C' '10'| tr 'T' '11' > "${@: -1}""Binary.csv" ;;
        esac
    done
fi   

rm opt.tmp
