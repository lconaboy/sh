#! /bin/bash

# Usage: ./check_ahf_finished.sh

# Must be run from the halos/ directory. Checks to see if the AHF run
# has finished, and prints out the log filenames of ones that haven't.

fin=($(grep -rl FINISHED | sort))
all=($(ls *.log | sort))
nall=$(ls *.log | wc -l)
nfin=$(grep -rl FINISHED | wc -l)

# echo $nall $nfin

for ((i=0; i<nall; i++)); do
    m=0
    for ((j=0; j<nfin; j++)); do
	# echo ${all[i]} ${fin[j]}
	if [ ${all[i]} = ${fin[j]} ]; then
	    m=1
	    break
	fi
    done

    if [ $m -eq 0 ]; then
	echo "${all[i]} not finished"
    fi
done

	    
