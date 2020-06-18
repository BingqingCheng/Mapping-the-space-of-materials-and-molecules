#!/bin/bash

# get xyz containing 48 (rigid) crystals and its full-unit-cell relaxed counterparts
tar xf RigCrys48__FullOptCrys48.xyz.tar.xz

# generate descriptors and perform PCA
asap gen_desc -f RigCrys48__FullOptCrys48.xyz soap -u longrange --crossover
asap map -f ASAP-desc.xyz -dm '[*]' pca --no-scale
