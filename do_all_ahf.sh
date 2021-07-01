#! /bin/bash

# Usage: ./do_all_ahf.sh <iout>
# 
# Run from output dir

i=$1

python ~/scripts/sh/gen_ahf_input.py $(pwd) $i

~/scripts/sh/run_r2g.sh $i g

wait

printf -v ii "%03g" $i

ln -s snap_${ii}_g snap_${ii}


sed -i "/out=/ c out=\"$ii\"" run_ahf.cosma

sbatch run_ahf.cosma
