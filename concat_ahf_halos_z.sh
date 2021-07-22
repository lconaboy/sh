#! /bin/bash

# Usage: cd AHF/XXX/halos && concat_ahf_halos.sh

# Concatenates all of the AHF outputs to a single file called
# all_XXX.AHF_halos. Must be run from the same directory as the
# *_AHF_halos files.

re='AHF\/([0-9]{3})'
# wd=$(pwd)
fn=$(ls ahf_.0000.*.AHF_halos)

if [[ $fn =~ \.(z[0-9]+\.[0-9]+) ]]; then
    n=${BASH_REMATCH[1]}
    echo $n
else
    echo "-- can't extract redshift from AHF filenames"
fi


fn="all_${n}.AHF_halos"
echo "Writing to $fn"

if [[ -f $fn ]]; then
    rm $fn
fi

cat *_halos > $fn

fn="all_${n}.AHF_particles"
echo "Writing to $fn"

if [[ -f $fn ]]; then
    rm $fn
fi

fns=($(ls *_particles))

for ifn in ${fns[@]}; do
    # Redirecting the input onto wc returns just the integer number of
    # lines
    x=$(wc -l < $ifn)
    if [[ $x -eq 1 ]]; then
	echo "Found empty particles file $ifn"
    else
	cat $ifn >> $fn
    fi
done
