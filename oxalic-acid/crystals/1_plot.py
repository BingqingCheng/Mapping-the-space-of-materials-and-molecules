import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

import ase.io


def get_info_values(key, atoms):
    """Return a ndarray with values stored under atoms_i.info[`key`]."""
    values = [atoms_i.info[key] for atoms_i in atoms]
    return np.asarray(values)


## Collect the data
atoms = ase.io.read('ASAP-lowD-map.xyz', ':')
rig_crys = atoms[:48]
fullopt_crys = atoms[48:]

rcrys_pcs = get_info_values('pca-d-10', rig_crys)
focrys_pcs = get_info_values('pca-d-10', fullopt_crys)

rcrys_pc1, rcrys_pc2 = rcrys_pcs[:, 0], rcrys_pcs[:, 1]
focrys_pc1, focrys_pc2 = focrys_pcs[:, 0], focrys_pcs[:, 1]

rcrys_energies = get_info_values('E_aims_mbd_relative', rig_crys)
focrys_energies = get_info_values('E_aims_mbd_relative', fullopt_crys)
energies = np.concatenate([rcrys_energies, focrys_energies])


## Plotting

# rigid and relaxed crystals
cmap = 'gnuplot'
cmin, cmax = energies.min(), 0.25*energies.max()  # we focus on the  low energy range

plt.scatter(rcrys_pc1, rcrys_pc2,
            cmap=cmap, vmin=cmin, vmax=cmax, edgecolor='k', linewidths=0.2,
            label='Initial Crystal Structures',
            zorder=2, s=20, c=rcrys_energies)
plt.scatter(focrys_pc1, focrys_pc2,
            cmap=cmap, vmin=cmin, vmax=cmax, edgecolor='k', linewidths=0.2,
            label='Relaxed Crystal Structures',
            zorder=3, s=80, c=focrys_energies)

plt.colorbar().set_label('Relative Energy / eV', rotation=270, labelpad=20)

# intersections between rigid crystals and its relaxed counterpart
for idx_i in range(48):
    plt.plot([rcrys_pc1[idx_i], focrys_pc1[idx_i]],
             [rcrys_pc2[idx_i], focrys_pc2[idx_i]],
             ls=':', lw=0.8, c='gray', zorder=1)


leg = plt.legend()
for handle in leg.legendHandles:
    handle.set_color('white')
    handle.set_edgecolor('black')
    handle.set_linewidth('0.2')

plt.tick_params(
    axis='both', which='both',
    bottom=False, top=False, right=False, left=False,
    labelbottom=False, labelleft=False)

plt.show()
