#! /bin/bash

module purge
module load Intel
module load OpenMPI

export LD_LIBRARY_PATH="${HOME}/codes/lib:${LD_LIBRARY_PATH}"
