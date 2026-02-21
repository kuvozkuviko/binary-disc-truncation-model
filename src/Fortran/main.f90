program truncation_radius_calculator
    use binary_module
    implicit none
    ! Input variables
    double precision :: Mstar, Mstar2, a_star2, e_star2, alpha_disk, au
    ! Output variable
    double precision :: R_trunc

    ! Input from the user
    print *, "Please choose a value for Mstar in solar units: "
    read *, Mstar
    print *, "Please choose a value for Mstar2 in solar units: "
    read *, Mstar2
    print *, "Please choose a value for the binary separation in astronomical units: "
    read *, a_star2
    print *, "Please choose a value for the binary eccentricity: "
    read *, e_star2
    print *, "Please choose a value for the viscosity: "
    read *, alpha_disk

    ! Ask for optional au value
    print *, "Please choose which portion of the disk you want to use for the H/r calculation, " // &
             "0 for the full disk, < 10 for small disk, > 10 for full disk, NOT 10 plz:) : "
    read *, au
        
    ! Call the compute_stype_truncation function
    R_trunc = COMPUTE_STYPE_TRUNCATION(Mstar, Mstar2, a_star2, e_star2, alpha_disk, au)

    ! Output the truncation radius
    print *, "The truncation radius is: ", R_trunc

end program truncation_radius_calculator

!gfortran -c disk_parameters.f90 Rt_compute.f90  # Compile the modules
!gfortran -o truncation_radius main.f90 disk_parameters.o Rt_compute.o  # Compile and link the main program with the module
!./truncation_radius  # Run the executable