#!/bin/bash

# get xyz containing 10000 random samples from QM9
tar xf qm9__Random1E4.xyz.tar.xz

# generate descriptors and perform PCA for C-centers aftwards
asap gen_desc -f qm9__Random1E4.xyz --no-periodic soap -u minimal -pa
asap map -f ASAP-desc.xyz -dm '[*]' -ua --only_use_species 6 pca --no-scale
