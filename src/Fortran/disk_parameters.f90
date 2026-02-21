! disk_parameters.f90
module disk_parameters
    implicit none

    ! Circumprimary disks
    double precision :: b_prim(5)
    double precision :: c_prim(5)

    ! Circumsecondary disks
    double precision :: b_sec(5)
    double precision :: c_sec(5)

    contains

    subroutine initialize_disk_parameters(R)
        double precision, intent(in) :: R
        
        ! Circumprimary disk parameters
        !Equation set for mu=0.1: 
        b_prim(1) = 9.764309764309791e-13*R**2 - 1.1074074074074087e-06*R - 0.6490235690235693
        c_prim(1) = 1.6611e-12*R**2 - 1.9605e-06*R + 8.5944e-01
        !Equation set for mu=0.2: 
        b_prim(2) = 6.509539842873163e-13*R**2 - 7.382716049382692e-07*R - 0.7126823793490461
        c_prim(2) = 1.6611e-12*R**2 - 1.9605e-06*R + 8.9944e-01
        !Equation set for mu=0.1: 
        b_prim(3) = 4.3771043771043816e-13*R**2 - 4.925925925925918e-07*R - 0.7551178451178455
        c_prim(3) = 1.7733e-12*R**2 - 2.0840e-06*R + 9.4066e-01
        !Equation set for mu=0.1: 
        b_prim(4) = 4.3771043771043937e-13*R**2 - 4.925925925925932e-07*R - 0.7651178451178456
        c_prim(4) = 1.7733e-12*R**2 - 2.0840e-06*R + 9.7066e-01
        !Equation set for mu=0.1: 
        b_prim(5) = 3.2547699214366364e-13*R**2 - 3.691358024691398e-07*R - 0.7763411896745228
        c_prim(5) = 1.6611e-12*R**2 - 1.9605e-06*R + 9.5944e-01

        ! Circumsecondary disk parameters
        !Equation set for mu=0.1: 
        b_sec(1) = -2.244668911335608e-14*R**2 + 2.4691358024707388e-09*R - 0.8100224466891136
        c_sec(1) = 1.8967e-12*R**2 - 2.2086e-06*R + 1.0019e+00
        !Equation set for mu=0.2: 
        b_sec(2) = 1.0101010101009552e-13*R**2 - 1.2222222222221502e-07*R - 0.808787878787879
        c_sec(2) = 1.7733e-12*R**2 - 2.0840e-06*R + 1.0107e+00
        !Equation set for mu=0.3: 
        b_sec(3) = 3.254769921436567e-13*R**2 - 3.691358024691327e-07*R - 0.7863411896745232
        c_sec(3) = 1.6611e-12*R**2 - 1.9605e-06*R + 9.8944e-01
        !Equation set for mu=0.4: 
        b_sec(4) = 2.132435465768843e-13*R**2 - 2.456790123456824e-07*R - 0.7975645342312008
        c_sec(4) = 1.8855e-12*R**2 - 2.2074e-06*R + 1.0019e+00
        !Equation set for mu=0.5: 
        b_sec(5) = 2.1324354657688054e-13*R**2 - 2.456790123456777e-07*R - 0.7875645342312014
        c_sec(5) = 1.7733e-12*R**2 - 2.0840e-06*R + 9.7066e-01
    end subroutine initialize_disk_parameters

end module disk_parameters