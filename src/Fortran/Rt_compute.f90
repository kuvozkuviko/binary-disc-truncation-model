module binary_module
contains
    subroutine fit_Hr(au, alpha_disk, result)
    ! Find coefficients of the equation of the Hr fit
    ! Evaluate Hr(alpha_disk) and use it

    ! The equation for Hr found in Reynolds.py from the fit_Hr() function is given by (with a = alpha_disk):
    ! all au: Hr(a) = 4.516471e+06*a^2 - 4.037350e+04*a + 1.988833e+02
    ! au < 10: Hr(a) = 2.883060e+08*a^2 - 5.298075e+05*a + 3.836260e+02
    ! au > 10: Hr(a) = 0.09826384282379806
        implicit none
        double precision, intent(in) :: alpha_disk, au
        double precision, intent(out) :: result

        ! Fit of Hr depending on au
        if (au>10) then
            result = 0.09826384282379806 ! At au greater than 10 H/r converges for all alpha_disk so the 
            !Choice of alpha_disk won't really affect the calculation
        else if (0 < au .and. au < 10) then
            result = 2.883060e+08*(alpha_disk**2) - 5.298075e+05*(alpha_disk) + 3.836260e+02
        else if (au==0) then
            result = 4.516471e+06*(alpha_disk**2) - 4.037350e+04*(alpha_disk) + 1.988833e+02
        else
            result = 0.0
            print *, "Please choose an au that is not 10"
        end if
    end subroutine fit_Hr

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    function COMPUTE_STYPE_TRUNCATION(Mstar, Mstar2, a_star2, e_star2, alpha_disk, au) result(truncation_radius)
    ! Function to compute the truncation radius of a circumprimary or circumsecondary disk in an S-type binary star system using 
    ! equation C.3 from Manara et al. 2019
        use disk_parameters
        implicit none
        double precision, intent(in) :: Mstar, Mstar2, a_star2, e_star2, alpha_disk
        double precision, intent(in), optional :: au
        double precision :: truncation_radius, q1, q2, mu, h, k, Rout_disk
        double precision :: R, R_egg1, R_egg2, Hr
        double precision :: b1, b2, c1, c2
        integer :: star

        ! Constants, Masses of stars should be in Msol
        q1 = Mstar / Mstar2
        q2 = Mstar2 / Mstar
        mu = Mstar2 / (Mstar + Mstar2) ! Reduced mass
        h = 0.88 ! Constant term from truncation equaiton
        k = 0.01 ! Exponent term for mu
        Rout_disk = 1000.0 ! Outer disk boundary in astronomical units (au)

        ! Choose star
        print *, "Please choose a star to measure (1 for circumprimary, 2 for circumsecondary): "
        read *, star
        do while (star /= 1 .and. star /= 2)
            print *, "Please choose either the circumprimary (1) or the circumsecondary (2)"
            read *, star
        end do

        ! If the mass of the secondary star is negligible
        if (Mstar2 <= 1.e-3) then
            print *, "Since Mstar2 is very small, this is not a binary problem and the truncation radius is ~ ", Rout_disk, " au"
            truncation_radius = Rout_disk
            return
        end if

        ! Use the fit_Hr subroutine  to find the aspect ratio (H/r) for the disk at the specified alpha_disk and au
        call fit_Hr(au, alpha_disk, Hr)
        R = Hr**(-2) *(1/alpha_disk)  ! Reynolds number calculation

        ! Roche Lobe radii for primary and secondary disks
        R_egg1 = (a_star2 * 0.49 * (q1**(2.0/3.0))) / (0.6 * (q1**(2.0/3.0)) + log(1.0 + (q1**(1.0/3.0))))
        R_egg2 = (a_star2 * 0.49 * (q2**(2.0/3.0))) / (0.6 * (q2**(2.0/3.0)) + log(1.0 + (q2**(1.0/3.0))))
     
        call initialize_disk_parameters(R)

        !Calculate b and c based on the value of mu, see Polyfitprimary/Polyfitsecondary or disk_parameters for more detail
        if (mu<=0) then
           print*, "Serendipity!" !In case of an unreasonable mu
        end if
        if (0<mu .and. mu<0.15) then
           b1 = b_prim(1)
           b2 = b_sec(1)
           c1 = c_prim(1)
           c2 = c_sec(1)
        else if (0.15<=mu .and. mu<2.5) then
           b1 = b_prim(2)
           b2 = b_sec(2)
           c1 = c_prim(2)
           c2 = c_sec(2)
        else if (2.5<=mu .and. mu<3.5) then
           b1 = b_prim(3)
           b2 = b_sec(3)
           c1 = c_prim(3)
           c2 = c_sec(3)
        else if (3.5<=mu .and. mu<4.5) then
           b1 = b_prim(4)
           b2 = b_sec(4)
           c1 = c_prim(4)
           c2 = c_sec(4)
        else
           b1 = b_prim(5)
           b2 = b_sec(5)
           c1 = c_prim(5)
           c2 = c_sec(5)
        end if

        ! Calculate the truncation radius based on the chosen star
        if (star == 1) then
            truncation_radius = R_egg1 * (b1 * e_star2**c1 + h * mu**k)
        else if (star == 2) then
            truncation_radius = R_egg2 * (b2 * e_star2**c2 + h * mu**k)
        else
            write(*, *) 'For the Circumprary disk please input star=1 while for the Circumsecondary disk please input star=2,' // &
                        'in both cases as integers so no 1. or 1.0, equivilantly no 2. or 2.0'
        end if

    end function COMPUTE_STYPE_TRUNCATION
end module binary_module