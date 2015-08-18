from numpy import zeros
from numpy import random
from numpy import linspace 

def make_init_file(start_lon,start_lat,npts,position_init_file):
    npts=100
    xyz=zeros((npts,3))
    xyz[:,0]= [random.uniform(start_lon-0.5,start_lon+0.5) for _ in xrange(npts)] # x index 100 points
    xyz[:,1]= [random.uniform(start_lat-0.5,start_lat+0.5) for _ in xrange(npts)] # y index 100 points
    xyz[:,2]=23 # at k=20 level, z level will be overwritten if the target_density in the namelist is larger than 0.
    xyz.T.astype('>f8').tofile('particle_init.bin') #the saving sequence should be x[:], y[:], z[:], not [x1,y1,z1],[x2,y2,z2]...
