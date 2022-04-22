!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                  
!   ICM Wetland Morphology Grid Averaging
!                                                  
!                                                  
!   Fortran code to write DEM pixel-level data to text file that will be processed with a Python script
!   to develop zonal averages (e.g. average water elevation within an ICM-LAVegMod grid cell or ICM-Hydro compartment.
!   
!   Command line arguments passed into this executable:
!   
!   1 = dem_file      : full path to binary raster file for DEM
!   2 = lwf_file      : full path to binary raster file for landtype classification
!   3 = grid_file    : full path to binary raster file for grid cell ID values
!   4 = comp_file     :file name, with relative path, to ICM-LAVegMod grid map file that is same resolution and structure as DEM XYZ
!   5 = nras_str      : number of raster pixels of dataset, must match size of binary arrays
!   6 = noData_str    : number to treat as NoData in the raster datasets

!                                                  
!   Questions: eric.white@la.gov                   
!   last update: 4/22/2022
!                                                     
!   project site: https://github.com/CPRA-MP      
!   documentation: http://coastal.la.gov/our-plan  
!                                                  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

program main

    implicit none

    ! definie generic variables
    integer,parameter :: sp=selected_real_kind(p=6) 
    integer,parameter :: fn_len=300                                 ! maximum character length allowed for filename character strings read in from input_params.csv
   
    ! define text string variables that are passed in from shell during program call
    character*fn_len :: dem_file                                    ! file name, with relative path, to DEM XYZ file
    character*fn_len :: lwf_file                                    ! file name, with relative path, to land/water file that is same resolution and structure as DEM XYZ
    character*fn_len :: edge_file                                   ! file name, with relative path, to marsh edge file that is same resolution and structure as DEM XYZ
    character*fn_len :: grid_file                                   ! file name, with relative path, to ICM-LAVegMod grid map file that is same resolution and structure as DEM XYZ
    character*fn_len :: comp_file                                   ! file name, with relative path, to ICM-Hydro compartment map file that is same resolution and structure as DEM XYZ
    character*fn_len :: out_file                                    ! file name, with relative path, to CSV file that will save output from this program

    character*20 :: nras_str                                        ! string storing the number of DEM pixels in master DEM - passed in from shell
    character*20 :: noData_str                                      ! string storing the value representing NoData in input XYZ rasters - passed in from shell
    
    ! define variables used by main program
    integer :: i                                                    ! iterator
    integer :: ndem                                                 ! number of DEM pixels in master DEM
    integer :: dem_NoDataVal                                        ! value representing NoData in input XYZ rasters
    
    real(sp),dimension(:),allocatable :: dem_z                      ! average elevation of DEM pixel (m NAVD88)
    integer,dimension(:),allocatable  :: dem_comp                   ! ICM-Hydro compartment ID overlaying DEM pixel (-)
    integer,dimension(:),allocatable  :: dem_grid                   ! ICM-LAVegMod grid ID overlaying DEM pixel (-)
    integer,dimension(:),allocatable  :: grid_comp                  ! ICM-Hydro compartment ID overlaying ICM-LAVegMod grid (-)
    integer,dimension(:),allocatable  :: dem_edge                   ! flag indicating whether DEM pixel is edge (0=non edge; 1=edge)
    integer,dimension(:),allocatable  :: dem_lndtyp                 ! Land type classification of DEM pixel
                                                                    !               1 = vegetated wetland
                                                                    !               2 = water
                                                                    !               3 = unvegetated wetland/new subaerial unvegetated mudflat (e.g., bare ground)
                                                                    !               4 = developed land/upland/etc. that are not modeled in ICM-LAVegMod
                                                                    !               5 = flotant marsh


    ! read in variables from function call - passed in from shell command line
    call GET_COMMAND_ARGUMENT(1,dem_file)
    call GET_COMMAND_ARGUMENT(2,lwf_file)
    call GET_COMMAND_ARGUMENT(3,edge_file)
    call GET_COMMAND_ARGUMENT(4,grid_file)
    call GET_COMMAND_ARGUMENT(5,comp_file)
    call GET_COMMAND_ARGUMENT(6,nras_str)
    call GET_COMMAND_ARGUMENT(7,noData_str)
    call GET_COMMAND_ARGUMENT(8,out_file)
    
    ! set variable values from input strings
    read(nras_str,*) ndem
    read(noData_str,*) dem_NoDataVal
    
    ! read in binary DEM raster
    allocate(dem_z(ndem))
    open(unit=100, file = trim(adjustL(dem_file)),form='unformatted')
    read(100) dem_z
    close(100)

    ! read in binary landtype raster
    allocate(dem_lndtyp(ndem))
    open(unit=101, file = trim(adjustL(lwf_file)),form='unformatted')
    read(101) dem_lndtyp
    close(101)

    ! read in binary marsh edge raster
    allocate(dem_edge(ndem))
    open(unit=103, file = trim(adjustL(edge_file)),form='unformatted')
    read(103) dem_edge
    close(103)

    ! read in binary raster containing ICM-LAVegMod grid cell ID value for each DEM pixel location
    allocate(dem_grid(ndem))
    open(unit=104, file = trim(adjustL(grid_file)),form='unformatted')
    read(104) dem_grid
    close(104)

    ! read in binary raster containing ICM-Hydro compartment ID value for each DEM pixel location
    allocate(dem_comp(ndem))
    open(unit=105, file = trim(adjustL(comp_file)),form='unformatted') 
    read(105) dem_comp
    close(105)
    
    ! write output CSV file
    open(unit=200, file = trim(adjustL(out_file) ) )
    write(200,'(A)') 'ndem,ICM_LAVegMod_GridCell,ICM_Hydro_Compartment,landtype,edge,z_NAVD88_m'
    do i = 1,ndem
        write(200,2000) i,dem_grid(i),dem_comp(i),dem_lndtyp(i),dem_edge(i),dem_z(i)
    end do
    
2000    format( 5(I0,','), F0.4 )    

end program
