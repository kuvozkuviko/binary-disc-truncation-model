! File to read the csv files in Fortran, ultimately unecessary since this is already done much easier with Pandas in Python

program read_csv
    implicit none
    ! Declare variables
    integer :: ios, n_rows, ID              ! ios for I/O status, n_rows for loop counter, ID for row index
    real(8) :: all_au(1000), above_10_au(1000)  ! Arrays to store data from the CSV file
    real(8) :: temp                          ! Temporary variable to store unused column data

    ! Open csv file
    open(unit=10, file='/home/andres/Documents/Astroworld/disk_pop/1e-3/mean_aspect_ratio_1e-3.csv', &
         status='old', action='read', iostat=ios)

    ! Check if file was opened successfully
    if (ios /= 0) then
        print*, 'Error opening CSV file, ios =', ios
        stop
    endif

    ! Skip the title row by reading it and not storing the result
    read(10, *, iostat=ios)
 !   if (ios /= 0) then
 !       print*, 'Error reading title row'
  !      stop
  !  endif

    ! Loop to read 1000 rows of data from the CSV file
    do n_rows = 1, 1000
        ! Read values from each row into corresponding variables
        read(10, *, iostat=ios) ID, all_au(n_rows), above_10_au(n_rows), temp     
        ! Check if reading the row failed (e.g., file ends early) 
        if (ios /= 0) then
            print*, 'Error opening CSV file, ios =', ios
            stop
        endif    
        ! Print the values to the console (for verification)
        write(*, *) ID, all_au(n_rows), above_10_au(n_rows), temp 
    end do

    ! Close the file after reading
    close(10)
  
end program read_csv