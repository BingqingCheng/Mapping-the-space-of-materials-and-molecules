#!/bin/bash
mkdir QM9_raw
cd QM9_raw
wget https://s3-eu-west-1.amazonaws.com/pstorage-npg-968563215/3195389/dsgdb9nsd.xyz.tar.bz2
tar -xvf dsgdb9nsd.xyz.tar.bz2
cd ..
python create_extended_xyz_qm9.py
rm -r QM9_raw
