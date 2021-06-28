#! /bin/bash

# Usage: run_r2g.sh <iout> <g/i/c>

i=$1
r=$(printf "%05d" ${i})
g=$(printf "%03d" ${i})

if [[ $2 == "i" ]]; then
    echo "Working in interpolating mode"
    snap_dir="snap_${g}_i"
    flag="-i"
    mi=""
    ma=""
elif [[ $2 == "g" ]]; then
    echo "Working in cell-by-cell mode"
    snap_dir="snap_${g}_g"
    flag="-g"
    mi=""
    ma=""
elif [[ $2 == "c" ]]; then
    snap_dir="snap_${g}_c"
    flag="-c"
    mi=0.475
    ma=0.525
    echo "-- bounding box [$mi, $ma]"
fi

work_dir="../output_${r}"

mkdir ${snap_dir}
cd ${snap_dir}

exe=${HOME}/codes/convert/ramses2gadget_mpi

mpiexec -n 8 $exe $flag $work_dir $mi $ma
