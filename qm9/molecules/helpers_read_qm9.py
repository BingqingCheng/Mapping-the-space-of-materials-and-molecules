import os
import numpy as np
from ase.io import read
from openbabel import pybel as pb

try:
        import StringIO as io
except ImportError:
        import io

try:
    import pybel as pb
except ImportError:
    try:
        import openbabel.pybel as pb
    except:
        print('pybel is not installed, related methods will fail.')


# From database
dict_energies_b3lyp_qm9={'H':-0.500273*27.2113845,
                  'C':-37.846772*27.2113845,
                  'N':-54.583861*27.2113845,
                  'O':-75.064579*27.2113845,
                  'F':-99.718730*27.2113845}


def xyz2ase(xyz_str):
    """    Convert a xyz file to an ASE atoms object via in-memory file (StringIO).    """
    xyzfile = io.StringIO()
    xyzfile.write(xyz_str)
    mol = read(xyzfile, format="xyz")
    return mol


def calculate_atomization_energy(mol_ase, molecular_energy, use_energies_dict):
    '''    Calculate atomization energy for a QM9 molecule    '''
    at_energy=0.0
    try:
        for at in mol_ase.get_chemical_symbols():
            at_energy+=use_energies_dict[at]
    except: return 0.0, 0.0
    
    return float(molecular_energy)-at_energy, at_energy


def read_qm9_single_file(filename):
    
    '''    Read a single file from the qm9 database    '''
   
    print(filename) 
    lines=[]
    with open(filename) as out:
        for line in out.readlines():
            lines.append(line)
            
            
    lines=[l.replace('.*^', 'e') for l in lines]
    lines=[l.replace('*^', 'e') for l in lines]
    
    commentline=lines[1].split()
    lines[1]='\n'
    xyz=''.join(lines[:-3])

    at=xyz2ase(xyz)
    at.info['idx_qm9']=int(commentline[1])
    at.info['rotational_constant_a_b3lyp_ghz']=float(commentline[2])
    at.info['rotational_constant_b_b3lyp_ghz']=float(commentline[3])
    at.info['rotational_constant_c_b3lyp_ghz']=float(commentline[4])
    at.info['dipole_moment_D']=float(commentline[5])
    at.info['polarizability_a0^3']=float(commentline[6])
    at.info['EHOMO_eV']=float(commentline[7])*27.2113845
    at.info['ELUMO_eV']=float(commentline[8])*27.2113845
    at.info['EGap_eV']=float(commentline[9])*27.2113845
    at.info['elect_spatial_extent_a0^2']=float(commentline[10])
    at.info['ZPE_eV']=float(commentline[11])*27.2113845
    at.info['U0_eV']=float(commentline[12])*27.2113845
    at.info['U_eV']=float(commentline[13])*27.2113845
    at.info['H_eV']=float(commentline[14])*27.2113845
    at.info['G_eV']=float(commentline[15])*27.2113845
    
    at.info['atomization_energy_eV']=calculate_atomization_energy(at, at.info['U0_eV'], dict_energies_b3lyp_qm9)[0]
    at.info['smiles_b3lypgeo']=lines[-2].split()[-1]
    
    pbmol = pb.readstring('xyz',xyz)
    at.info['n_rings']=len(pbmol.OBMol.GetSSSR())
    hybridization = np.array([at.hyb for at in pbmol.atoms])
    in_ring = np.array([atom_pb.OBAtom.IsInRing() for atom_pb in pbmol.atoms])    
    
    charges=[]
    for i,l in enumerate(lines[2:-3]):
        charges.append(float(l.split()[-1]))

    at.arrays.update( {'mulliken_charges':np.array(charges),'hybridzation': hybridization, 'in_ring': in_ring})
    
    return at


def read_qm9_database(database_folder):
    '''    Read complete folder for qm9    '''
    list_files = [os.path.join(database_folder, x) for x in os.listdir(database_folder)]
    atoms=[]
    for filename in list_files:
        atoms.append(read_qm9_single_file(filename))        
    return atoms



