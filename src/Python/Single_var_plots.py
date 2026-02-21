import matplotlib.pyplot as plt
import numpy as np
from Rt_q_dep import compute_stype_truncation_qdep as cst


# Function to recreate Figure C.1 from Manara et. al 2019
def fit_pp():
    q2_prim = [0.2, 0.4, 0.6, 0.8, 1.0]
    q2_sec = [1/2, 1/4, 1/6, 1/8, 1/10]
    Rt_divby_abin_prim = [0.45, 0.41, 0.37, 0.35, 0.33]
    Rt_divby_abin_sec = [0.28, 0.23, 0.21, 0.19, 0.18]
    q2 = np.linspace(0.001, 1, 1000)
    q1 = 1/q2
    mu = np.linspace(0.001, 0.5001, 1000)
    fit1 = cst(q1, q2, 0, 0, 1)
    fit2 = cst(q1, q2, 0, 0, 2)

    plt.figure(figsize=(14, 8))
    plt.xlabel(r"q = $M_2/M_1$", fontsize=34)
    plt.ylabel(r"$R_t/a_{bin}$", fontsize=34)
    plt.tick_params(axis='x', length=13, width=2.4, labelsize=26)
    plt.tick_params(axis='y', length=13, width=2.4, labelsize=26)
    plt.scatter(q2_prim, Rt_divby_abin_prim, c='blue', edgecolor='black', label="P&P (1977) values for circumprimary disc")
    plt.plot(q2, fit1, c='blue', label='Circumprimary fit')
    plt.scatter(q2_sec, Rt_divby_abin_sec, c='red', edgecolor='black', label="P&P (1977) values for circumsecondary disc")
    plt.plot(q2, fit2, c='red', label='Circumsecondary fit')
    plt.legend(fontsize=20, loc="best", markerscale=1.5, frameon=True, fancybox=True, edgecolor="black")

    plt.tight_layout()
    plt.savefig("Recreation_of_Manara_plot.pdf", format="pdf")
    plt.show()

def plot_bec_vs_R():
    mu = [0.1, 0.2, 0.3, 0.4, 0.5]  # Values of mu
    e = 0.5  # Chosen eccentricity

    # Coefficients for parameter b for different values of mu and R
    b1_p = [-0.66, -0.75, -0.78]
    b2_p = [-0.72, -0.78, -0.80]
    b3_p = [-0.76, -0.80, -0.81]
    b4_p = [-0.77, -0.81, -0.82]
    b5_p = [-0.78, -0.81, -0.82]
    b_p = [b1_p, b2_p, b3_p, b4_p, b5_p]

    # Coefficients for parameter c for different values of mu and R
    c1_p = [0.84, 0.68, 0.56]
    c2_p = [0.88, 0.72, 0.60]
    c3_p = [0.92, 0.75, 0.63]
    c4_p = [0.95, 0.78, 0.66]
    c5_p = [0.94, 0.78, 0.66]
    c_p = [c1_p, c2_p, c3_p, c4_p, c5_p]


    b1_s = [-0.81, -0.81, -0.83]
    b2_s = [-0.81, -0.82, -0.83]
    b3_s = [-0.79, -0.82, -0.83]
    b4_s = [-0.80, -0.82, -0.83]
    b5_s = [-0.79, -0.81, -0.82]

    b_s = [b1_s, b2_s, b3_s, b4_s, b5_s]

    c1_s = [0.98, 0.80, 0.69]
    c2_s = [0.99, 0.82, 0.70]
    c3_s = [0.97, 0.81, 0.69]
    c4_s = [0.98, 0.80, 0.68]
    c5_s = [0.95, 0.78, 0.66]

    c_s = [c1_s, c2_s, c3_s, c4_s, c5_s]

    R = [1e4, 1e5, 1e6]  

    fig, ax = plt.subplots(2, 1, figsize=(14, 10))

    colors = ['red', 'blue', 'green', 'purple', 'orange']

    for i, (mu_val, b_vals, c_vals) in enumerate(zip(mu, b_p, c_p)):
        bec_vals = [b * (e**c) for b, c in zip(b_vals, c_vals)]
        ax[0].plot(R, bec_vals, marker='o', color=colors[i], label=f'mu={mu_val}')

    for i, (mu_val, b_vals, c_vals) in enumerate(zip(mu, b_s, c_s)):
        bec_vals = [b * (e**c) for b, c in zip(b_vals, c_vals)]
        ax[1].plot(R, bec_vals, marker='o', color=colors[i], label=f'mu={mu_val}')

    # Customize the plot
    fig.supxlabel(r'Reynolds number ($\mathcal{R}$)', fontsize=28)
    fig.supylabel(r'$be^{c}$', fontsize=28)
    for i in range(2):
        ax[i].set_xscale('log')
        ax[i].legend(fontsize=18, loc="best", markerscale=1.5, frameon=True, fancybox=True, edgecolor="black")
        ax[i].tick_params(axis='x', length=10, width=2, labelsize=20)
        ax[i].tick_params(axis='y', length=10, width=2, labelsize=20)
    plt.savefig("bec(R)differentmu.pdf", format="pdf")
    plt.tight_layout()
    plt.show()


#fit_pp()
plot_bec_vs_R()
