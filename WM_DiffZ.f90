subroutine DiffZ

    use params
    implicit none

    
    real(sp),dimension(:),allocatable :: ras1
    real(sp),dimension(:),allocatable :: ras0
    real(sp),dimension(:),allocatable :: ras01
    real(sp) :: noData
    integer :: i
    

    read(noData_str,*) noData

    allocate(ras1(nras))
    allocate(ras0(nras))
    allocate(ras01(nras))
    
    ras1  = 0.0
    ras0  = 0.0
    ras01 = 0.0
    
    write(*,'(a,a)') 'comparing:  ', trim(adjustL(ras1_bin_pth))
    write(*,'(a,a)') '       to:  ', trim(adjustL(ras0_bin_pth))
    
    open(unit=100, file = trim(adjustL(ras1_bin_pth)),form='unformatted')
    read(100) ras1
    close(100)

    open(unit=101, file = trim(adjustL(ras0_bin_pth)),form='unformatted')
    read(101) ras0
    close(101)
    

    do i=1,nras
        if (ras1(i) == noData) then
            ras01(i) = noData
        elseif (ras0(i) == noData) then
            ras01(i) = noData
        else
            ras01(i) = ras1(i) - ras0(i)
        end if
    end do

    open(unit=200, file = trim(adjustL(ras01_bin_pth)),form='unformatted')
    write(*,'(A,A)') ' saved to: ',trim(adjustL(ras01_bin_pth))    
    write(200) ras01
    close(200)
    
    return
end
