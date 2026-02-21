import numpy as np
import Reynolds_4 as rey

# Function to compute the truncation radius of a circumprimary or circumsecondary disk in an S-type binary star system using equation C.3 from
# Manara et al. 2019
def compute_stype_truncation(Mstar, Mstar2, a_star2, e_star2, alpha_disk, au=15):
   star = int(input("Please choose a star to measure: "))
   if star != 1 and star !=2:
      print("Please choose either the circumprimary (1) or the circumsecondary (2)")

   #Masses of stars should in Msol
   q1 = Mstar / Mstar2
   q2 = Mstar2 / Mstar
   mu = Mstar2 / (Mstar+Mstar2) # reduced mass
   h = 0.88 # Constant term from truncation equation
   k = 0.01 # Exponent term for mu

   Rout_disk = 1000.0 # Outer disk boundary in astronomical units (au)

   # Default value of truncation radius, in case no valid calculation is possible
   truncation_radius = Rout_disk
   # If the mass of the secondary star is negligible, treat the system as a single star, no truncation
   if Mstar2 <= 1.e-3:
      print(f"Since Mstar2 is very small, this is not a binary problem and the truncation radius is ~ {truncation_radius} au")
      return truncation_radius
    
   # Use the Reynolds module to find the aspect ratio (H/r) for the disk at different alphas (1e-4, 5e-4, 1e-3, 5e-3)
   Hr_coeffs, Hr4, Hr54, Hr3, Hr53 = rey.fit_Hr(au)
   if au is not None and au > 10: # If the distance is greater than 10 au, H/r converges for all alpha so the choice of alpha doesn't matter
      Hr = Hr3
   else:
      Hr = np.polyval(Hr_coeffs, alpha_disk)   

   R = pow(Hr, -2) * 1/(alpha_disk)  # Reynolds number calculation

   #Roche Lobe radii for primary and secondary disks
   R_egg1 = (a_star2 * 0.49 * pow(q1, 2/3)) / (0.6 * pow(q1, 2/3) + np.log(1 + pow(q1, 1/3)))
   R_egg2 = (a_star2 * 0.49 * pow(q2, 2/3)) / (0.6 * pow(q2, 2/3) + np.log(1 + pow(q2, 1/3)))

   #Circumprimary disk parameters
   #Equation set for mu=0.1: 
   b_p1 = 9.764309764309791e-13*R**2 + -1.1074074074074087e-06*R**1 + -0.6490235690235693*R**0 
   c_p1 = 1.6611e-12*R**2 + -1.9605e-06*R**1 + 8.5944e-01*R**0
   #Equation set for mu=0.2: 
   b_p2 = 6.509539842873163e-13*R**2 + -7.382716049382692e-07*R**1 + -0.7126823793490461*R**0 
   c_p2 = 1.6611e-12*R**2 + -1.9605e-06*R**1 + 8.9944e-01*R**0
   #Equation set for mu=0.3: 
   b_p3 = 4.3771043771043816e-13*R**2 + -4.925925925925918e-07*R**1 + -0.7551178451178455*R**0 
   c_p3 = 1.7733e-12*R**2 + -2.0840e-06*R**1 + 9.4066e-01*R**0
   #Equation set for mu=0.4: 
   b_p4 = 4.3771043771043937e-13*R**2 + -4.925925925925932e-07*R**1 + -0.7651178451178456*R**0 
   c_p4 = 1.7733e-12*R**2 + -2.0840e-06*R**1 + 9.7066e-01*R**0
   #Equation set for mu=0.5: 
   b_p5 = 3.2547699214366364e-13*R**2 + -3.691358024691398e-07*R**1 + -0.7763411896745228*R**0 
   c_p5 = 1.6611e-12*R**2 + -1.9605e-06*R**1 + 9.5944e-01*R**0

   #Cicumsecondary disk parameters
   #Equation set for mu=0.1: 
   b_s1 = -2.244668911335608e-14*R**2 + 2.4691358024707388e-09*R**1 + -0.8100224466891136*R**0 
   c_s1 = 1.8967e-12*R**2 + -2.2086e-06*R**1 + 1.0019e+00*R**0
   #Equation set for mu=0.2: 
   b_s2 = 1.0101010101009552e-13*R**2 + -1.2222222222221502e-07*R**1 + -0.808787878787879*R**0 
   c_s2 = 1.7733e-12*R**2 + -2.0840e-06*R**1 + 1.0107e+00*R**0
   #Equation set for mu=0.3: 
   b_s3 = 3.254769921436567e-13*R**2 + -3.691358024691327e-07*R**1 + -0.7863411896745232*R**0 
   c_s3 = 1.6611e-12*R**2 + -1.9605e-06*R**1 + 9.8944e-01*R**0
   #Equation set for mu=0.4: 
   b_s4 = 2.132435465768843e-13*R**2 + -2.456790123456824e-07*R**1 + -0.7975645342312008*R**0 
   c_s4 = 1.8855e-12*R**2 + -2.2074e-06*R**1 + 1.0019e+00*R**0
   #Equation set for mu=0.5: 
   b_s5 = 2.1324354657688054e-13*R**2 + -2.456790123456777e-07*R**1 + -0.7875645342312014*R**0 
   c_s5 = 1.7733e-12*R**2 + -2.0840e-06*R**1 + 9.7066e-01*R**0

   # Lists containing the different b and c values for primary and secondary disks for each mu
   b_prim = [b_p1, b_p2, b_p3, b_p4, b_p5]
   c_prim = [c_p1, c_p2, c_p3, c_p4, c_p5]
   b_sec = [b_s1, b_s2, b_s3, b_s4, b_s5]
   c_sec = [c_s1, c_s2, c_s3, c_s4, c_s5]

   #Calculate b and c based on the value of mu, see Polyfitprimary/Polyfitsecondary for more detail
   if mu<0:
      print("Serendipity!") #In case of an unreasonable mu
   if mu<0.15:
      b1 = b_prim[0]
      b2 = b_sec[0]
      c1 = c_prim[0]
      c2 = c_sec[0]
   elif mu>=0.15 and mu<2.5:
      b1 = b_prim[1]
      b2 = b_sec[1]
      c1 = c_prim[1]
      c2 = c_sec[1]
   elif mu>=2.5 and mu<3.5:
      b1 = b_prim[2]
      b2 = b_sec[2]
      c1 = c_prim[2]
      c2 = c_sec[2]
   elif mu>=3.5 and mu<4.5:
      b1 = b_prim[3]
      b2 = b_sec[3]
      c1 = c_prim[3]
      c2 = c_sec[3]
   else:
      b1 = b_prim[4]
      b2 = b_sec[4]
      c1 = c_prim[4]
      c2 = c_sec[4]

   # Choice of disk to compute the truncation radius for
   if star==1:
      truncation_radius = R_egg1 * (b1 * e_star2**c1 + h * mu**k)
   elif star==2:
      truncation_radius = R_egg2 * (b2 * e_star2**c2 + h * mu**k)
   else:
      print('''For the Circumprary disk please input star=1 while for the Circumsecondary disk please input star=2,
               in both cases as integers so no 1. or 1.0, equivilantly no 2. or 2.0''')

   return truncation_radius

if __name__ == "__main__":
   Mstar = float(input("Please choose a value for Mstar in solar units: "))
   Mstar2 = float(input("Please choose a value for Mstar2 in solar units: "))
   a_star2 = float(input("Please choose a value for the binary separation in astronomical units: "))
   e_star2 = float(input("Please choose a value for the binary eccentricity: "))
   alpha_disk = float(input("Please choose a value for the viscosity: "))
   au = 0
   au_choice = float(input("Please choose the limit measurement value in astronomical units (enter 0 for all au): "))
   if au_choice == 0:
      au is None
   else:
      au = au_choice

   R_trunc = compute_stype_truncation(Mstar, Mstar2, a_star2, e_star2, alpha_disk, au)
   print(R_trunc)

#Mstar = 1
#Mstar = 1/2
#a_star2 = 100
#e_star2 = 0
#R = 38.56

#e_star = 0.5
#R = 17.77