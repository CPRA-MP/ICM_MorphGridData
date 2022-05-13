import os
import sys
import subprocess
import numpy as np

mpterm = 'MP2023'
sterm = 'S%02d' % int(sys.argv[1])
gterm = 'G%03d' % int(sys.argv[2])
cterm = 'C000'
uterm = 'U00'
vterm = 'V00'
rterm = 'SLA'
startyear = 2019
year = int(sys.argv[3])
elapsedyear = year - startyear +1

print('\nPreparing summary files for grid and compartment zonal statistics for %s %s - %d' % (sterm, gterm,year) )

par_dir = os.getcwd()

MorphGridData_exe_path = './morph_grid_data_v23.0.0'

runprefix    = '%s_%s_%s_%s_%s_%s_%s'   % (mpterm,sterm,gterm,cterm,uterm,vterm,rterm)        
file_oprefix = '%s_O_%02d_%02d'         % (runprefix,elapsedyear,elapsedyear)        
file_prefix  = '%s_N_%02d_%02d'         % (runprefix,elapsedyear,elapsedyear)

dem_file  = '%s/%s/%s/geomorph/output/%s_N_%02d_%02d_W_dem30.xyz.b'                           % (par_dir, sterm, gterm, runprefix,elapsedyear,elapsedyear)
lwf_file  = '%s/%s/%s/geomorph/output/%s_N_%02d_%02d_W_lndtyp30.xyz.b'                        % (par_dir, sterm, gterm, runprefix,elapsedyear,elapsedyear)
edge_file = '%s/%s/%s/geomorph/output/%s_N_%02d_%02d_W_edge30.xyz.b'                          % (par_dir, sterm, gterm, runprefix,elapsedyear,elapsedyear)
grid_file = '%s/%s/%s/geomorph/input/MP2023_S00_G000_C000_U00_V00_SLA_I_00_00_W_grid30.xyz.b' % (par_dir, sterm, gterm)
comp_file = '%s/%s/%s/geomorph/input/MP2023_S00_G000_C000_U00_V00_SLA_I_00_00_W_comp30.xyz.b' % (par_dir, sterm, gterm)
out_file  = '%s/%s/%s/geomorph/output/%s_N_%02d_%02d_W_grid_data.csv'                         % (par_dir, sterm, gterm, runprefix,elapsedyear,elapsedyear)
ndem = 171284090
dem_NoDataVal = -9999
dem_res = 30
n500grid = 173898
ncomp = 1778

Gdw_bin_n = 14    # number of water depth bins used by Gadwall HSI
GwT_bin_n = 9     # number of water depth bins used by Greenwing Teal HSI
MtD_bin_n = 9     # number of water depth bins used by Mottled Duck HSI


fortran_run = subprocess.call([MorphGridData_exe_path, dem_file, lwf_file, edge_file, grid_file, comp_file, str(ndem), str(dem_NoDataVal),out_file])
print('Finished running %s.' % MorphGridData_exe_path)

print('Reading in %s.' % monthly_stg_file)
monthly_stg_file = '%s/%s/%s/hydro/TempFiles/compartment_monthly_mean_stage_%04d.csv'  % (par_dir, sterm, gterm, year)
# comp,stage_m_01,stage_m_02,stage_m_03,stage_m_04,stage_m_05,stage_m_06,stage_m_07,stage_m_08,stage_m_09,stage_m_10,stage_m_11,stage_m_12
comp_mon_stg = {}
with open(monthly_stg_file,mode='r') as comp_stg_data:
    nline = 0
    for line in comp_stg_data:
        if nline > 0:
            c = int(line.split(',')[0])
            comp_mon_stg[c] = {}
            for n_mon in range(1,13):
                comp_mon_stg[c][n_mon] = int(line.split(',')[n_mon])
    nline += 1

print('Reading in %s.' % out_file)

grid_bed_z_all = {}
grid_bed_z = {} 

grid_land_z_all = {}
grid_land_z = {}
 
grid_pct_land_all = {}
grid_pct_land = {}

grid_pct_land_wetl_all = {} 
grid_pct_land_wetl = {} 

grid_pct_water_all = {} 
grid_pct_water = {} 

grid_pct_edge_all = {}
grid_pct_edge = {}

grid_Gdw_depths = {}
grid_GwT_depths = {}
grid_MtD_depths = {}

comp_water_z_all = {}
comp_water_z = {}

comp_wetland_z_all = {}
comp_wetland_z = {}

comp_edge_area_all = {}
comp_edge_area = {}

comp_pct_water_all = {}
comp_pct_water = {}

comp_pct_upland_all = {}
comp_pct_upland = {}

for g in range(1,n500grid+1):
    grid_bed_z_all[g] = []         
    grid_bed_z[g] = 0.0         
    
    grid_land_z_all[g] = []      
    grid_land_z[g] = 0.0

    grid_pct_land_all[g] = []    
    grid_pct_land[g] = 0.0
    
    grid_pct_land_wetl_all[g] = [] 
    grid_pct_land_wetl[g] = 0.0
    
    grid_pct_water_all[g] = []
    grid_pct_water[g] = 0.0     
    
    grid_pct_edge_all[g] = []      
    grid_pct_edge[g] = 0.0

    grid_Gdw_depths[g] = []
    for Gdw_bin in range(0,Gdw_bin_n + 1):
        grid_Gdw_depths[g][Gdw_bin] = 0.0
        
    grid_GwT_depths[g] = []
    for GwT_bin in range(0,GwT_bin_n + 1):
        grid_GwT_depts[g][GwT_bin] = 0.0
        
    grid_MtD_depths[g] = []    
    for MtD_bin in range(0,MtD_bin_n + 1):
        grid_MtD_depths[g][MtD_bin] = 0.0
    
for c in range(1,ncomp+1):                           
    comp_water_z_all[c] = []       
    comp_water_z[c] = 0.0
           
    comp_wetland_z_all[c] = [] 
    comp_wetland_z[c] = 0.0    
    
    comp_edge_area_all[c] = []    
    comp_edge_area[c] = 0.0    
    
    comp_pct_water_all[c] = []    
    comp_pct_water[c] = 0.0    
    
    comp_pct_upland_all[c] = []   
    comp_pct_upland[c] = 0.0   

fivepct = range(1,ndem,int(np.floor(ndem/20)))

with open(out_file,mode='r') as grid_data:
    nline = 0
    for line in grid_data:
        if nline > 0:   # header: ndem,ICM_LAVegMod_GridCell,ICM_Hydro_Compartment,landtype,edge,z_NAVD88_m
            if nline in fivepct:
                print('%d%s...' % (fivepct.index(nline)*5,'%'),end="")
                sys.stdout.flush()
            elif nline == ndem:
                 print('100%. Done.')
            
            g     = int(float(line.split(',')[1]))
            c   = int(float(line.split(',')[2]))
            lndtyp = int(float(line.split(',')[3]))
            edge   = int(float(line.split(',')[4]))
            elev   = float(line.split(',')[5])
            
            if c > 0:
                comp_edge_area_all[c].append(edge*dem_res*dem_res)
                if lndtyp == 2:
                    comp_water_z_all[c].append(elev)
                    comp_pct_water_all[c].append(1)
                else:
                    if lndtyp != 4:     # check if upland/developed
                        comp_wetland_z_all[c].append(elev)
                    else:
                        comp_pct_upland_all[c].append(1)
            
            if g > 0:
                grid_pct_edge_all[g].append(edge)
                if lndtyp == 2:
                    grid_bed_z_all[g].append(elev)
                    grid_pct_water_all[g].append(1)
                else:
                    grid_land_z_all[g].append(elev)
                    grid_pct_land_all[g].append(1)
                    if lndtyp != 4:     # check if upland/developed
                        grid_pct_land_wetl_all[g].append(1)
                
               
                if c > 0:
                    dep_oct_apr = (comp_mon_stg[c][1]+comp_mon_stg[c][2]+comp_mon_stg[c][3]+comp_mon_stg[c][4]+comp_mon_stg[c][10]+comp_mon_stg[c][11]+comp_mon_stg[c][12])/7.0
                    dep_sep_mar = (comp_mon_stg[c][1]+comp_mon_stg[c][2]+comp_mon_stg[c][3]+comp_mon_stg[c][9]+comp_mon_stg[c][10]+comp_mon_stg[c][11]+comp_mon_stg[c][12])/7.0
                    dep_ann     = (comp_mon_stg[c][1]+comp_mon_stg[c][2]+comp_mon_stg[c][3]+comp_mon_stg[c][4]+comp_mon_stg[c][5]+comp_mon_stg[c][6]+comp_mon_stg[c][7]+comp_mon_stg[c][8]+comp_mon_stg[c][9]+comp_mon_stg[c][10]+comp_mon_stg[c][11]+comp_mon_stg[c][12])/12.0
                    
                    # tabulate area of grid cell within each Gadwall depth bin; depth thresholds (in m) are: [0,0.04,0.08,0.12,0.18,0.22,0.28,0.32,0.36,0.40,0.44,0.78,1.50]     
                    if dep_oct_apr <= 0.0:
                        grid_Gdw_depths[g][1]  = grid_Gdw_depths[g][1] + dem_res**2
                    elif dep_oct_apr <= 0.04:
                        grid_Gdw_depths[g][2]  = grid_Gdw_depths[g][2] + dem_res**2
                    elif dep_oct_apr <= 0.08:
                        grid_Gdw_depths[g][3]  = grid_Gdw_depths[g][3] + dem_res**2
                    elif dep_oct_apr <= 0.12:
                        grid_Gdw_depths[g][4]  = grid_Gdw_depths[g][4] + dem_res**2
                    elif dep_oct_apr <= 0.18:
                        grid_Gdw_depths[g][5]  = grid_Gdw_depths[g][5] + dem_res**2
                    elif dep_oct_apr <= 0.22:
                        grid_Gdw_depths[g][6]  = grid_Gdw_depths[g][6] + dem_res**2
                    elif dep_oct_apr <= 0.28:
                        grid_Gdw_depths[g][7]  = grid_Gdw_depths[g][7] + dem_res**2
                    elif dep_oct_apr <= 0.32:
                        grid_Gdw_depths[g][8]  = grid_Gdw_depths[g][8] + dem_res**2
                    elif dep_oct_apr <= 0.36:
                        grid_Gdw_depths[g][9]  = grid_Gdw_depths[g][9] + dem_res**2
                    elif dep_oct_apr <= 0.40:
                        grid_Gdw_depths[g][10] = grid_Gdw_depths[g][10] + dem_res**2
                    elif dep_oct_apr <= 0.44:
                        grid_Gdw_depths[g][11] = grid_Gdw_depths[g][11] + dem_res**2
                    elif dep_oct_apr <= 0.78:
                        grid_Gdw_depths[g][12] = grid_Gdw_depths[g][12] + dem_res**2
                    elif dep_oct_apr <= 1.50:
                        grid_Gdw_depths[g][13] = grid_Gdw_depths[g][13] + dem_res**2
                    else
                        grid_Gdw_depths[g][14] = grid_Gdw_depths[g][14] + dem_res**2
                    
                    # tabulate area of grid cell within each Greenwing Teal depth bin; depth thresholds (in m) are: [0,0.06,0.18,0.22,0.26,0.30,0.34,1.0]
                    if dep_sep_mar <= 0.0:
                        grid_GwT_depths[g][1] = grid_GwT_depths[g][1] + dem_res**2
                    elif dep_sep_mar <= 0.06:
                        grid_GwT_depths[g][2] = grid_GwT_depths[g][2] + dem_res**2
                    elif dep_sep_mar <= 0.18:
                        grid_GwT_depths[g][3] = grid_GwT_depths[g][3] + dem_res**2
                    elif dep_sep_mar <= 0.22:
                        grid_GwT_depths[g][4] = grid_GwT_depths[g][4] + dem_res**2
                    elif dep_sep_mar <= 0.26:
                        grid_GwT_depths[g][5] = grid_GwT_depths[g][5] + dem_res**2
                    elif dep_sep_mar <= 0.30:
                        grid_GwT_depths[g][6] = grid_GwT_depths[g][6] + dem_res**2
                    elif dep_sep_mar <= 0.34:
                        grid_GwT_depths[g][7] = grid_GwT_depths[g][7] + dem_res**2
                    elif dep_sep_mar <= 1.0:
                        grid_GwT_depths[g][8] = grid_GwT_depths[g][8] + dem_res**2
                    else
                        grid_GwT_depths[g][9] = grid_GwT_depths[g][9] + dem_res**2
                       
                    # tabulate area of grid cell within each Mottled Duck depth bin; depth thresholds (in m) are: [0,0.08,0.30,0.36,0.42,0.46,0.50,0.56]
                    if dep_ann <= 0.0:        
                        grid_MtD_depths[g][1] = grid_MtD_depths[g][1] + dem_res**2
                    elif dep_ann <= 0.08:            
                        grid_MtD_depths[g][2] = grid_MtD_depths[g][2] + dem_res**2
                    elif dep_ann <= 0.30:            
                        grid_MtD_depths[g][3] = grid_MtD_depths[g][3] + dem_res**2
                    elif dep_ann <= 0.36:            
                        grid_MtD_depths[g][4] = grid_MtD_depths[g][4] + dem_res**2
                    elif dep_ann <= 0.42:            
                        grid_MtD_depths[g][5] = grid_MtD_depths[g][5] + dem_res**2
                    elif dep_ann <= 0.46:            
                        grid_MtD_depths[g][6] = grid_MtD_depths[g][6] + dem_res**2
                    elif dep_ann <= 0.50] then            
                        grid_MtD_depths[g][7] = grid_MtD_depths[g][7] + dem_res**2
                    elif dep_ann <= 0.56:            
                        grid_MtD_depths[g][8] = grid_MtD_depths[g][8] + dem_res**2
                    else
                        grid_MtD_depths[g][9] = grid_MtD_depths[g][9] + dem_res**2

        nline += 1

# determine zonal averages over each ICM-LAVegMod grid cell
for g in range(1,n500grid+1):
    ng = len(grid_bed_z_all[g]) + len(grid_land_z_all[g])
    
    if ng > 0:
        grid_bed_z[g]          = sum(grid_bed_z_all[g]) / ng
        grid_land_z[g]         = sum(grid_land_z_all[g]) / ng
        grid_pct_land[g]       = 100.0*sum(grid_pct_land_all[g]) / ng
        grid_pct_land_wetl[g]  = 100.0*sum(grid_pct_land_wetl_all[g]) / ng
        grid_pct_water[g]      = 100.0*sum(grid_pct_water_all[g]) / ng
        grid_pct_edge[g]       = 100.0*sum(grid_pct_edge_all[g]) / ng
    else:
        grid_bed_z[g]          = 0.0
        grid_land_z[g]         = 0.0
        grid_pct_land[g]       = 0.0
        grid_pct_land_wetl[g]  = 0.0
        grid_pct_water[g]      = 0.0
        grid_pct_edge[g]       = 0.0
        

# determine zonal averages over each ICM-Hydro compartment
for c in range(1,ncomp+1):    
    nc = len(comp_water_z_all[c]) + len(comp_wetland_z_all[c]) + len(comp_pct_upland_all[c])

    if nc > 0:
        comp_pct_upland[c] = sum(comp_pct_upland_all[c]) / nc
        comp_water_z[c]    = sum(comp_water_z_all[c]   ) / nc
        comp_wetland_z[c]  = sum(comp_wetland_z_all[c] ) / nc
        comp_pct_water[c]  = sum(comp_pct_water_all[c] ) / nc
        comp_edge_area[c]  = sum(comp_edge_area_all[c] )
    else:
        comp_pct_upland[c] = 0.0
        comp_water_z[c]    = 0.0
        comp_wetland_z[c]  = 0.0
        comp_pct_water[c]  = 0.0
        comp_edge_area[c]  = 0.0        
        

# output files
new_grid_filepath   = '%s/%s/%s/hydro/TempFiles/grid_data_500m_end%d.csv' % (par_dir, sterm, gterm, year)
comp_elev_file      = '%s/%s/%s/hydro/TempFiles/compelevs_end_%d.csv' % (par_dir, sterm, gterm, year)
comp_wat_file       = '%s/%s/%s/hydro/TempFiles/PctWater_%d.csv' % (par_dir, sterm, gterm, year)
comp_upl_file       = '%s/%s/%s/hydro/TempFiles/PctUpland_%d.csv' % (par_dir, sterm, gterm, year)
grid_pct_edge_file  = '%s/%s/%s/hsi/%s_W_pedge.csv' % (par_dir, sterm, gterm, file_prefix)

grid_Gdw_dep_file   = '%s/%s/%s/hsi/GadwallDepths_cm_%d.csv' % (par_dir, sterm, gterm, year)
grid_GwT_dep_file   = '%s/%s/%s/hsi/GWTealDepths_cm__%d.csv' % (par_dir, sterm, gterm, year)
grid_MtD_dep_file   = '%s/%s/%s/hsi/MotDuckDepths_cm_%d.csv' % (par_dir, sterm, gterm, year)

grid_data_file     = new_grid_filepath  

print('Writing output files:')
with open(grid_data_file,mode='w') as gdaf:  
    print('     - %s' % grid_data_file)
    gdaf.write('GRID,MEAN_BED_ELEV,MEAN_LAND_ELEV,PERCENT_LAND_0-100,PERCENT_WETLAND_0-100,PERCENT_WATER_0-100\n')
    for g in grid_bed_z.keys():
        gdaf.write('%d,%0.4f,%0.4f,%0.2f,%0.2f,%0.2f\n' % (g,grid_bed_z[g],grid_land_z[g],grid_pct_land[g],grid_pct_land_wetl[g],grid_pct_water[g]) )
    
with open(grid_pct_edge_file,mode='w') as gdef:  
    print('     - %s' % grid_pct_edge_file)
    gdef.write('GRID,PERCENT_EDGE_0-100\n')
    for g in grid_pct_edge.keys():
        gdef.write('%d,%0.4f' % (g,grid_pct_edge[g]) )
      
with open(comp_elev_file,mode='w') as cef:
    print('     - %s' % comp_elev_file)
    cef.write('ICM_ID,MEAN_BED_ELEV,MEAN_MARSH_ELEV,MARSH_EDGE_AREA\n')
    for c in comp_water_z.keys():
        cef.write('%d,%0.4f,%0.4f,%d\n' % (c,comp_water_z[c],comp_wetland_z[c],comp_edge_area[c]) )

with open(comp_wat_file, mode='w') as cwf:
    print('     - %s' % comp_wat_file)
    for c in comp_pct_water.keys():
        cwf.write( '%d,%0.4f\n' % (c,comp_pct_water[c]) )

with open(comp_upl_file, mode='w') as cuf:
    print('     - %s' % comp_upl_file)
    for c in comp_pct_upland.keys():
        cuf.write( '%d,%0.4f\n' % (c,comp_pct_upland[c]) )

with open(grid_Gdw_dep_file, mode='w') as Gdw:    
    Gdw.write('GRID_ID,VALUE_0,VALUE_4,VALUE_8,VALUE_12,VALUE_18,VALUE_22,VALUE_28,VALUE_32,VALUE_36,VALUE_40,VALUE_44,VALUE_78,VALUE_150,VALUE_151\n')
    for g in grid_Gdw_depths.keys():
        linewrite = '%d' % g
        for Gdw_bin in range(0,Gdw_bin_n + 1):
            linewrite = '%s,%d' % (linewrite,grid_Gdw_depths[g][Gdw_bin])
        Gdw.write('%s\n' % linewrite)

with open(grid_GwT_dep_file, mode='w') as GwT:
    GwT.write('GRID_ID,VALUE_0,VALUE_6,VALUE_18,VALUE_22,VALUE_26,VALUE_30,VALUE_34,VALUE_100,VALUE_101\n')
    for g in grid_GwT_depths.keys():
        linewrite = '%d' % g
        for GwT_bin in range(0,GwT_bin_n + 1):
            linewrite = '%s,%d' % (linewrite,grid_GwT_depths[g][GwT_bin])
        GwT.write('%s\n' % linewrite)

with open(grid_MtD_dep_file, mode='w') as MtD:
    MtD.write('GRID_ID,VALUE_0,VALUE_8,VALUE_30,VALUE_36,VALUE_42,VALUE_46,VALUE_50,VALUE_56,VALUE_57\n')
    for g in grid_MtD_depths.keys():
        linewrite = '%d' % g
        for MtD_bin in range(0,MtD_bin_n + 1):
            linewrite = '%s,%d' % (linewrite,grid_MtD_depths[g][MtD_bin])
        MtD.write('%s\n' % linewrite)
