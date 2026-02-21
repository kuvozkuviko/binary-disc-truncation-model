import numpy as np


# Function to compute the truncation radius of a circumprimary or circumsecondary disk in an S-type binary star system using equation C.3 from
# Manara et al. 2019. This function is modified so that we can directly give inputs for the mass ratios q1 and q2 instead of the masses. This
# is so that in the Single_var_plots.py we can plot Rt/a as a function of q for 0 eccentricity. In this case the truncation radius is
# dimensionless. This is done by not multiplying the Roche Lobe radii by a_bin.
def compute_stype_truncation_qdep(q1, q2, e_star2, alpha_disk, star, au=15):
   #Masses of stars should in Msol
   h = 0.88 # Constant term from truncation equation
   k = 0.01 # Exponent term for mu
   mu = 1/(1+q1)

   Rout_disk = 1000.0 # Outer disk boundary in astronomical units (au)

   # Default value of truncation radius, in case no valid calculation is possible
   truncation_radius = Rout_disk
   # If the mass of the secondary star is negligible, treat the system as a single star, no truncation

   #Roche Lobe radii for primary and secondary disks
   R_egg1 = (0.49 * pow(q1, 2/3)) / (0.6 * pow(q1, 2/3) + np.log(1 + pow(q1, 1/3)))
   R_egg2 = (0.49 * pow(q2, 2/3)) / (0.6 * pow(q2, 2/3) + np.log(1 + pow(q2, 1/3)))
   
   # Choice of disk to compute the truncation radius for
   if star==1:
      truncation_radius = R_egg1 * (h * mu**k)
   elif star==2:
      truncation_radius = R_egg2 * (h * mu**k)
   else:
      truncation_radius = 0

   return truncation_radius