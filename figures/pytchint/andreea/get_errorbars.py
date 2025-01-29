import numpy as np
import matplotlib.pyplot as plt

dtc = np.genfromtxt('out_det', unpack = True)
ctc = np.genfromtxt('out_casino', unpack = True)
dtcd = np.genfromtxt('out_det_dcsd', unpack = True)
ctcd = np.genfromtxt('out_casino_dcsd', unpack = True)
tc0 = np.genfromtxt('out_0', unpack=True)
tcd0 = np.genfromtxt('out_dcsd_0', unpack=True)

averages = []
errors = []

fig, ax = plt.subplots(2,1, figsize = (8,5))
for i in range(8):
    for j in range(5):
        averages.append(np.average(dtc[0][5*i:5*(i+1)]))
        errors.append(np.std(dtc[0][5*i:5*(i+1)]))
x = [3]*5 + [4]*5+[5]*5+[6]*5+[7]*5+[8]*5+[9]*5+[10]*5
x2 = [3,4,5,6,7,8,9,10]
av = [0]*8
av2 = [averages[5*i] for i in range(8)]
err = [errors[5*i] for i in range(8)]
ax[1].errorbar(x2, av, yerr=err)
ax[1].plot(x, dtc[0]-np.array(averages), 'o')
ax[1].plot(x2, tc0[1]-np.array(av2), 'o')
ax[1].set_ylim(-0.00038, 0.00025)
ax[1].set_ylabel(r'$E-\langle E\rangle$')
ax[1].set_xlabel(r'$Z$')

averages = []
errors = []

for i in range(8):
    for j in range(5):
        averages.append(np.average(ctc[0][5*i:5*(i+1)]))
        errors.append(np.std(ctc[0][5*i:5*(i+1)]))

err = [errors[5*i] for i in range(8)]
ax[0].errorbar(x2, av, yerr=err)
ax[0].plot(x, ctc[0]-np.array(averages), 'o')
print(min(ctc[0]-np.array(averages)))
ax[0].set_ylim(-0.00038, 0.00025)
ax[0].set_ylabel(r'$E-\langle E\rangle$')
plt.savefig('TC_comp.svg')
plt.show()

averages = []
errors = []
fig, ax = plt.subplots(2,1, figsize = (8,5))
for i in range(8):
    for j in range(5):
        averages.append(np.average(dtcd[0][5*i:5*(i+1)]))
        errors.append(np.std(dtcd[0][5*i:5*(i+1)]))
err = [errors[5*i] for i in range(8)]
av2 = [averages[5*i] for i in range(8)]
ax[1].errorbar(x2, av, yerr=err)
ax[1].plot(x, dtcd[0]-np.array(averages), 'o')
ax[1].plot(x2, tcd0[1]-np.array(av2), 'o')
ax[1].set_ylim(-0.0001, 0.0001)
ax[1].set_ylabel(r'$E-\langle E\rangle$')
ax[1].set_xlabel(r'$Z$')

averages = []
errors = []

for i in range(8):
    for j in range(5):
        averages.append(np.average(ctcd[0][5*i:5*(i+1)]))
        errors.append(np.std(ctcd[0][5*i:5*(i+1)]))
err = [errors[5*i] for i in range(8)]
ax[0].errorbar(x2, av, yerr=err)
ax[0].plot(x, ctcd[0]-np.array(averages), 'o')
ax[0].set_ylim(-0.0001, 0.0001)
ax[0].set_ylabel(r'$E-\langle E\rangle$')
plt.savefig('TCDCSD_comp.svg')
plt.show()

ip_ctc = ctc[1] - ctc[0]
ip_ctcd = ctcd[1] - ctcd[0]
ip_dtc = dtc[1] - dtc[0]
ip_dtcd = dtcd[1] - dtcd[0]

first_row_atoms = [-7.47806,-14.66736, -24.65391,-37.8450, -54.5892, -75.0673, -99.7339, -128.9376]
first_row_ions = [-7.279913, -14.32476,-24.34892,-37.43103, -54.0546,-74.5668, -99.0928, -128.1431]
ips = [first_row_ions[i] - first_row_atoms[i] for i in range(8)]
x2 = np.array(x2)
averages = []
errors = []
for i in range(8):
    averages.append(np.average(ip_ctc[5*i:5*(i+1)]))
    errors.append(np.std(ip_ctc[5*i:5*(i+1)]))
averages = np.array(averages)
plt.bar(x2 - 0.5, averages - ips, width = 0.2, align = 'edge', label = 'CASINO')
averages = []
errors = []
for i in range(8):
    averages.append(np.average(ip_dtc[5*i:5*(i+1)]))
    errors.append(np.std(ip_dtc[5*i:5*(i+1)]))
averages = np.array(averages)

plt.bar(x2 - 0.3, averages - ips, width = 0.2, align = 'edge', label = 'Deterministic')
averages = []
errors = []
for i in range(8):
    averages.append(np.average(ip_ctcd[5*i:5*(i+1)]))
    errors.append(np.std(ip_ctcd[5*i:5*(i+1)]))
averages = np.array(averages)

plt.bar(x2-0.1, averages - ips, width = 0.2, align = 'edge', label = 'CASINO+DCSD')
averages = []
errors = []
for i in range(8):
    averages.append(np.average(ip_dtcd[5*i:5*(i+1)]))
    errors.append(np.std(ip_dtcd[5*i:5*(i+1)]))
averages = np.array(averages)
plt.bar(x2 + 0.1, averages - ips, width = 0.2, align = 'edge', label = 'Deterministic + DCSD')
plt.bar(x2 + 0.3, tcd0[0]-tcd0[1] - ips, width = 0.2, align = 'edge', label = 'Deterministic from 0 + DCSD')
plt.legend()
plt.savefig('IPS.svg')
plt.show()


