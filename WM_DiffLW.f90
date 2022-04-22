subroutine DiffLW
    ! lndtyp 1 = vegetated wetland
    ! lndtyp 2 = water
    ! lndtyp 3 = unvegetated wetland/new subaerial unvegetated mudflat (e.g., bare ground)
    ! lndtyp 4 = developed land/upland/etc. that are not modeled in ICM-LAVegMod
    ! lndtyp 5 = flotant marsh
    
    ! combinations when comparison raster (ras0) is vegetated land (lndtyp=1)
    ! no difference in landtype:        ras01 = 11
    ! vegetated land loss:              ras01 = 12
    ! loss of vegetation:               ras01 = 13
    ! new upland from marsh:            ras01 = 14      ! this combination should not appear since this process is not currently in ICM-Morph
    ! new flotant from marsh:           ras01 = 15      ! this combination should not appear since this process is not currently in ICM-Morph
    
    ! combinations when comparison raster (ras0) is water (lndtyp=2)
    ! vegetated land gain:              ras01 = 21
    ! no difference in landtype:        ras01 = 22
    ! new bareground/mudflat:           ras01 = 23
    ! new upland from water:            ras01 = 24      ! this combination should not appear since this process is not currently in ICM-Morph
    ! new flotant from water:           ras01 = 25      ! this combination should not appear since this process is not currently in ICM-Morph
    
    ! combinations when comparison raster (ras0) is mudflat/bareground (lndtyp=3)
    ! vegetation gain:                  ras01 = 31
    ! bareground/mudflat land loss:     ras01 = 32
    ! no difference in landtype:        ras01 = 33
    ! new upland from bareground:       ras01 = 34      ! this combination should not appear since this process is not currently in ICM-Morph
    ! new flotant from bareground:      ras01 = 35      ! this combination should not appear since this process is not currently in ICM-Morph
        
    ! combinations when comparison raster (ras0) is developed/upland (lndtyp=4)
    ! vegetated marsh gain:             ras01 = 41      ! this combination should not appear since this process is not currently in ICM-Morph
    ! upland/developed land loss:       ras01 = 42      ! this combination should not appear since this process is not currently in ICM-Morph
    ! new bareground from upland:       ras01 = 43      ! this combination should not appear since this process is not currently in ICM-Morph
    ! no difference in landtype:        ras01 = 44
    ! new flotant from upland:          ras01 = 45      ! this combination should not appear since this process is not currently in ICM-Morph
    
    ! combinations when comparison raster (ras0) is flotant marsh (lndtyp=5)
    ! vegetated land gain:              ras01 = 51
    ! flotant marsh loss:               ras01 = 52
    ! new bareground gain from flotant: ras01 = 53
    ! new upland from flotant:          ras01 = 54      ! this combination should not appear since this process is not currently in ICM-Morph    
    ! no difference in landtype:        ras01 = 55
    
    use params
    implicit none

    
    integer,dimension(:),allocatable :: ras1
    integer,dimension(:),allocatable :: ras0
    integer,dimension(:),allocatable :: ras01
    integer :: noData
    integer :: i
    

    read(noData_str,*) noData

    allocate(ras1(nras))
    allocate(ras0(nras))
    allocate(ras01(nras))
    
    ras1  = 0
    ras0  = 0
    ras01 = 0
    
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
            ras01(i) = 10*ras0(i) + ras1(i)
        end if
    end do

    open(unit=200, file = trim(adjustL(ras01_bin_pth)) , form='unformatted' )
    write(*,'(A,A)') ' saved to: ',trim(adjustL(ras01_bin_pth))    
    write(200) ras01
    close(200)
    
    return
end