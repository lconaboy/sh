#! /bin/bash

dirs=($(. check_empty_directories.sh))
nd=$((${#dirs[@]} / 2 ))  # $dirs is output_xxxxx \n full/empty ...

for ((i=0; i<$nd; i++)); do
    j=$(( $i * 2 ))  # output_xxxxx
    k=$(( $j + 1 ))  # full/empty

    if [[ ${dirs[k]} == full ]]; then
	iout=${dirs[j]}
	python ~/scripts/sh/get_redshift_from_info.py ${iout:7:12}
	break
    fi
done
