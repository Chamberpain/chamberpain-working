from numpy import *
from pylab import *
import popy

folder='/plumdata2/PLUM_SHARED/NASA/llc/llc_4320/regions/DrakePassage/'

u=memmap(folder+'/U/U_768x919x90.20111116T200000',dtype='>f4',shape=(90,919,768),mode='r')
v=memmap(folder+'/V/V_768x919x90.20111116T200000',dtype='>f4',shape=(90,919,768),mode='r')
w=memmap(folder+'/W/W_768x919x90.20111116T200000',dtype='>f4',shape=(90,919,768),mode='r')

xg=memmap(folder+'/grid/XG_768x919',dtype='>f4',shape=(919,768),mode='r')
yg=memmap(folder+'/grid/YG_768x919',dtype='>f4',shape=(919,768),mode='r')
xc=memmap(folder+'/grid/XC_768x919',dtype='>f4',shape=(919,768),mode='r')
yc=memmap(folder+'/grid/YC_768x919',dtype='>f4',shape=(919,768),mode='r')

dyg=memmap(folder+'/grid/DYG_768x919',dtype='>f4',shape=(919,768),mode='r')
dxg=memmap(folder+'/grid/DXG_768x919',dtype='>f4',shape=(919,768),mode='r')

drf=popy.mds.rdmds('/plumdata2/PLUM_SHARED/NASA/llc/llc_4320/regions/grid/grid_full/DRF')
drc=popy.mds.rdmds('/plumdata2/PLUM_SHARED/NASA/llc/llc_4320/regions/grid/grid_full/DRC')
rac=fromfile(folder+'/grid/RAC_768x919',dtype='>f4').reshape(919,768)

print drf.shape,rac.shape,drc.shape

i=0;j=1;k=4

ux = (u*drf*dyg[newaxis,:,:])#[k,:30,:31]
vy = (v*drf*dxg[newaxis,:,:])#[k,:31,:30]
wz = (w*rac[newaxis,:,:])#[k:k+2,:30,:30]
ux=diff(ux,axis=-1)
vy = diff(vy,axis=0)
wz=diff(wz,axis=0).squeeze()
print ux.sum(),vy.sum(),wz.sum()
print ux.shape,vy.shape,wz.shape
for ix in range(2):
    for jx in range(2):
        for iy in range(2):
            for jy in range(2):
                for iw in range(2):
                    for jw in range(2):
                        print ix,jx,iy,jy,iw,jw, ux[jx,ix]+vy[jy,iy]-wz[jw,iw]