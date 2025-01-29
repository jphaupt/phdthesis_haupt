# N2 Excited State Data

TODO: NH3 data

/algpfs1/phaupt/neci/spin-gaps/standard_fciqmc/fixparity2024

## CASCI-Jastrow
### Absolute Energies

asterisk indicates calculation needs further inspection (e.g. larger walker number)
double asterisk means it's been rerun with trial wave functions
**NOTE: I will also want to run these with trial wave functions to be more sure!

| state  | avdz             | avtz             |
| ------ | ---------------- | ---------------- |
| gs     | -109.4869509(85) | -109.534973(17)* |
| 1Pig   | -109.145116(82)  | -109.19543(16)** |
| 1Sigu- | -109.12030(20)   |                  |
| 1Delu  | -109.107187(52)  |                  |
| 3Sigu+ | -109.201567(40)  |                  |
| 3Pig   | -109.192041(41)  |                  |
| 3Delu  | -109.156050(34)  |                  |

### Excited State Energies

TODO
- [ ] remember to also include data from Loos et al table 2
- [ ] also include experimental data
- [ ] also include exFCI data

**NOTE: this table is in mHa

double asterisk indicates wrong state being targeted (most likely)

| state  | avdz  | avtz  | Loos avdz | Loos avtz | exFCI avqz | exp   |
| ------ | ----- | ----- | --------- | --------- | ---------- | ----- |
| 1Pig   | 341.8 | 339.5 | 345.8     |           | 343.2      | 342.1 |
| 1Sigu- | 366.7 |       | 369.3     |           | 364.6      |       |
| 1Delu  | 379.8 |       | 383.3     |           | 378.9      |       |
| 3Sigu+ | 285.4 |       | 283       |           | 284.8      |       |
| 3Pig   | 294.9 |       | 295.8     |           | 295.1      |       |
| 3Delu  | 330.9 |       | 329.3     |           | 326.3      |       |

## CASSCF-Jastrow
