import numpy as np
import matplotlib.pyplot as plt

casino_dz_v = np.genfromtxt('casino_1param2_variances_dz.dat',  unpack = True)
dz = np.genfromtxt('1param2-landscape_reverse_dz.dat', unpack = True)
tz = np.genfromtxt('1param2-landscape_reverse_tz.dat', unpack = True)
qz = np.genfromtxt('1param2-landscape_reverse_qz.dat', unpack = True)
cdz = np.genfromtxt('1param2-landscape_reverse_cdz.dat', unpack = True)
ctz = np.genfromtxt('1param2-landscape_reverse_ctz.dat', unpack = True)

plt.errorbar(casino_dz_v[0], casino_dz_v[1], yerr = casino_dz_v[2], marker = 'o', markersize = 2, lw = 0, elinewidth=1, capsize=2, label = 'CASINO DZ')

plt.plot(dz[0], dz[1], label = 'DZ')
plt.plot(tz[0], tz[1], label = 'TZ')
plt.plot(qz[0], qz[1], label = 'QZ')
plt.plot(cdz[0], cdz[1], label = 'CDZ')
plt.plot(ctz[0], ctz[1], label = 'CTZ')

plt.ylabel('Variance')
plt.xlabel('Parameter')

plt.yscale('log')
plt.legend()

plt.show()

plt.plot(dz[0], dz[2], label = 'DZ')
plt.plot(tz[0], tz[2], label = 'TZ')
plt.plot(qz[0], qz[2], label = 'QZ')
plt.plot(cdz[0], cdz[2], label = 'CDZ')
plt.plot(ctz[0], ctz[2], label = 'CTZ')
plt.hlines(-7.47806, -3, 3, 'k')

plt.ylabel('Energy')
plt.xlabel('Parameter')

plt.legend()

plt.show()
