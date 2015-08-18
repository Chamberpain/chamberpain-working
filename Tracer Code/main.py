import pxssh
import getpass
import paramiko
import matplotlib 
from numpy import *
import pylab as plt
from pylab import *
import fnmatch
import os
from netCDF4 import Dataset
import random
from fabric.api import *
###### Setup ####### 
outnames = ['TEST_0000_0001.GRAD.0000000002.data','TEST_0000_0001.TSG.0000000002.data','TEST_0000_0001.GRAD.0000000003.data','TEST_0000_0001.TSG.0000000003.data','TEST_0000_0001.MLD.0000000002.data','TEST_0000_0001.MLD.0000000003.data','TEST_0000_0001.XYZ.0000000002.data','TEST_0000_0001.XYZ.0000000003.data']
npts = 1000
position_init_file = 'particle_init.bin'
init_file = 'NML.TEST_0000'
init_data = ['&PARAM\n', 
"casename='TEST_0000',\n", 
"path2uvw='../data/',\n", 
"fn_UVEL='UVEL.0000000100.data',\n", 
"fn_VVEL='VVEL.0000000100.data',\n", 
"fn_WVEL='WVEL.0000000100.data',\n", 
"fn_THETA='THETA.0000000100.data',\n", 
"fn_SALT='SALT.0000000100.data',\n", 
"fn_GAMMA='GAMMA.0000000100.data',\n", 
"fn_PHIHYD='',\n", 
"fn_parti_init='"+position_init_file+"',\n", 
'target_density=27.4,\n', 
'vel_stationary=.False.,\n', 
'Npts='+str(npts)+',\n', 
'dt_reinit=-1,\n', 
'dt_mld=4320.,\n', 
'dt=4320,\n', 
'tstart=0.,\n', 
'tend=86400000.,\n', 
'NPP=1,\n', 
'dt_case=8640,\n', 
'pickup=0.,\n', 
'dumpFreq=86400.,\n', 
'diagFreq=864000.,\n', 
'pickupFreq=7776000.,\n', 
'saveTSG=.FALSE.,\n', 
'useMLD=.TRUE.,\n', 
'useKh=.TRUE.,\n', 
'Khdiff=25.0,\n', 
'Kvdiff=1e-5,\n', 
'/\n']
temp = open(init_file,'w')
temp.writelines(init_data)
temp.close()
####################

def argo_matches(): 
    matches = []
    for root, dirnames, filenames in os.walk('/Users/paulchamberlain/Data'):
        for filename in fnmatch.filter(filenames, '*.nc'):
            matches.append(os.path.join(root, filename))
    return matches

def net_cdf_read(match):
    nc_fid = Dataset(match, 'r') 
    lat = nc_fid.variables['LATITUDE']
    lat = lat[lat!=lat._FillValue]
    start_lat = (lat[0]+77.875)*6
    lon = nc_fid.variables['LONGITUDE']
    lon = lon[lon!=lon._FillValue]
    start_lon = lon[0]*6
    start_time = nc_fid.variables['JULD'][0]
    make_init_file(start_lat,start_lon)
    file_upload_run()
#    file_download(outnames)

def make_init_file(start_lat,start_lon):
    xyz=zeros((npts,3))
    xyz[:,0]= [random.uniform(start_lon-0.5,start_lon+0.5) for _ in xrange(npts)] # x index 100 points
    xyz[:,1]= [random.uniform(start_lat-0.5,start_lat+0.5) for _ in xrange(npts)] # y index 100 points
    xyz[:,2]=20 # at k=20 level, z level will be overwritten if the target_density in the namelist is larger than 0.
    xyz.T.astype('>f8').tofile(position_init_file) #the saving sequence should be x[:], y[:], z[:], not [x1,y1,z1],[x2,y2,z2]...

def file_upload_run():
    with settings(host_string="gyre.ucsd.edu", user = "pchamber", password="==$pArKy2015"):
        filepath = '/home/pchamber/Tracer/src/particle_init.bin'
        localpath = './particle_init.bin'
        put(filepath,localpath)
        filepath = '/home/pchamber/Tracer/src/NML.TEST_0000'
        localpath = './NML.TEST_0000'
        put(filepath,localpath)
        run("cd /home/pchamber/Tracer/src && ./opt.ensemble < NML.TEST_0000")

def file_download(outnames):
    host = "gyre.ucsd.edu"
    port = 22
    transport = paramiko.Transport((host, port))
    password = "==$pArKy2015"
    username = "pchamber"
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    for name in outnames:
        filepath = '/home/pchamber/Tracer/src/output/'+name
        localpath = './Output/'+name
        sftp.get(filepath, localpath)
    sftp.close()
    transport.close()

matches = argo_matches()
for match in matches[:1]:
    net_cdf_read(match)

# opt=fromfile('./Output/'+filenames[-1],'>f4').reshape(-1,3,npts)
# x,y=opt[0,0,:],opt[0,1,:] #this is in model grid index coordinate, convert to lat-lon using x=x/6.0;y=y/6.0-77.875
# x=x/6.0;y=y/6.0-77.875
# plot(x,y,'r-')
# opt=fromfile('./Output/'+filenames[-2],'>f4').reshape(-1,3,npts)
# x,y=opt[0,0,:],opt[0,1,:] #this is in model grid index coordinate, convert to lat-lon using x=x/6.0;y=y/6.0-77.875
# x=x/6.0;y=y/6.0-77.875
# plot(x,y,'b-')
# xlabel('x')
# ylabel('y')
# show()