import matplotlib.pyplot as plt
n2 = -109.543481
f2 = -199.532431
o2 = -150.328884
f = -99.735148
n = -54.589743
o = -75.06821

n2_dcsd_det = -109.523310770918
f2_dcsd_det = -199.494708097849
o2_dcsd_det = -150.255911359709

n_dcsd_det = -54.583911019661
f_dcsd_det = -99.713946519588
o_dcsd_det = -75.054407934764

n2_dcsd_cas = -109.521213152102
f2_dcsd_cas = -199.486845116260
o2_dcsd_cas = -150.249152734208

n_dcsd_cas = -54.582967616710
o_dcsd_cas = -75.052848203571
f_dcsd_cas = -99.711530140254

fig, ax = plt.subplots(2,3, figsize = (12,4))

ax[0][0].bar([1,2,3], [n2_dcsd_cas-n2, o2_dcsd_cas-o2, f2_dcsd_cas-f2])
ax[1][0].bar([1,2,3], [n2_dcsd_det-n2, o2_dcsd_det-o2, f2_dcsd_det-f2])
ax[0][1].bar([1,2,3], [n_dcsd_cas-n, o_dcsd_cas-o, f_dcsd_cas-f])
ax[1][1].bar([1,2,3], [n_dcsd_cas-n, o_dcsd_cas-o, f_dcsd_cas-f])
ax[0][2].bar([1,2,3], [n2_dcsd_cas-2*n_dcsd_cas-n2+2*n, o2_dcsd_cas-2*o_dcsd_cas-o2+2*o,f2_dcsd_cas-2*f_dcsd_cas-f2+2*f])
ax[1][2].bar([1,2,3], [n2_dcsd_det-2*n_dcsd_det-n2+2*n, o2_dcsd_det-2*o_dcsd_det-o2+2*o,f2_dcsd_det-2*f_dcsd_det-f2+2*f])
ax[1][0].set_xticks([1,2,3])
ax[1][1].set_xticks([1,2,3])
ax[1][2].set_xticks([1,2,3])
ax[0][0].set_xticks([1,2,3])
ax[0][1].set_xticks([1,2,3])
ax[0][2].set_xticks([1,2,3])
ax[1][0].set_xticklabels(['N2', 'O2', 'F2'])
ax[1][1].set_xticklabels(['N', 'O', 'F'])
ax[1][2].set_xticklabels(['N2', 'O2', 'F2'])
ax[0][0].set_xticklabels(['N2', 'O2', 'F2'])
ax[0][1].set_xticklabels(['N', 'O', 'F'])
ax[0][2].set_xticklabels(['N2', 'O2', 'F2'])
ax[0][0].set_ylabel(r'$\Delta E$')
ax[1][0].set_ylabel(r'$\Delta E$')
plt.savefig('heat.svg')
plt.show()
