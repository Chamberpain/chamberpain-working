
def net_cdf_read(match):
    nc_fid = Dataset(match, 'r') 
    lat = nc_fid.variables['LATITUDE']
    lat = lat[lat!=lat._FillValue]
    start_lat = (lat[0]+77.875)*6
    lon = nc_fid.variables['LONGITUDE']
    lon = lon[lon!=lon._FillValue]
    start_lon = lon[0]*6
    reference_temp = nc_fid.variables['REFERENCE_DATE_TIME']
    reference_time = datetime.datetime(int(''.join(reference_temp[:4])),int(''.join(reference_temp[4:6])),int(''.join(reference_temp[6:8])))
    sose_start = datetime.datetime(2005,01,01)
    delta_time = sose_start- reference_time
    truth_array = nc_fid.variables['JULD'][:]>delta_time.days
    referenced_start = nc_fid.variables['JULD'][:]
    referenced_start = referenced_start[referenced_start>delta_time.days]
    time_advance = datetime.timedelta(days = referenced_start[0])
    start_time = reference_time+time_advance
    make_init_file(start_lat,start_lon)
    make_config(start_time,run_length)
    return lon,lat