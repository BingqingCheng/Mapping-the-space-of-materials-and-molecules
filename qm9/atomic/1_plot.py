import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import ase.io


def get_arrays(key, atoms):
    """Return a long ndarray of arrays stored under atoms_i.arrays[`key`]."""
    arrays = atoms[0].arrays[key]
    for atoms_i in atoms[1:]:
        arrays = np.concatenate((arrays, atoms_i.arrays[key]))
    return arrays


## Collect the data
qm9_1E4 = ase.io.read('ASAP-lowD-map.xyz', ':')

pcs = get_arrays('pca-d-10', qm9_1E4)
pc1, pc2 = pcs[:, 0], pcs[:, 1]

properties = {
        'charge': get_arrays('mulliken_charges', qm9_1E4),
        'hybridization': get_arrays('hybridization', qm9_1E4),
        'in_ring': get_arrays('in_ring', qm9_1E4)*1,            # NOTE: times one converts booleans to integers
        }


## Prepare data for plotting

# remove non-C entries (which all have NaN as PC)
del1, del2 = np.where(np.isnan(pc1))[0], np.where(np.isnan(pc2))[0]
assert np.array_equal(del1, del2)

pc1 = np.delete(pc1, del1)
pc2 = np.delete(pc2, del1)
for key_i, val_i in properties.items():
    properties[key_i] = np.delete(val_i, del1)



## Plotting

# Mulliken Charges
plt.scatter(pc1, pc2, c=properties['charge'],
            cmap='gnuplot',
            edgecolor='k', linewidths=0.2)
cbar = plt.colorbar()
cbar.set_label('Mulliken Charges / C', rotation=270, labelpad=20)
plt.tick_params(axis='both', which='both',
                bottom=False, top=False, right=False, left=False,
                labelbottom=False, labelleft=False)
plt.show()

# Hybridization
plt.scatter(pc1, pc2, c=properties['hybridization'],
            cmap=mpl.colors.ListedColormap(['lightgreen', 'royalblue', 'gray']),
            edgecolor='k', linewidths=0.2)
cbar = plt.colorbar()
cbar.set_label('Hybridization', rotation=270, labelpad=20)
cbar.set_ticks([1, 2, 3])
cbar.set_ticklabels(['sp', 'sp$^{2}$', 'sp$^{3}$'])
plt.clim(0.5, 3.5)
plt.tick_params(axis='both', which='both',
                bottom=False, top=False, right=False, left=False,
                labelbottom=False, labelleft=False)
plt.show()

# In Ring
plt.scatter(pc1, pc2, c=properties['in_ring'],
            cmap=mpl.colors.ListedColormap(['lightgreen', 'gray']),
            edgecolor='k', linewidths=0.2)
cbar = plt.colorbar()
cbar.set_label('Is in Ring', rotation=270, labelpad=20)
cbar.set_ticks([0, 1])
cbar.set_ticklabels(['No', 'Yes'])
plt.clim(-0.5, 1.5)
plt.tick_params(axis='both', which='both',
                bottom=False, top=False, right=False, left=False,
                labelbottom=False, labelleft=False)
plt.show()
