print('\nPreparing summary files for grid and compartment zonal statistics.')

MorphGridData_exe_path = '%s/%s/%s/geomorph/morph_grid_data_v23.0.0' % (par_dir, sterm, gterm)

runprefix = '%s_%s_%s_%s_%s_%s_%s' % (mpterm,sterm,gterm,cterm,uterm,vterm,rterm)        
file_oprefix    = r'%s_O_%02d_%02d' % (runprefix,elapsedyear,elapsedyear)        

dem_file =  '%s/%s/%s/geomorph/output/%s_O_%02d_%02d_W_dem30.xyz.b' % (par_dir, sterm, gterm, runprefix)
lwf_file =  '%s/%s/%s/geomorph/output/%s_O_%02d_%02d_W_lndtyp30.xyz.b' % (par_dir, sterm, gterm, runprefix)
edge_file = '%s/%s/%s/geomorph/output/%s_O_%02d_%02d_W_edge30.xyz.b' % (par_dir, sterm, gterm, runprefix)
grid_file = '%s/%s/%s/geomorph/input/MP2023_S00_G000_C000_U00_V00_SLA_I_00_00_W_grid30.xyz' % (par_dir, sterm, gterm)
comp_file = '%s/%s/%s/geomorph/input/MP2023_S00_G000_C000_U00_V00_SLA_I_00_00_W_comp30.xyz' % (par_dir, sterm, gterm)
out_file = '%s/%s/%s/geomorph/output/%s_O_%02d_%02d_W_grid_data.csv' % (par_dir, sterm, gterm, runprefix)
ndem = 171284090
dem_NoDataVal = -9999

        
fortran_run = subprocess.call([MorphGridData_exe_path, dem_file, lwf_file, edge_file, grid_file, comp_file, ndem, dem_NoDataVal])


with open(out_file,mode='r') as grid_data:
    nline = 0
    for line in grid_data:
        if nline > 0:   # header: ndem,ICM_LAVegMod_GridCell,ICM_Hydro_Compartment,landtype,edge,z_NAVD88_m
            gr     = int(float(line.split(',')[1]))
            comp   = int(float(line.split(',')[2]))
            lndtyp = int(float(line.split(',')[3]))
            edge   = int(float(line.split(',')[4]))
            elev   = float(line.split(',')[5]))
            
            
        
        nline += 1
        
for g in sav_ave_dict.keys():
    ng = len(sav_all_dict[g])
    if ng > 0:
        sav_ave_dict[g] = sum(sav_all_dict[g]) / ng
    else:
        sav_ave_dict[g] = 0.0
