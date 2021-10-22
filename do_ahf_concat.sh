#! /bin/bash

for i in AHF/*/halos; do
    if ! [ -f $i/all*halos ]; then
	cd $i && ~/scripts/sh/concat_ahf_halos.sh && cd -
    fi
done
