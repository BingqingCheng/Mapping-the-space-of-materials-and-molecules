import sys
from helpers_read_qm9 import read_qm9_database
from ase.io import write

''' Converts raw QM9 xyz files to a combined extended xyz file used by ASAP and projection_viewer '''

if __name__='__main__':
    atoms = read_qm9_database('QM9_raw')
    write('atoms_qm9.xyz',atoms)
