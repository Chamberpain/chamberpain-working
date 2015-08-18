#!/usr/bin/env python
# encoding: utf-8

""" 
plot_proj.py

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-= Desccription =-
Plot a field on a orthogonal projection
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-= Issues =-
*  Hopefully none..
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Contributors: isaB. 
"""
 
# -------------------------
# -- Module dependencies --

import os
import sys

import numpy as np
import matplotlib as matp
import h5py as hdf

import matplotlib.colors as col
import matplotlib.pyplot as plt

from time import clock
from mpl_toolkits.basemap import Basemap


# ~~~~ directories, files, fields.. stuff ~~~~ #

pltdir   = 'plots_dir_path'
griddir  = 'grid_file_dir_path'

# -- plotting format --
params = {
      'axes.labelsize': 12,
      'legend.fontsize': 14,
      'xtick.labelsize': 10,
      'ytick.labelsize': 10,
      'lines.linewidth': 2
      }

plt.rcParams.update(params)

# ~~~ plots stuff ~~~ #
c_min    = 0.
c_max    = .5
bb_lab   = 'm/s'
map_plot = 'BuPu'

#~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~#
def main():
    global ffvec, datadir
    datadir = 'run_dir_path'
    print datadir
    print "Now doing %s ... " % (datadir)

~~~~~~~~~~~ LOAD COORD FROM MODEL GRID ~~~~~~~~~~~~~~#
def read_grid():
    grid_file    = os.path.join(griddir, 'grid.mat')
    grid         = hdf.File(grid_file,'r')
    read_grid.XC = grid['XC'][:] 
    read_grid.YC = grid['YC'][:]
    read_grid.RC = grid['RC'][:]

#~~~~~~~~~~~~~~~~~ PLOT THE FIELD~~~~~~~~~~~~~~~~~~~~#
def plot_ff(ffvec,outfile):
    # load grid
    read_grid()
    XC         = read_grid.XC
    YC         = read_grid.YC
    len_x      = len(XC[0,:])
    len_y      = len(YC[:,0])
    
    # mask bathy values of ffvec
    ffmsk      = np.ma.masked_equal(ffvec,0.)
    
    # let's make a nice plot!
    fig1       = plt.figure(1,figsize=(8,8))

    # coords for the projection
    latcorners = YC[:,0]
    loncorners = XC[0,:]
    
    # center the projection at the south pole
    lon_0      = XC[0,0] 
    lat_0      = YC[0,0]
    
    # contourf levels
    levels     = np.linspace(c_min, c_max, 60)
    # create figure and axes instances
    #ax         = fig1.add_axes([0.1,0.1,0.8,0.8])
    m          = Basemap(projection='ortho', lat_0=-90, lon_0=lon_0)
    lons, lats = loncorners, latcorners
    x, y       = m(*np.meshgrid(lons, lats))
    m.contourf(x, y, ffmsk,  cmap=map_plot, levels=levels, extend='max')
    
    # m.contour(x, y, bathy, 1,linewidhth=2,colors='k')
    m.drawcoastlines()
    m.drawparallels(np.arange(-80, 90, 20))
    m.drawmeridians(np.arange(0, 360, 20))
    m.fillcontinents(color='gray',lake_color='gray') 
    m.drawmapboundary(fill_color='gray')

    cbar    = plt.colorbar(shrink=0.5)
    cbar.set_ticks((np.linspace(c_min,c_max,5)))
    cbar.ax.set_xlabel(bb_lab, rotation='horizontal',fontsize=12)
    plt.clim(c_min, c_max)
    
    # if we wanna add some bathymetry contours (first, load bathy!!)..
    #plt.contour(bathy, v, extent=ax_ext, aspect=1, origin='lower', colors='black', linewidth=0.1)
    # ..or plot a box..
    #plt.plot([114., 114., 129., 129., 114.], [53., 43., 43., 53., 53.], 'y--', linewidth=3)
    
    # ..or Orsi's fronts (NB: it's a bit messy, coz my file is not trivial, as some points are missing..)
    frontdir    = 'fronts_dir'
    fronts      = ['pf', 'saf', 'saccf']#,  'stf', 'sbdy']
    col_FF      = ['black', 'black', 'black', 'black', 'black']
    i = 0
    for ff in fronts:
        lon_FF = []
        lat_FF = []

        dataFile = os.path.join(frontdir, 'fronts_file.txt')
        data = open(dataFile, 'r')

        for line in data.readlines():
            if not line.strip().startswith('%'):
		    coord  = line.split()
		    lon_FF = np.append(lon_FF, float(coord[0]))
		    lat_FF = np.append(lat_FF, float(coord[1]))
	    else:
		    if len(lon_FF)!= 0:
			    xL, yL = map(lon_FF,lat_FF)
			    map.plot(xL, yL, '-',color='blue',linewidth=2)
			    lon_FF = []
			    lat_FF = []
			    
        data.close()
        i += 1

    
    plt.title('pretty pretty plot', fontsize=16)
    
    # ~~~~~~~~~ save figure ~~~~~~~~~ #
    print outfile
    plt.savefig(outfile, bbox_inches='tight', dpi=500)
    #plt.show()
    plt.close(1)
    
    
  ~~~~~~~~~~~~ RUN THE SCRIPT ~~~~~~~~~~~~~~#
if __name__ == "__main__":
    for fold in exp:
        # run the script
        main()
