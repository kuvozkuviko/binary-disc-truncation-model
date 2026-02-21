import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde as kde
import pandas as pd
from scipy.signal import find_peaks as fp

def plot_Hr(au=None, df_a=None, df_b=None, df_c=None, df_d=None):
    if df_a is None:
        df_a = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/1e-3/mean_aspect_ratio_1e-3.csv", index_col=0, header=0)
    if df_b is None:
        df_b = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/1e-4/mean_aspect_ratio_1e-4.csv", index_col=0, header=0)
    if df_c is None:
        df_c = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/5e-3/mean_aspect_ratio_5e-3.csv", index_col=0, header=0)
    if df_d is None:
        df_d = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/5e-4/mean_aspect_ratio_5e-4.csv", index_col=0, header=0)

    density = False

    if au is not None and au < 10:  # Plot for au<10
        plt.figure(figsize=(12,8))
        Hr3 = df_a.iloc[:, 2]  
        Hr4 = df_b.iloc[:, 2]
        Hr53 = df_c.iloc[:, 2]
        Hr54 = df_d.iloc[:, 2]

        title = r"Density of $\frac{H}{r}$ for au<10"

        if len(Hr3) == len(Hr4):
            bins = int(np.sqrt(len(Hr3)))
        else:
            bins = 32

        xvals = np.linspace(min(Hr3.min(), Hr4.min(), Hr53.min(), Hr54.min()), max(Hr3.max(), Hr4.max(), Hr53.max(), Hr54.max()), 1000, endpoint=True)
        kde3 = kde(Hr3)(xvals)
        kde4 = kde(Hr4)(xvals)
        kde53 = kde(Hr53)(xvals)
        kde54 = kde(Hr54)(xvals)
        #Mean value of H/r
        guess3 = Hr3.mean()
        guess4 = Hr4.mean()
        guess53 = Hr53.mean()
        guess54 = Hr54.mean()

        #Find peak indeces
        peaks3, _ = fp(kde3, height=100)
        peaks4, _ = fp(kde4, height=100)
        peaks53, _ = fp(kde53, height=50)
        peaks54, _ = fp(kde54, height=100)


        #x values and KDE values for the detected peaks
        tmu3 = xvals[peaks3]
        tmu4 = xvals[peaks4]
        tmu53 = xvals[peaks53]
        tmu54 = xvals[peaks54]
        kde3_p = kde3[peaks3]
        kde4_p = kde4[peaks4]
        kde53_p = kde53[peaks53]
        kde54_p = kde54[peaks54]


        plt.hist(Hr3, bins=bins, density=True, alpha=0.55, color='b', edgecolor='b', label=r'$\frac{H}{r}$: $\alpha=10^{-3}$')
        plt.hist(Hr4, bins=bins, density=True, alpha=0.55, color='g', edgecolor='g', label=r'$\frac{H}{r}$: $\alpha=10^{-4}$')
        plt.hist(Hr53, bins=bins, density=True, alpha=0.55, color='orange', edgecolor='orange', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-3}$')
        plt.hist(Hr54, bins=bins, density=True, alpha=0.55, color='pink', edgecolor='pink', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-4}$')

        plt.plot(xvals, kde3, color='b', lw=2)
        plt.plot(xvals, kde4, color='g', lw=2)
        plt.plot(xvals, kde53, color='orange', lw=2)
        plt.plot(xvals, kde54, color='pink', lw=2)

        #Plotting the means
        plt.axvline(guess3, color='b', linestyle='--')  # Mean line for Hr3
        plt.axvline(guess4, color='g', linestyle='--')
        plt.axvline(guess53, color='orange', linestyle='--')
        plt.axvline(guess54, color='pink', linestyle='--')
        plt.scatter(tmu3, kde3_p, marker="x", c='red', label=f'({tmu3[0]:.3e}, {kde3_p[0]:.3e})', s=200)
        plt.scatter(tmu4, kde4_p, marker="x", c='purple', label=f'({tmu4[0]:.3e}, {kde4_p[0]:.3e})', s=200)
        plt.scatter(tmu53, kde53_p, marker="x", c='brown', label=f'({tmu53[0]:.3e}, {kde53_p[0]:.3e})', s=200)
        plt.scatter(tmu54, kde54_p, marker="x", c='navy', label=f'({tmu54[0]:.3e}, {kde54_p[0]:.3e})', s=200)
        # Calculate R and show it on the graph

        plt.title(title, fontsize=14)
        plt.xlabel(r"$\frac{H}{r}$", fontsize=14)
        plt.ylabel("Density", fontsize=14)
        plt.legend(fontsize=14)
        plt.show()

        return tmu4[0], tmu54[0], tmu3[0], tmu53[0]

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    elif au is not None and au>10:  # Plot for au>10
        fig, ax = plt.subplots(1, 2, figsize=(12, 8))
        Hr3 = df_a.iloc[:, 1]
        Hr4 = df_b.iloc[:, 1]
        Hr53 = df_c.iloc[:, 1]
        Hr54 = df_d.iloc[:, 1]

        title = r"Density of $\frac{H}{r}$ au>10"

        if len(Hr3) == len(Hr4):
            bin = int(np.sqrt(len(Hr3)))
        else:
            bin = 32

        min_val = min(Hr3.min(), Hr4.min(), Hr53.min(), Hr54.min())
        max_val = max(Hr3.max(), Hr4.max(), Hr53.min(), Hr54.max())
        bins = np.linspace(min_val, max_val, bin)

        xvals = np.linspace(min_val, max_val, 1000, endpoint=True)
        kde3 = kde(Hr3)(xvals)
        kde4 = kde(Hr4)(xvals)
        kde53 = kde(Hr53)(xvals)
        kde54 = kde(Hr54)(xvals)

        guess3 = Hr3.mean()
        guess4 = Hr4.mean()
        guess53 = Hr53.mean()
        guess54 = Hr54.mean()

        #Find peak indeces
        peaks3, _ = fp(kde3, height=100)
        peaks4, _ = fp(kde4, height=100)
        peaks53, _ = fp(kde53, height=50)
        peaks54, _ = fp(kde54, height=100)

        #x values and KDE values for the detected peaks
        tmu3 = xvals[peaks3]
        tmu4 = xvals[peaks4]
        tmu53 = xvals[peaks53]
        tmu54 = xvals[peaks54]
        kde3_p = kde3[peaks3]
        kde4_p = kde4[peaks4]
        kde53_p = kde53[peaks53]
        kde54_p = kde54[peaks54]

        if len(kde4_p) > 0:
            R3, R4 = pow(tmu3[0], -2) * 1/(1e-3), pow(tmu4[0], -2) * 1/(1e-4) # R = 1/kde4_p_a (R_value for the first peak)
            R53, R54 = pow(tmu53[0], -2) * 1/(5e-3), pow(tmu54[0], -2) * 1/(5e-4)
            err = (R3 + R4 + R53 + R54) / 4
            error = np.sqrt(((err-R3)**2 + (err - R4)**2 + (err-R3)**2 + (err-R4)**2)/4)            
    
        for i in range(0, 2):
            count, bins1, _ = ax[i].hist(Hr3, bins=bins, density=density, alpha=0.55, color='b', edgecolor='b', label=r'$\frac{H}{r}$: $\alpha=10^{-3}$')
            count, bins2, _ = ax[i].hist(Hr4, bins=bins, density=density, alpha=0.55, color='g', edgecolor='g', label=r'$\frac{H}{r}$: $\alpha=10^{-4}$')
            count, bins3, _ = ax[i].hist(Hr53, bins=bins, density=density, alpha=0.55, color='orange', edgecolor='orange', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-3}$')
            count, bins4, _ = ax[i].hist(Hr54, bins=bins, density=density, alpha=0.55, color='pink', edgecolor='pink', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-4}$')
            bin_width1 = bins1[1] - bins1[0]
            bin_width2 = bins2[1] - bins2[0]
            bin_width3 = bins3[1] - bins3[0]
            bin_width4 = bins4[1] - bins4[0]
            ax[i].plot(xvals, kde3*1000*bin_width1, color='b', label=r'KDE $\frac{H}{r}$: $\alpha=10^{-3}$', lw=2)
            ax[i].plot(xvals, kde4*1000*bin_width2, color='g', label=r'KDE $\frac{H}{r}$: $\alpha=10^{-4}$', lw=2)
            ax[i].plot(xvals, kde53*1000*bin_width3, color='orange', label=r'KDE $\frac{H}{r}$: $\alpha=5 \cdot 10^{-3}$', lw=2)
            ax[i].plot(xvals, kde54*1000*bin_width4, color='pink', label=r'KDE $\frac{H}{r}$: $\alpha=5 \cdot 10^{-4}$', lw=2)
            ax[i].set_xlabel(r'$\frac{H}{r}$', fontsize=14)
            ax[i].set_ylabel('Density', fontsize=14)
            ax[i].axvline(guess3, color='b', linestyle='--', label=f'Guess: {guess3:.3e}')  # Mean line for Hr3
            ax[i].axvline(guess4, color='g', linestyle='--', label=f'Guess: {guess4:.3e}')
            ax[i].axvline(guess53, color='orange', linestyle='--', label=f'Guess: {guess53:.3e}')
            ax[i].axvline(guess54, color='pink', linestyle='--', label=f'Guess: {guess54:.3e}')
            ax[i].scatter(tmu3[0], kde3_p[0]*1000*bin_width1, marker="x", c='red', label=f'({tmu3[0]:.3e}, {kde3_p[0]:.3e})', s=200)
            ax[i].scatter(tmu4[0], kde4_p[0]*1000*bin_width2, marker="x", c='purple', label=f'({tmu4[0]:.3e}, {kde4_p[0]:.3e})', s=200)
            ax[i].scatter(tmu53[0], kde53_p[0]*1000*bin_width3, marker="x", c='brown', label=f'({tmu53[0]:.3e}, {kde53_p[0]:.3e})', s=200)
            ax[i].scatter(tmu54[0], kde54_p[0]*1000*bin_width4, marker="x", c='navy', label=f'({tmu54[0]:.3e}, {kde54_p[0]:.3e})', s=200)
            if i == 0:
                ax[i].set_title(title, fontsize=14)
                ax[i].legend(fontsize=14)
            else:
                ax[i].set_title(title + " zoomed in (x < 0.09835)", fontsize=14)                
                ax[i].set_xlim(left=min(xvals), right=0.09835)
        plt.tight_layout()
        plt.show()

        return tmu4[0], tmu54[0], tmu3[0], tmu53[0]

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    elif au==10:
        print("Please choose any number that isn't 10")
        a, b, c, d, e = 0, 0, 0
        return a, b, c, d, e

###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################

    else:  # Plot for all au
        plt.figure(figsize=(14,10))
        Hr3 = df_a.iloc[:, 0]  
        Hr4 = df_b.iloc[:, 0]
        Hr53 = df_c.iloc[:, 0]
        Hr54 = df_d.iloc[:, 0]
        title = r"Density of $\frac{H}{r}$ for all au"

        if len(Hr3) == len(Hr4):
            bins = int(np.sqrt(len(Hr3)))
        else:
            bins = 32

        xvals = np.linspace(min(Hr3.min(), Hr4.min(), Hr53.min(), Hr54.min()), max(Hr3.max(), Hr4.max(), Hr53.max(), Hr54.max()), 1000, endpoint=True)
        kde3 = kde(Hr3)(xvals)
        kde4 = kde(Hr4)(xvals)
        kde53 = kde(Hr53)(xvals)
        kde54 = kde(Hr54)(xvals)
        #Mean value of H/r
        guess3 = Hr3.mean()
        guess4 = Hr4.mean()
        guess53 = Hr53.mean()
        guess54 = Hr54.mean()

        #Find peak indeces
        peaks3, _ = fp(kde3, height=100)
        peaks4, _ = fp(kde4, height=100)
        peaks53, _ = fp(kde53, height=100)
        peaks54, _ = fp(kde54, height=100)

        #x values and KDE values for the detected peaks
        tmu3 = xvals[peaks3]
        tmu4 = xvals[peaks4]
        tmu53 = xvals[peaks53]
        tmu54 = xvals[peaks54]
        kde3_p = kde3[peaks3]
        kde4_p = kde4[peaks4]
        kde53_p = kde53[peaks53]
        kde54_p = kde54[peaks54]

        count, bins1, _ = plt.hist(Hr3, bins=bins, density=density, alpha=0.6, color='b', edgecolor='b', label=r'$\frac{H}{r}$: $\alpha=10^{-3}$')
        count, bins2, _ = plt.hist(Hr4, bins=bins, density=density, alpha=0.6, color='g', edgecolor='g', label=r'$\frac{H}{r}$: $\alpha=10^{-4}$')
        count, bins3, _ = plt.hist(Hr53, bins=bins, density=density, alpha=0.6, color='orange', edgecolor='orange', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-3}$')
        count, bins4, _ = plt.hist(Hr54, bins=bins, density=density, alpha=0.6, color='pink', edgecolor='pink', label=r'$\frac{H}{r}$: $\alpha=5 \cdot 10^{-4}$')
        bin_width1 = bins1[1] - bins1[0]
        bin_width2 = bins2[1] - bins2[0]
        bin_width3 = bins3[1] - bins3[0]
        bin_width4 = bins4[1] - bins4[0]
        plt.plot(xvals, kde3*1000*bin_width1, color='b', label=r'KDE $\frac{H}{r}$: $\alpha=10^{-3}$', lw=2)
        plt.plot(xvals, kde4*1000*bin_width2, color='g', label=r'KDE $\frac{H}{r}$: $\alpha=10^{-4}$', lw=2)
        plt.plot(xvals, kde53*1000*bin_width3, color='orange', label=r'KDE $\frac{H}{r}$: $\alpha=5 \cdot 10^{-3}$', lw=2)
        plt.plot(xvals, kde54*1000*bin_width4, color='pink', label=r'KDE $\frac{H}{r}$: $\alpha=5 \cdot 10^{-4}$', lw=2)
        #Plotting the means
        plt.axvline(guess3, color='b', linestyle='--', label=f'Guess: {guess3:.3e}')  # Mean line for Hr3
        plt.axvline(guess4, color='g', linestyle='--', label=f'Guess: {guess4:.3e}')
        plt.axvline(guess53, color='orange', linestyle='--', label=f'Guess: {guess53:.3e}')
        plt.axvline(guess54, color='pink', linestyle='--', label=f'Guess: {guess54:.3e}')  # Mean line for Hr3
        plt.scatter(tmu3, kde3_p*1000*bin_width1, marker="x", c='red', label=f'({tmu3[0]:.3e}, {kde3_p[0]:.3e})', s=200)
        plt.scatter(tmu4, kde4_p*1000*bin_width2, marker="x", c='purple', label=f'({tmu4[0]:.3e}, {kde4_p[0]:.3e})', s=200)
        plt.scatter(tmu53, kde53_p*1000*bin_width3, marker="x", c='brown', label=f'({tmu53[0]:.3e}, {kde53_p[0]:.3e})', s=200)
        plt.scatter(tmu54, kde54_p*1000*bin_width4, marker="x", c='navy', label=f'({tmu54[0]:.3e}, {kde54_p[0]:.3e})', s=200)
    
        plt.title(title, fontsize=14)
        plt.xlabel(r"$\frac{H}{r}$", fontsize=14)
        plt.ylabel("Density", fontsize=14)
        plt.legend(fontsize=14)
        plt.show()

        return tmu4[0], tmu54[0], tmu3[0], tmu53[0]
 
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def fit_Hr(au=None, deg=2, df_a=None, df_b=None, df_c=None, df_d=None):
    if df_a is None:
        df_a = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/1e-4/mean_aspect_ratio_1e-4.csv", index_col=0, header=0)
    if df_b is None:
        df_b = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/5e-4/mean_aspect_ratio_5e-4.csv", index_col=0, header=0)
    if df_c is None:
        df_c = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/1e-3/mean_aspect_ratio_1e-3.csv", index_col=0, header=0)
    if df_d is None:
        df_d = pd.read_csv("/home/andres/Documents/Astroworld/disk_pop/5e-3/mean_aspect_ratio_5e-3.csv", index_col=0, header=0)
   
    if au is not None and 0< au < 10:
        Hra = df_a.iloc[:, 2] 
        Hrb = df_b.iloc[:, 2]
        Hrc = df_c.iloc[:, 2]
        Hrd = df_d.iloc[:, 2]
    elif au is not None and au > 10:
        Hra = df_a.iloc[:, 1] 
        Hrb = df_b.iloc[:, 1]
        Hrc = df_c.iloc[:, 1]
        Hrd = df_d.iloc[:, 1]
    elif au is not None and au == 10:
        Hra = 0 
        Hrb = 0
        Hrc = 0
        Hrd = 0
        print("Please choose an au that is not 10")
    else:
        Hra = df_a.iloc[:, 0] 
        Hrb = df_b.iloc[:, 0]
        Hrc = df_c.iloc[:, 0]
        Hrd = df_d.iloc[:, 0]

    xvals = np.linspace(min(Hra.min(), Hrb.min(), Hrc.min(), Hrd.min()), max(Hra.max(), Hrb.max(), Hrc.max(), Hrd.max()), 1000, endpoint=True)
    
    kdea = kde(Hra)(xvals)
    kdeb = kde(Hrb)(xvals)
    kdec = kde(Hrc)(xvals)
    kded = kde(Hrd)(xvals)
    
    peaksa, _ = fp(kdea, height=50)
    peaksb, _ = fp(kdeb, height=50)
    peaksc, _ = fp(kdec, height=50)
    peaksd, _ = fp(kded, height=50)

    #x values and KDE values for the detected peaks
    tmua = xvals[peaksa]
    tmub = xvals[peaksb]
    tmuc = xvals[peaksc]
    tmud = xvals[peaksd]
    kdea_p = kdea[peaksa]
    kdeb_p = kdeb[peaksb]
    kdec_p = kdec[peaksc]
    kded_p = kded[peaksd]

    alpha = [1e-4, 5e-4, 1e-3]#, 5e-3]
    kde_fit = [kdea_p[0], kdeb_p[0], kdec_p[0]]#, kded_p[0]]
    
    gauss_pol = np.polyfit(alpha, kde_fit, deg)
    alpha_vals = np.linspace(min(alpha), max(alpha), 1000, endpoint=True)
    gauss_poly_curve = np.polyval(gauss_pol, alpha_vals)
#    equation_Hr = r"Hr(a) = " + " + ".join([rf"{coeff:e}*a^{deg-ix}" for ix, coeff in enumerate(gauss_pol)]).replace("+ -","- ").replace("a^1", "a").replace("*a^0", "")
#    plt.plot(alpha_vals, gauss_poly_curve)
#    plt.scatter(alpha, kde_fit)

#   plt.show()
    #print(equation_Hr)

    # Display results and fit in another text file to use them
#    with open("/home/andres/Documents/Astroworld/text/Hrvalues.txt", "w") as file:
#        file.write(f"{tmua[0]}\n{tmub[0]}\n{tmuc[0]}\n")
#        file.write(equation_Hr)    
    return gauss_pol, tmua[0], tmub[0], tmuc[0], tmud[0]
