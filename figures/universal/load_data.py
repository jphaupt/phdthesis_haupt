import numpy as np
import uncertainties
from uncertainties import ufloat_fromstr

def load_data_with_uncertainties(file_path: str, uncertainty_cols: list[int]) -> np.ndarray:
    data = np.genfromtxt(file_path, dtype=str)
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

import pandas as pd

from uncertainties import unumpy
from uncertainties import ufloat, ufloat_fromstr
from uncertainties.core import UFloat
from math import isnan

def format_ufloat(x):
    if isinstance(x, type(ufloat(1, 1))):
        return f"{x:+.1uS}"  # Uses the shorthand format
    return x

def col2ufloat(col):
    return [ufloat_fromstr("nan") if pd.isna(x) else ufloat_fromstr(x) for x in col]

def display_formatted(df):
    # Create a copy to avoid modifying original
    display_df = df.copy()

    # Format ufloat columns
    for col in df.columns:
        if isinstance(df[col].iloc[0], UFloat):
            display_df[col] = df[col].apply(lambda x: f"{x:+.1uS}")

    display(display_df)

def get_system_values(filename):
    # read in data
    df = pd.read_csv(filename, comment='#', skipinitialspace=True)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x) # strip data
    df.rename(columns=lambda x: x.strip(), inplace=True) # strip headers too

    # handle NaNs as ufloats as well
    df["vdz"] = col2ufloat(df["vdz"])
    df["vtz"] = col2ufloat(df["vtz"])

    if "vqz" in df.columns: df["vqz"] = col2ufloat(df["vqz"])

    # display_formatted(df)

    # Get gs values as a series
    # gs_values = df[df['state'] == 'gs'].iloc[0]
    # display(gs_values)

    # Create new dataframe excluding gs
    # diff_df = df[df['state'] != 'gs'].reset_index(drop=True).copy()

    # cols_to_diff = df.columns[1:]  # All columns except first
    # for col in cols_to_diff:
    #     # display(diff_df[col])
    #     # display(gs_values[col])
    #     diff_df[col] = diff_df[col] - gs_values[col]
    # for col in diff_df.columns[1:]:
    #     diff_df[col] *= 1000
    # # display_formatted(diff_df)

    return df
    # type(df["avdz"][1])
