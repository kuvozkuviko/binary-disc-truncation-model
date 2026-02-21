import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from Rt_no_input import compute_stype_truncation_no_input as cs_trunc_ni
from Rt_fixed_mu import compute_stype_truncation_fixed_mu as cs_trunc_mu
from Rt_abin_dep import compute_stype_truncation_abin_dep as cst_abin
from matplotlib.colors import LogNorm
from matplotlib import cm
from matplotlib.legend_handler import HandlerPathCollection
from matplotlib.lines import Line2D
from scipy.optimize import minimize

# Define arrays for different variables
mu = np.arange(0.005, 0.5005, 0.005)  # Mass parameter range
q = mu / (1 - mu)  # Mass ratio based on mu
e = np.arange(0, 1, 0.01)  # Eccentricity range
a_bin = np.arange(1, 1001, 10)  # Binary separation range in AU
alpha = np.linspace(1e-4, 1e-3, 100)  # Viscosity alpha range

# Set color map for plotting
cmap = cm.viridis
norm_abin = LogNorm(vmin=min(a_bin), vmax=max(a_bin), clip=False)  # Normalization for binary separation
colours_abin = cmap(norm_abin(a_bin))  # Colors for a_bin
norm_e = LogNorm(vmin=0.001, vmax=max(e), clip=False)  # Normalization for eccentricity
colours_e = cmap(norm_e(e))  # Colors for eccentricity

# Constant values for the parameters
ac = 100 # Binary separation
qc = 0.5 # Mass ratio
muc = qc / (1 + qc)  # Compute mass parameter from mass ratio
ec = 0.5 # Eccentricity
alphac = 1e-3 # Viscosity alpha

# Function to plot R_t/a_bin as a function of q, e, and alpha individually while keeping the other parameters constant
def plot_for_variables(qc, ec, alphac, q, e, alpha):
    fig, ax = plt.subplots(3, 1, figsize=(12, 12))  # Create a figure with 3 subplots

    # Calculate truncation radii for each variable
    Rt_q1 = [cs_trunc_ni(mu_i, ec, alphac, 1) for mu_i in mu]  # Circumprimary for varying mu
    Rt_e1 = [cs_trunc_ni(muc, e_i, alphac, 1) for e_i in e]  # Circumprimary for varying e
    Rt_alph1 = [cs_trunc_ni(muc, ec, alpha_i, 1) for alpha_i in alpha]  # Circumprimary for varying alpha
    Rt_q2 = [cs_trunc_ni(mu_i, ec, alphac, 2) for mu_i in mu]  # Circumsecondary for varying mu
    Rt_e2 = [cs_trunc_ni(muc, e_i, alphac, 2) for e_i in e]  # Circumsecondary for varying e
    Rt_alph2 = [cs_trunc_ni(muc, ec, alpha_i, 2) for alpha_i in alpha]  # Circumsecondary for varying alpha

    # Set axis labels
    ax[0].set_xlabel(r"$q=M_2/M_1$", fontsize=18)
    ax[1].set_xlabel(r"$e$", fontsize=18)
    ax[2].set_xlabel(r"$\alpha$", fontsize=18)
    fig.supylabel(r"Normalised Truncation Radius $R_t/a_{bin}$", fontsize=20)

    # Plot the curves for different values of variables
    ax[0].plot(q, Rt_q1, color='blue', lw=3, label='Circumprimary')
    ax[0].plot(q, Rt_q2, color='red', lw=3, label='Circumsecondary')
    ax[1].plot(e, Rt_e1, color='blue', lw=3)
    ax[1].plot(e, Rt_e2, color='red', lw=3)
    ax[2].set_xscale('log')
    ax[2].plot(alpha, Rt_alph1, color='blue', lw=3, label='Circumprimary')
    ax[2].plot(alpha, Rt_alph2, color='red', lw=3, label='Circumsecondary')

    # Minimize the function to find the minimum of the truncation radius as a function of alpha
    def Rt_alpha_function(alpha_val, muc, ec, mode):
        return cs_trunc_ni(muc, ec, alpha_val, mode)  # The function to minimize
    
    # Minimize for both circumprimary and circumsecondary
    result_1 = minimize(Rt_alpha_function, x0=1e-3, args=(muc, ec, 1), bounds=[(min(alpha), max(alpha))], method='L-BFGS-B')
    result_2 = minimize(Rt_alpha_function, x0=1e-3, args=(muc, ec, 2), bounds=[(min(alpha), max(alpha))], method='L-BFGS-B')

    # Extract the minima points
    alpha_crit_1 = result_1.x[0]
    alpha_crit_2 = result_2.x[0]
    min_Rt_alph1 = cs_trunc_ni(muc, ec, alpha_crit_1, 1)
    min_Rt_alph2 = cs_trunc_ni(muc, ec, alpha_crit_2, 2)

    # Mark the minima on the Rt/a as a function of alpha plot
    ax[2].plot(alpha_crit_1, min_Rt_alph1, 'o', color='blue', label='Min', zorder=5)
    ax[2].plot(alpha_crit_2, min_Rt_alph2, 'o', color='red', label='Min', zorder=5)

    # Display values of both minima on the Rt/a as a function of alpha plot
    #ax[2].text(alpha_crit_1, min_Rt_alph1+0.05, f"({alpha_crit_1:.2e}, {min_Rt_alph1:.2f})", fontsize=10, color='blue', ha='left', va='bottom')
    #ax[2].text(alpha_crit_2, min_Rt_alph2+0.05, f"({alpha_crit_2:.2e}, {min_Rt_alph2:.2f})", fontsize=10, color='red', ha='left', va='bottom')
    # Customize tick parameters for all subplots
    for i in range(3):
        ax[i].tick_params(axis='x', length=7, width=1.5, labelsize=15)
        ax[i].tick_params(axis='y', length=7, width=1.5, labelsize=15)

    # Adjust layout and save the plot
    plt.subplots_adjust(hspace=0.45)
    plt.savefig("Rt_function_of_qealpha.pdf", format="pdf")
    plt.tight_layout()
    plt.show()


# Function to create couloured plots to consider to variables set at 3 different values of a third parameter
def multivariable_plots():
    # To get one plot, since more would be too many, choice is used to choose between the 3 plots
    choice = int(input("Please choose either 1, 2, or 3 to plot R(q, e), R(q, a_bin), or R(alpha, a_bin) respectively, R(q, e) is the default: "))
    # Custom handler for legend markers
    class CustomHandler(HandlerPathCollection):
        def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
            return [Line2D([0], [0], linestyle="", marker=orig_handle.get_paths()[0],
                            markerfacecolor="white", markeredgecolor="black", markersize=fontsize / 2)]
                
    fig, ax = plt.subplots(figsize=(12,8))
    # Set up the appropriate normalization and color mapping based on user input
    if choice == 3 or choice == 2:
        colours = colours_abin
        norm = norm_abin
        label = r'Binary separation [$au$]'
    else:
        colours = colours_e
        norm = norm_e
        label = 'Eccentricity e'
    
    if choice == 2:
        Rt_0 = [cst_abin(mu, ac, 0, alphac, 2)]  # Truncation radius for varying mass ratio at e = 0
        Rt_05 = [cst_abin(mu, ac, 0.5, alphac, 2)] # Truncation radius for varying mass ratio at e=0.5
        Rt_09 = [cst_abin(mu, ac, 0.9, alphac, 2)] # Truncation radius for varying mass ratio at e = 0.9
        ax.set_xlabel(r"Mass ratio $q=M_2/M_1$", fontsize=25)
        ax.set_ylabel(r"$log_{10}$ Truncation radius $R_t$ [$au$]", fontsize=25)
        ax.set_yscale('log')
        ax.scatter(q, Rt_0, marker="o", c=colours, edgecolor='black', label="e=0")
        ax.scatter(q, Rt_05, marker="^", c=colours, edgecolor='black', label="e=0.5")
        ax.scatter(q, Rt_09, marker="s", c=colours, edgecolor='black', label="e=0.9")
        plt.savefig("Rt_vs_q_different_e.pdf", format="pdf")

    elif choice == 3:
        Rt_0 = [cs_trunc_mu(0.5, ac, 0, alpha, 2)] # varying viscosity at e = 0
        Rt_05 = [cs_trunc_mu(0.5, ac, 0.5, alpha, 2)] # varying viscosity at e = 0.5
        Rt_09 = [cs_trunc_mu(0.5, ac, 0.9, alpha, 2)] # varying viscosity at e = 0.9
        ax.set_xlabel(r"Viscosity $\alpha$", fontsize=25)
        ax.set_ylabel(r"$log_{10}$ of Truncation radius $R_t$ [$au$]", fontsize=25)
        ax.set_xscale('log') 
        ax.scatter(alpha, Rt_0, marker="o", c=colours, edgecolor='black', label="e=0")
        ax.scatter(alpha, Rt_05, marker="^", c=colours, edgecolor='black', label="e=0.5")
        ax.scatter(alpha, Rt_09, marker="s", c=colours, edgecolor='black', label="e=0.9")
        plt.savefig("Rt_vs_alpha_different_e.pdf", format="pdf")

    else:    
        Rt_4 = [cs_trunc_ni(mu, e, 1e-4, 2)] # varying mass ratio and eccentricity at alpha = 1e-4
        Rt_5_4 = [cs_trunc_ni(mu, e, 5e-4, 2)] # varying mass ratio and eccentricity at alpha = 5e-4
        Rt_3 = [cs_trunc_ni(mu, e, 1e-3, 2)] # varying mass ratio and eccentricity at alpha = 1e-3
        ax.set_xlabel(r"Mass ratio $q=M_2/M_1$", fontsize=25)
        ax.set_ylabel(r"Truncation radius $R_t/a_{bin}$", fontsize=25)
        ax.scatter(q, Rt_4, marker="o", c=colours, edgecolor='black', label=r"$\alpha$=$10^{-4}$")
        ax.scatter(q, Rt_5_4, marker="^", c=colours, edgecolor='black', label=r"$\alpha$=$5 \times 10^{-4}$")
        ax.scatter(q, Rt_3, marker="s", c=colours, edgecolor='black', label=r"$\alpha$=$10^{-3}$")
        plt.savefig("Rt_vs_q_different_alpha.pdf", format="pdf")
    # Customize tick parameters for all subplots
    ax.tick_params(axis='x', length=10, width=2, labelsize=18)
    ax.tick_params(axis='y', length=10, width=2, labelsize=18)
    # add colour bar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([]) # Set empty array for colour mapping
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label(label=label, fontsize=28)
    cbar.ax.yaxis.set_tick_params(labelsize=18)  # Increase tick size
    plt.legend(fontsize=22, loc="best", markerscale=1.5, frameon=True, fancybox=True, edgecolor="black",
           handler_map={ax.collections[0]: CustomHandler(),
                        ax.collections[1]: CustomHandler(),
                        ax.collections[2]: CustomHandler()})
    plt.show()

plot_for_variables(qc, ec, alphac, q, e, alpha)
#multivariable_plots()