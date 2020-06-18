#!/bin/bash

# get xyz containing 56 relaxed conformers and 2x3000 conformers from two MD trajectories
tar xf LocalOpt56__FirstMD3000__SecondMD3000.xyz.tar.xz

# generate descriptors, perform spares kPCA on locally relaxed conformers and project remaining conformers
asap gen_desc -f LocalOpt56__FirstMD3000__SecondMD3000.xyz --no-periodic soap -c 2.5 -n 8 -l 8 -g 0.25 -z 4 --crossover
asap map -f ASAP-desc.xyz -dm '[*]' skpca -s sequential -n 56 --no-scale
