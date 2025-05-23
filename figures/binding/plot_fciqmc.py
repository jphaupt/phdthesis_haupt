# %%
import numpy as np
import re
import matplotlib.pyplot as plt
import logging

# %%
# def parse_uncertainty(value_with_uncertainty: str) -> tuple[float, float]:
#     """
#     Parses a string representing a float with uncertainty in the format
#     `value(uncertainty)`

#     Args:
#         value_with_uncertainty (str): A string containing a value with
#             uncertainty, e.g., '1.1(2)'.

#     Returns:
#         tuple[float, float]:
#             - The numerical value as a float.
#             - The uncertainty as a float.

#     Raises:
#         ValueError: If the input string is not in the correct format.

#     Example:
#         >>> parse_uncertainty("1.1(2)")
#         (1.1, 0.2)
#     """
#     check = re.fullmatch(r"(-?[\d.]+)\((\d+)\)", value_with_uncertainty)
#     if not check:
#         raise ValueError("Input must be in the format 'value(uncertainty)', e.g. 1.1(2)")

#     value = float(check.group(1))
#     uncertainty_digits = check.group(2)
#     uncertainty = float(uncertainty_digits) * 10**(-len(check.group(1).split('.')[-1]))
#     return value, uncertainty

# assert parse_uncertainty("1.1(2)") == (1.1, 0.2)

# # %%
# def load_data_with_uncertainties(file_path: str, uncertainty_cols: list[int]) -> np.ndarray:
#     data = np.genfromtxt(file_path, dtype=str)
#     processed_data = []
#     for i, col in enumerate(data.T): # iterate over columns
#         if i in uncertainty_cols:
#             parsed_vals = []
#             for val in col:
#                 if val.lower() == 'nan':
#                     parsed_vals.append((np.nan, np.nan))
#                 else:
#                     parsed_vals.append(parse_uncertainty(val))
#             parsed_vals = np.array(parsed_vals)
#             processed_data.append(parsed_vals[:, 0]) # values
#             processed_data.append(parsed_vals[:, 1]) # uncertainties
#         else:
#             processed_data.append(np.where(col == 'nan', np.nan, col.astype(float)))

#     processed_data = np.column_stack(processed_data)
#     # sort based on first column
#     return processed_data[processed_data[:,0].argsort()]

import numpy as np
import uncertainties
from uncertainties import ufloat_fromstr

def load_data_with_uncertainties(file_path: str, uncertainty_cols: list[int]) -> np.ndarray:
    # print(file_path)
    data = np.genfromtxt(file_path, dtype=str)
    # print(data)
    processed_data = []
    for i, col in enumerate(data.T): # iterate over columns
        if i in uncertainty_cols:
            parsed_vals = []
            for val in col:
                if val.lower() == 'nan':
                    parsed_vals.append(ufloat_fromstr("nan"))
                else:
                    parsed_vals.append(ufloat_fromstr(val))
            processed_data.append(np.array(parsed_vals))
            # parsed_vals = np.array(parsed_vals)
            # processed_data.append(parsed_vals[:, 0]) # values
            # processed_data.append(parsed_vals[:, 1]) # uncertainties
        else:
            processed_data.append(np.where(col == 'nan', np.nan, col.astype(float)))

    processed_data = np.column_stack(processed_data)
    # sort based on first column
    return processed_data[processed_data[:,0].argsort()]

# %%
data_all = [
            # "N2_avdz_fciqmc.dat",
            # "N2_avqz_fciqmc.dat",
            "N2_avtz_rhf.dat",
            "N2_avtz_casci.dat",
            "N2_avtz_casscf.dat",
            "N2_avtz_fciqmc.dat"
            ]
data_f12_all = [
                # "N2_avqz_f12.dat",
                "N2_avtz_f12.dat",
                # "N2_avtz_dcsdf12.dat"
                ]
data_exp = np.genfromtxt('experiment.dat')

# %%

# for data_name in data_all:
#     data = load_data_with_uncertainties(data_name, [1])
#     data_name = data_name.split("_")[-1].split(".")[0].upper()
#     plt.plot(data[:,0], data[:,1], 'o-', label=f"{data_name}-Jastrow")
#     # plt.plot(data[:,0], data[:,-1], 's-', label=data_name+"_dcsd")
# for data_name in data_f12_all:
#     data = np.genfromtxt(data_name)
#     plt.plot(data[:,0], data[:,-1], 'd-', label="MRCI-F12", markerfacecolor='none')
# plt.legend()
# plt.ylim(-109.190, -109.175)
# plt.xlim(left=4)
# # plt.plot(data_exp[:,0], data_exp[:,1], 'k-', label='Experiment')
# # plt.savefig("binding_curves.pdf")
# plt.show()
# plt.close()

# %%
# plot_comp2exp = lambda x,t: plt.errorbar(data_exp[:,0], [1000*x.n for x in comp2exp(x)], yerr=[1000*x.s for x in comp2exp(x)], fmt='.-', label=t)
comp2exp = lambda x: (x - x[-1]) - (data_exp[:,1] - data_exp[-1,1])
plot_comp2exp = lambda x,t: plt.errorbar(data_exp[:,0], [1000*x.n for x in comp2exp(x)], yerr=[1000*x.s for x in comp2exp(x)], fmt='.-', label=t)
for data_name in data_all:
    print(data_name)
    data = load_data_with_uncertainties(data_name, [1])
    data_name = data_name.split("_")[-1].split(".")[0].upper()
    residuals = (data[:,1]-data[-1,1]) - (data_exp[:,1]-data_exp[-1,1])
    # plt.plot(data_exp[:,0], residuals, 'o-', label=f"{data_name}-Jastrow")
    plot_comp2exp(data[:,1], f"{data_name}-Jastrow")
    residuals = (data[:,-1]-data[-1,-1]) - (data_exp[:,1]-data_exp[-1,1])
    # plt.plot(data_exp[:,0], residuals, 's-', label=data_name+"_dcsd")
for data_name in data_f12_all:
    # remove last 2 points from f12 data because they are bad
    data = np.genfromtxt(data_name)
    residuals = (data[:-2,-1]-data[-3,-1]) - (data_exp[:-2,1]-data_exp[-3,1])
    plt.plot(data_exp[:-2,0], 1000*residuals, 'd-', label="MRCI-F12", markerfacecolor='none', zorder=1)
data_nontc = np.genfromtxt("N2_nontcfciqmc_bind_avtz.dat")
residuals = (data_nontc[:,1]-data_nontc[-1,1]) - (data_exp[:,1]-data_exp[-1,1])
# plt.plot(data_exp[:,0], residuals, '^-', label="Non-TC-FCIQMC", zorder=1)
# plt.grid(True, which="both", ls="--")
# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
plt.legend()
xlim = plt.xlim()
ylim = plt.ylim()
plt.fill_between([min(data_exp[:,0])-10, max(data_exp[:,0])+10], -1.6, 1.6, alpha=0.2, color='k')
plt.axline((-100,0), (100,0), color='k', linestyle='--', linewidth=0.5)
plt.xlim(xlim)
plt.ylim(ylim)
plt.ylim(top=8)
plt.ylabel(r"$E-E_\mathrm{exp}$ (mHa)")
plt.xlabel(r"Interatomic Distance (Bohr)")
plt.savefig("residuals.pdf", bbox_inches='tight')
plt.show()
plt.close()


# # %%
# for data_name in data_f12_all:
#     # remove last 2 points from f12 data because they are bad
#     data = np.genfromtxt(data_name)
#     residuals = (data[:-2,-1]-data[2,-1]) - (data_exp[:-2,1]-data_exp[2,1])
#     plt.plot(data_exp[:-2,0], residuals, 'd-', label=data_name)
# for data_name in data_all:
#     data = load_data_with_uncertainties(data_name, [1])
#     residuals = (data[:,1]-data[2,1]) - (data_exp[:,1]-data_exp[2,1])
#     # plt.plot(data_exp[:,0], residuals, 'o-', label=data_name)
#     residuals = (data[:,-1]-data[2,-1]) - (data_exp[:,1]-data_exp[2,1])
#     plt.plot(data_exp[:,0], residuals, '^-', label=data_name+"_dcsd")
# plt.grid(True, which="both", ls="--")
# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
# plt.fill_between([min(data_exp[:,0]), max(data_exp[:,0])], -0.0016, +0.0016, alpha=0.2, color='k')
# plt.savefig("residuals_zeroedminimum.pdf", bbox_inches='tight')
# plt.close()
