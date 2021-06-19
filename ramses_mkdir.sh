#! /bin/bash

mi=$1
ma=$2

for i in $(seq -f "%05g" $mi $ma); do
    mkdir output_$i
done
