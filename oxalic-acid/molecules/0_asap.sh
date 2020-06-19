#!/bin/bash

# get xyz containing 56 relaxed configurations and 7x3000 conformers from 7 MD trajectories
tar xf LocalOpt56__MD3000x7.xyz.tar.xz

# generate descriptors, perform spares kPCA on locally relaxed configurations and project remaining conformers
asap gen_desc -f LocalOpt56__MD3000x7.xyz --no-periodic soap -c 2.5 -n 8 -l 8 -g 0.25 -z 4 --crossover
asap map -f ASAP-desc.xyz -dm '[*]' skpca -s sequential -n 56 --no-scale
