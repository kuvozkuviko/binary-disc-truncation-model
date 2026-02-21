import numpy as np
import matplotlib.pyplot as plt

# Interpolating the Circumprimary data from Table C.1 from Manara et. al 2019 to create polynomial fits of b and c as a function of the Reynolds
# number depending on the value of mu

# Values of mu (mass ratio parameter)
mu = [0.1, 0.2, 0.3, 0.4, 0.5]

# Coefficients for parameter b for different values of mu and R
b1 = [-0.66, -0.75, -0.78]
b2 = [-0.72, -0.78, -0.80]
b3 = [-0.76, -0.80, -0.81]
b4 = [-0.77, -0.81, -0.82]
b5 = [-0.78, -0.81, -0.82]

b = [b1, b2, b3, b4, b5]  # List of b for all mu values

# Coefficients for parameter c for different values of mu and R
c1 = [0.84, 0.68, 0.56]
c2 = [0.88, 0.72, 0.60]
c3 = [0.92, 0.75, 0.63]
c4 = [0.95, 0.78, 0.66]
c5 = [0.94, 0.78, 0.66]

c = [c1, c2, c3, c4, c5] # List of c for all mu values

R = [1e4, 1e5, 1e6] # Values of Reynolds number

def fit(b, c, R, log=False, deg=2):
    """
    Function to fit polynomial curves of b and c coefficients as a function of R.
    It returns the polynomial equations for both b(R) and c(R) for each value of mu.
    
    """
    if log == True: # Give the option of using the log
        R = [np.log10(Ri) for Ri in R] # Values of Reynolds number
    b_fit = []  # Store polynomial coefficients for b(R)
    c_fit = []  # Store polynomial coefficients for c(R)
    eqs_b = []  # Store b(R) equations
    eqs_c = []  # Store c(R) equations

    # Fit b values for each set of mu using a polynomial of degree 'deg'
    for bi in b:
        b_pol = np.polyfit(R, bi, deg)
        b_fit.append(b_pol)

    # Fit c values for each set of mu using a polynomial of degree 'deg'
    for ci in c:
        c_pol = np.polyfit(R, ci, deg)
        c_fit.append(c_pol)

    # Generate fine-grained values for R to plot smooth curves
    R_vals = np.linspace(min(R), max(R), 1000, endpoint=True)

    # Create subplots for b(R) and c(R)
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    #plt.suptitle('Circumprimary', fontsize=16)

    for i, b_fitted in enumerate(b_fit):
        # Evaluate the polynomial over R_vals
        b_poly_curve = np.polyval(b_fitted, R_vals)
        ax[0].plot(R_vals, b_poly_curve, label=r'$\mu$' + f'={mu[i]}')
        # Generate a string representation of the equation for b(R)
        equation_b = "b(R) = " + " + ".join([f"{coeff:.3e}*R^{deg-ix}" for ix, coeff in enumerate(b_fitted)]).replace("+ -", "- ").replace("R^1", "R").replace("*R^0", "")
        # Display the equation on the plot
        #ax[0].text(0.45, 0.98 - i*0.1, equation_b, transform=ax[0].transAxes, fontsize=8,
        #           verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white"))
        #eqs_b.append(equation_b)
   
    # Scatter plot the original b values
    for bi in b:
        ax[0].scatter(R, bi)
    if log == True:
        ax[0].set_xlabel(r'log10($\mathcal{R}$)')
        ax[0].set_title(r'b(log10($\mathcal{R}$))')
    else:
        ax[0].set_xlabel(r'$\mathcal{R}$', fontsize=18)
        #ax[0].set_title('b(R)')
    ax[0].set_ylabel('b', fontsize=18)

    # Plot polynomial fits and equations for c(R)
    for i, c_fitted in enumerate(c_fit):
        # Evaluate the polynomial over R_vals
        c_poly_curve = np.polyval(c_fitted, R_vals)
        ax[1].plot(R_vals, c_poly_curve, label=r'$\mu$' + f'={mu[i]}')
        # Generate a string representation of the equation for c(R)
        #equation_c = "c(R) = " + " + ".join([f"{coeff:.3e}*R^{deg-ix}" for ix, coeff in enumerate(c_fitted)]).replace("+ -", "- ").replace("R^1", "R").replace("*R^0", "")
        # Display the equation on the plot
        #ax[1].text(0.45, 0.98 - i*0.1, equation_c, transform=ax[1].transAxes, fontsize=8, verticalalignment='top',
        #            bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white"))
        #eqs_c.append(equation_c)

    # Scatter plot the original c values
    for ci in c:
        ax[1].scatter(R, ci)
    if log == True:
        ax[1].set_xlabel(r'log10($\mathcal{R}$)')
        ax[1].set_title(r'rc(log10($\mathcal{R}$))')

    else:
        ax[1].set_xlabel(r'$\mathcal{R}$', fontsize=18)
        #ax[1].set_title('c(R)')
    ax[1].set_ylabel('c', fontsize=18)

    # Increase tick mark size
    for i in range(2):
        ax[i].tick_params(axis='x', length=8, width=1.5, labelsize=13.5)
        ax[i].tick_params(axis='y', length=8, width=1.5, labelsize=13.5)
        ax[i].legend(fontsize=14, ncol=2)

    
    plt.tight_layout()
    plt.savefig("circumprimary_b_c.pdf", format="pdf")
    plt.show()
    # Return the equations for both b(R) and c(R)
    #return eqs_b, eqs_c

#eqs1, eqs2 = fit(b, c, R)
# Print the resulting equations for each value of mu
#for i, (eq1, eq2) in enumerate(zip(eqs1, eqs2)):
#    print(f"Equation set for mu={i+1}: \n {eq1} \n {eq2}")  

fit(b, c, R)
