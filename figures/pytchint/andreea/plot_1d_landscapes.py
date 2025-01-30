import numpy as np
import matplotlib.pyplot as plt

casino_dz_v = np.genfromtxt('casino_1param_variances_dz.dat',  unpack = True)
casino_ctz_v = np.genfromtxt('casino_1param_variances.dat',  unpack = True)
casino_dz_e = np.genfromtxt('casino_1param_energies_dz.dat',  unpack = True)
casino_ctz_e = np.genfromtxt('casino_1param_energies.dat',  unpack = True)
dz = np.genfromtxt('1param-landscape_reverse_dz.dat', unpack = True)
tz = np.genfromtxt('1param-landscape_reverse_tz.dat', unpack = True)
qz = np.genfromtxt('1param-landscape_reverse_qz.dat', unpack = True)
cdz = np.genfromtxt('1param-landscape_reverse_cdz.dat', unpack = True)
ctz = np.genfromtxt('1param-landscape_reverse_ctz.dat', unpack = True)

fig, ax = plt.subplots(2,2)

ax[0][0].errorbar(casino_dz_v[0][::10], casino_dz_v[1][::10], yerr = casino_dz_v[2][::10], marker = 'o', markersize = 2, lw = 0, elinewidth=1, capsize=2, label = 'CASINO DZ')
ax[0][0].errorbar(casino_ctz_v[0][::2], casino_ctz_v[1][::2], yerr = casino_ctz_v[2][::2], marker='s',markersize = 2,lw = 0, elinewidth=1, capsize=2, label = 'CASINO CTZ')

ax[0][0].plot(dz[0], dz[1], label = 'DZ')
ax[0][0].plot(tz[0], tz[1], label = 'TZ')
ax[0][0].plot(qz[0], qz[1], label = 'QZ')
ax[0][0].plot(cdz[0], cdz[1], label = 'CDZ')
ax[0][0].plot(ctz[0], ctz[1], label = 'CTZ')

ax[0][0].set_ylabel(r'$\sigma^2_\mathrm{ref}$/Hartree$^2$')
ax[0][0].set_xlabel(r'$c_{ee}$')

ax[0][0].set_yscale('log')

ax[1][0].errorbar(casino_dz_e[0][::10], casino_dz_e[1][::10], yerr = casino_dz_e[2][::10], marker = 'o', markersize = 2, lw = 0, elinewidth=1, capsize=2, label = 'cc-pVDZ VMC')
ax[1][0].errorbar(casino_ctz_e[0][::2], casino_ctz_e[1][::2], yerr = casino_ctz_e[2][::2], marker='s',markersize = 2,lw = 0, elinewidth=1, capsize=2, label = 'cc-pCVTZ VMC')

ax[1][0].plot(dz[0], dz[2], label = 'cc-pVDZ')
ax[1][0].plot(tz[0], tz[2], label = 'cc-pVTZ')
ax[1][0].plot(qz[0], qz[2], label = 'cc-pVQZ')
ax[1][0].plot(cdz[0], cdz[2], label = 'cc-pCVDZ')
ax[1][0].plot(ctz[0], ctz[2], label = 'cc-pCVTZ')
ax[1][0].hlines(-7.47806, -3, 3, 'k', label = 'Exact')

ax[1][0].set_ylabel(r'$E_\mathrm{ref}$/Hartree')
ax[1][0].set_xlabel(r'$c_{ee}$')

ax[1][0].legend(fontsize=8)
casino_dz_v = np.genfromtxt('casino_1param2_variances_dz.dat',  unpack = True)
casino_dz_e = np.genfromtxt('casino_1param2_energies_dz.dat',  unpack = True)
dz = np.genfromtxt('1param2-landscape_reverse_dz.dat', unpack = True)
tz = np.genfromtxt('1param2-landscape_reverse_tz.dat', unpack = True)
qz = np.genfromtxt('1param2-landscape_reverse_qz.dat', unpack = True)
cdz = np.genfromtxt('1param2-landscape_reverse_cdz.dat', unpack = True)
ctz = np.genfromtxt('1param2-landscape_reverse_ctz.dat', unpack = True)

ax[0][1].errorbar(casino_dz_v[0], casino_dz_v[1], yerr = casino_dz_v[2], marker = 'o', markersize = 2, lw = 0, elinewidth=1, capsize=2, label = 'CASINO DZ')

# next(ax[0, 1].figure._get_default_prop_cycle())
ax[0,1]._get_lines.get_next_color()

ax[0][1].plot(dz[0], dz[1], label = 'DZ')
ax[0][1].plot(tz[0], tz[1], label = 'TZ')
ax[0][1].plot(qz[0], qz[1], label = 'QZ')
ax[0][1].plot(cdz[0], cdz[1], label = 'CDZ')
ax[0][1].plot(ctz[0], ctz[1], label = 'CTZ')

ax[0][1].set_ylabel(r'$\sigma^2_\mathrm{ref}$/Hartree$^2$')
ax[0][1].set_xlabel(r'$c_{en}$')

ax[0][1].set_yscale('log')

ax[1][1].errorbar(casino_dz_e[0], casino_dz_e[1], yerr = casino_dz_e[2], marker = 'o', markersize = 2, lw = 0, elinewidth=1, capsize=2, label = 'CASINO DZ')
# next(ax[1, 1].figure._get_default_prop_cycle())
ax[1,1]._get_lines.get_next_color()
ax[1][1].plot(dz[0], dz[2], label = 'DZ')
ax[1][1].plot(tz[0], tz[2], label = 'TZ')
ax[1][1].plot(qz[0], qz[2], label = 'QZ')
ax[1][1].plot(cdz[0], cdz[2], label = 'CDZ')
ax[1][1].plot(ctz[0], ctz[2], label = 'CTZ')
ax[1][1].hlines(-7.47806, -3, 3, 'k')

ax[1][1].set_ylabel(r'$E_\mathrm{ref}$/Hartree')
ax[1][1].set_xlabel(r'$c_{en}$')

ax[0][1].sharey(ax[0][0])
ax[1][1].sharey(ax[1][0])
plt.tight_layout()
plt.savefig('1parameter.pdf')
plt.show()
