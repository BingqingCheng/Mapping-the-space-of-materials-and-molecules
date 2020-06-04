import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

import ase.io


def get_info_values(key, atoms):
    """Return a ndarray with values stored under atoms_i.info[`key`]."""
    values = [atoms_i.info[key] for atoms_i in atoms]
    return np.asarray(values)

def get_arrays(key, atoms):
    """Return a long ndarray of arrays stored under atoms_i.arrays[`key`]."""
    arrays = atoms[0].arrays[key]
    for atoms_i in atoms[1:]:
        arrays = np.concatenate((arrays, atoms_i.arrays[key]))
    return arrays


## Collect the data
atoms = ase.io.read('ASAP-lowD-map.xyz', ':')
local_opt = atoms[:56]
first_md = atoms[56:3056]
second_md = atoms[3056:]

lopt_pcs = get_info_values('skpca-d-10', local_opt)
fmd_pcs = get_info_values('skpca-d-10', first_md)
smd_pcs = get_info_values('skpca-d-10', second_md)

lopt_pc1, lopt_pc2 = lopt_pcs[:, 0], lopt_pcs[:, 1]
fmd_pc1, fmd_pc2 = fmd_pcs[:, 0], fmd_pcs[:, 1]
smd_pc1, smd_pc2 = smd_pcs[:, 0], smd_pcs[:, 1]

lopt_energies = get_info_values('E_dftbplus_ts_relative', local_opt)


## Plotting

# marker size scaling of locally relaxed conformers according to stability
size_range = [30, 150]
inv_energy = 1./(lopt_energies + 0.1)
inv_energy_range = [np.min(inv_energy), np.max(inv_energy)]
sizes = size_range[0] + (size_range[1] - size_range[0])/(inv_energy_range[1] - inv_energy_range[0]) * inv_energy

# locally relaxed conformers
pcmm = plt.scatter(lopt_pc1, lopt_pc2, zorder=2, s=sizes, c=lopt_energies, cmap='gnuplot', edgecolor='k', linewidths=0.2)
plt.colorbar(pcmm).set_label('Relative Energy / eV', rotation=270, labelpad=20)

# molecular dynamics data from two trajectories initialized in different basins
plt.plot(fmd_pc1, fmd_pc2, c='lightgray', alpha=0.8, lw=2, ls=':', zorder=1)
plt.plot(smd_pc1, smd_pc2, c='darkgray', alpha=0.8, lw=2, ls=':', zorder=1)


plt.tick_params(axis='both', which='both',
    bottom=False, top=False, right=False, left=False,
    labelbottom=False, labelleft=False)

plt.show()
