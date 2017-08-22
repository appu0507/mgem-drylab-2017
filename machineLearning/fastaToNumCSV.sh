#!/bin/bash
# "${@: -2:1} is a dereplicated fasta file, "${@: -1}" it the organism and round number
python ./convertReadsToCSV.py "${@: -1}" opt.tmp #converts fasta file to csv

if [ $# -lt 2 ] # checks if any flags, if not use default behaviour
then 
        cat opt.tmp | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' 
        # translates each base to an integer
else
    maxargs=4
    while test $# -gt 0
    do
        case "$1" in
            -k) 
                if [ "$#" == "$maxargs" ] 
                then
                cat opt.tmp |  perl -pe "s/.{$2}(?=.*,)/$&,/g" | sed 's/,,/,/g' | sed 's/,\./\./g' | sed 's/\.,/\./g' | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' > comma.tmp
                else
                cat opt.tmp |  perl -pe "s/.{$2}(?=.*,)/$&,/g" | sed 's/,,/,/g' | sed 's/,\./\./g' | sed 's/\.,/\./g' | sed 's/A/1/g'| sed 's/G/2/g'| sed 's/C/3/g'| sed 's/T/4/g' 
                fi
                shift 2 
                ;;
            # split file into kmers of size  $OPTARG, so there is a , in the csv file every $OPTARG characters in the sequence
            -b)
                if [ -e comma.tmp ]
                then
                    cat comma.tmp | perl -pe 's/(1|A)(?=.*,)/00/g'| perl -pe 's/(2|C)(?=.*,)/01/g' | perl -pe 's/(3|G)(?=.*,)/10/g' | perl -pe 's/(4|T)(?=.*,)/11/g'
                    rm comma.tmp
                else 
                    cat opt.tmp | perl -pe 's/(1|A)(?=.*,)/00/g'| perl -pe 's/(2|C)(?=.*,)/01/g' | perl -pe 's/(3|G)(?=.*,)/10/g' | perl -pe 's/(4|T)(?=.*,)/11/g'
                fi
                shift
                ;;
            # translates bases to binary instead of numeric
            *) 
                echo "unrecofnized option"
                break
                ;;
        esac
    done
fi   

rm opt.tmp
