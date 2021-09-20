#! /bin/bash

x=(output_00*)

min=-1
max=$(( ${#x[@]} -1 ))

for ((i=$max; i>$min; i--)); do
    n=$(ls ${x[$i]} | wc -l);
    if [[ $n -gt 0 ]]; then
	echo ${x[$i]} full;
    else
	echo ${x[$i]} empty;
    fi
done
