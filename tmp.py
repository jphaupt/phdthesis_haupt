import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

# Define the max truncation order we want to support
N_max = 30

# Precompute a_mn for m, n in [0, N_max)
a_mn_table = np.zeros((N_max, N_max))

for m in range(N_max):
    for n in range(N_max):
        integrand = lambda y, x: np.sqrt(x**2 + y**2) * np.cos(m * np.pi * x) * np.cos(n * np.pi * y)
        a_mn, _ = dblquad(integrand, -1, 1, lambda _: -1, lambda _: 1)
        # Normalize coefficients since cosine basis is not orthonormal on [-1,1]
        norm = (1 if m == 0 else 0.5) * (1 if n == 0 else 0.5)
        a_mn_table[m, n] = a_mn * norm

# Fast evaluation using precomputed coefficients
def fast_cosine_expansion(x, y, N):
    result = 0.0
    for m in range(N):
        for n in range(N):
            result += a_mn_table[m, n] * np.cos(m * np.pi * x) * np.cos(n * np.pi * y)
    return result

# Vectorized evaluation for a cross section
def f_N_cross_section_fast(x_vals, N):
    return np.array([fast_cosine_expansion(x, 0.0, N) for x in x_vals])

# Evaluate and plot again
x_vals = np.linspace(-1, 1, 200)
f_true = np.abs(x_vals)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, f_true, label='Original $f(x, 0) = |x|$', linewidth=2)

for N in [1, 3, 5, 10, 20, 30]:
    f_approx = f_N_cross_section_fast(x_vals, N)
    plt.plot(x_vals, f_approx, label=f'N = {N}')

plt.title('Approximation of $f(x, y) = \sqrt{x^2 + y^2}$ along $y=0$')
plt.xlabel('x')
plt.ylabel('f(x, 0)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
