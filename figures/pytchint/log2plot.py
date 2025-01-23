import numpy as np
import matplotlib.pyplot as plt
import sys

def read_data(file_path):
    """
    Reads a file with two columns of integers, ignoring lines starting with '#'.

    Args:
        file_path (str): Path to the input file.

    Returns:
        np.ndarray: Array of x values (first column).
        np.ndarray: Array of y values (second column).
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                x, y = map(int, line.split())
                data.append((x, y))
            except ValueError:
                print(f"Skipping invalid line: {line}")

    data = np.array(data)
    return data[:, 0], data[:, 1]

def plot_log2_x_axis(x, y):
    """
    Plots the first column (x) against the second column (y) with a log2 x-axis.

    Args:
        x (np.ndarray): Array of x values.
        y (np.ndarray): Array of y values.
    """
    plt.figure(figsize=(8, 6))
    plt.axvline(x=2**7, color='k', linestyle='--', label='x=2^7')
    plt.plot(x, y/60, marker='o', linestyle='-', label='Data')
    plt.xscale('log', base=2)
    plt.xlabel('Number of Cores')
    plt.ylabel('Elapsed Real Time (Min)')
    # plt.title('Plot of Y vs X (log2 scale for X)')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    # plt.legend()
    plt.show()

def main():
    """
    Main function to read the file, parse data, and plot it.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        x, y = read_data(file_path)
        plot_log2_x_axis(x, y)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
