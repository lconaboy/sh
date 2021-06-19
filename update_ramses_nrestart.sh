#! /bin/bash

# Run from the directory containing the ramses output dirs. Uses a few
# other shell scripts to find the latest non-empty output dir and
# extracts the output number, then inserts into the namelist file,
# making a backup of the old one. Works in the case of empty/nonempty
# output dirs (i.e. running with withoutmkdir=.true.)

lo=$(. find_latest_output.sh)  # latest output_xxxxx

if [[ $lo =~ _([0-9]{5}) ]]; then
    printf -v ln "%g" ${BASH_REMATCH[1]}  # latest output n
fi

nml=($(ls *.nml))

if [[ ${#nml[@]} -ne 1 ]]; then
    echo More than one namelist found, exiting
    exit 1
fi

echo Updating nrestart to $ln
cp $nml $nml.bak
sed -i "/nrestart/ c nrestart=$ln" $nml
