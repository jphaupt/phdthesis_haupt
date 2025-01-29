import numpy as np
import matplotlib.pyplot as plt

f2 = np.genfromtxt('var_F2.dat', unpack = True, usecols = (0,1))
n2 = np.genfromtxt('var_N2.dat', unpack = True, usecols = (0,1))
o2 = np.genfromtxt('var_O2.dat', unpack = True, usecols = (0,1))

fig, ax = plt.subplots(2,3, figsize = (15,6))

ax[0][0].plot(range(len(f2[0])), f2[0])
ax[0][1].plot(range(len(n2[0])), n2[0])
ax[0][2].plot(range(len(o2[0])), o2[0])
ax[1][0].plot(range(len(f2[1])), f2[1])
ax[1][1].plot(range(len(n2[1])), n2[1])
ax[1][2].plot(range(len(o2[1])), o2[1])

ax[1][0].set_ylabel('Energy')
ax[0][0].set_ylabel('Variance')

ax[1][0].set_xlabel('Iteration')
ax[1][1].set_xlabel('Iteration')
ax[1][2].set_xlabel('Iteration')
ax[1][2].set_yticks([-149.91, -149.90, -149.89])
ax[0][0].set_title('F2')
ax[0][1].set_title('N2')
ax[0][2].set_title('O2')
plt.savefig('trajectories.png')
plt.show()
