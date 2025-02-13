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
