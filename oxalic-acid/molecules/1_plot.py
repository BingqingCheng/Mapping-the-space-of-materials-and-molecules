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

pcs = get_info_values('skpca-d-10', atoms)
energies = get_info_values('E_relative', atoms)


## Plotting (PC1 vs PC2)
fig, axl = plt.subplots()

# define limits for color-coding
ll, ul = np.min(energies), np.max(energies)

# MD which stays in its initial minimum (with transparency)
axl.scatter(pcs[12056:15056, 0], pcs[12056:15056, 1], c=energies[12056:15056],
            alpha=0.4, zorder=1, s=10, cmap='gnuplot', edgecolor='k', linewidths=0.2, vmin=ll, vmax=ul)
# remaining 6 MDs
axl.scatter(np.concatenate((pcs[56:12056, 0], pcs[15056:21056, 0])),
            np.concatenate((pcs[56:12056, 1], pcs[15056:21056, 1])),
            c=np.concatenate((energies[56:12056], energies[15056:21056])),
            alpha=1.0, zorder=1, s=10, cmap='gnuplot', edgecolor='k', linewidths=0.2, vmin=ll, vmax=ul)
# locally relaxed configurations
pcmm = axl.scatter(pcs[:56, 0], pcs[:56, 1],
                   zorder=2, s=50, c=energies[:56],
                   cmap='gnuplot', edgecolor='k', linewidths=0.2, vmin=ll, vmax=ul)
plt.colorbar(pcmm, ax=axl).set_label('Relative Energy / eV', rotation=270, labelpad=20)

# first step of MD starting from high energy configuration
axl.plot(pcs[18056:18058, 0], pcs[18056:18058, 1],
          alpha=0.8, c='darkgray', lw=2, ls=':', zorder=1)

plt.tick_params(axis='both', which='both',
    bottom=False, top=False, right=False, left=False,
    labelbottom=False, labelleft=False)

plt.show()
