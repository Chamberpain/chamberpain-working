import mpl_toolkits.basemap.pyproj as pyproj
import numpy as np
import sys
import shapefile
from osgeo import osr
from dateutil.relativedelta import *
import datetime


def ice_map(date_inp,m):
    date_code=str(date_inp.year)+'%02.0f' % date_inp.month
    file_path='/Users/paulchamberlain/Data/SOCCOM/SEA_ICE/NOAAG02135/'+str(date_inp.strftime("%B"))+'/shp_extent/extent_S_'+date_code+'_polyline/extent_S_'+date_code+'_polyline'
    prj_file = open(file_path+'.prj', 'r')
    prj_txt = prj_file.read()
    srs = osr.SpatialReference()
    srs.ImportFromESRI([prj_txt])

    shpProj = pyproj.Proj(srs.ExportToProj4())
    mapProj = pyproj.Proj(m.proj4string)
    sf = shapefile.Reader(file_path)
    shapes = sf.shapes()
    shpX = [] 
    shpY = []
    for n in range(len(shapes)):
        shpX = [px[0] for px in shapes[n].points]
        shpY = [px[1] for px in shapes[n].points]
        lonlat = np.array(shpProj(shpX,shpY,inverse=True)).T
        ice_data = np.array(mapProj(lonlat[:,0],lonlat[:,1])).T
        m.plot(ice_data[:,0],ice_data[:,1],linewidth=.9,color='m')
    return m 