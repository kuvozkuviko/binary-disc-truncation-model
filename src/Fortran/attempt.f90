! This program only exists to test if binary_module works

program test_fit_Hr
    use binary_module
    implicit none
    ! Declare variables for disc viscosity parameter, result, and binary separation
    double precision :: alpha_disk
    double precision :: result
    double precision :: au

    print *, "Testing fit_Hr subroutine"

    ! Test 1: Call fit_Hr with alpha_disk = 0.001 and au = 0 (average H/r over all discs)
    alpha_disk = 0.001
    au = 0
    call fit_Hr(au=au, alpha_disk=alpha_disk, result=result)
    print *, "Result for alpha_disk = 0.001 (H/r average over all discs): ", result

    ! Test 2: Call fit_Hr with alpha_disk = 0.001 and au = 5.0
    alpha_disk = 0.001
    au = 5.0
    call fit_Hr(au=au, alpha_disk=alpha_disk, result=result)
    print *, "Result for alpha_disk = 0.001, au = 5.0: ", result

    ! Test 3: Call fit_Hr with alpha_disk = 0.001 and au = 10.0 (result not printed because it is an invalid au)
    alpha_disk = 0.001
    au = 10.0
    call fit_Hr(au=au, alpha_disk=alpha_disk, result=result)

    ! Test 4: Call fit_Hr with alpha_disk = 0.001 and au = 15.0
    alpha_disk = 0.001
    au = 15.0
    call fit_Hr(au=au, alpha_disk=alpha_disk, result=result)
    print *, "Result for alpha_disk = 0.001, au = 15.0: ", result

end program test_fit_Hr