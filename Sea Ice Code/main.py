from dateutil.relativedelta import *
import datetime
from ice_plot import ice_map
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import mpl_toolkits.basemap.pyproj as pyproj
import numpy as np
import sys
import shapefile
from osgeo import osr
import os
import glob
import pandas as pd


#####  Inputs
start_date  = datetime.date(2012,6,24)
end_date = datetime.date(2015,6,26)
time_advance = datetime.timedelta(days=10)
#####

def f_parse(float_name): 
	df = pd.read_csv(float_name,sep='\t',skiprows=16,error_bad_lines=False,warn_bad_lines=False,usecols = [0,3,5,6])
    col = list(df.columns)
    col[0] = 'Cruise'
    col[1] = 'Date'
    col[2] = 'Lon'
    col[3] = 'Lat'
    df.columns = col
	df.Date = pd.to_datetime(df['Date'])
	df_new = df.drop_duplicates(subset='Date')
	return df_new

def gather_float_data(): 
	file_names = glob.glob('/Users/paulchamberlain/Data/SOCCOM/LOW_RES_DRIFTER/*.TXT')
	df = pd.DataFrame(columns=['Cruise','Date','Lon','Lat'])
	for float_name in file_names:
	    df_new = f_parse(float_name)
	    df = pd.concat([df,df_new])
	return df

def inside_ice(lon,lat):
        xpt,ypt = m(lon,lat)
        lon,lat = m(xpt,ypt,inverse = True)
        di_new = di[(di.Lon>[lon-2]) & (di.Lon<[lon+2])]['Lat'].values
	for n in di_new:
	    if n > lat:
		return True
        return 
        
def plot_float_data():
    latlon = np.array(df[(df.Date<=display_date)&(df.Date>=start_date)][['Lat','Lon','Cruise']].values)
    xpt,ypt = m(latlon[:,1],latlon[:,0])
    m.plot(xpt,ypt,'ko',markersize = 2)
    return

def place_marker():
    df_new = df[(df.Date<=display_date)&(df.Date>=start_date)]
    df_new = df_new.drop_duplicates(subset='Cruise',take_last=True)	
    latlon = np.array(df_new[['Lat','Lon','Cruise','Date']].values)

    x2, y2 = (-50, 7)
    for n in range(len(latlon)):
        marker_color = 'ro'
    	xend,yend = m(latlon[n,1],latlon[n,0])
    	name = latlon[n,2]
    	if inside_ice(latlon[n,1],latlon[n,0]):
            marker_color = 'yo'
	m.plot(xend,yend,marker_color,markersize = 6)
        plt.annotate(latlon[n,2],xy=(xend,yend),xycoords='data',xytext=(x2, y2),fontsize=6,textcoords='offset points',color='k',arrowprops=dict(arrowstyle="->", color='g'))
    return

def ice_map(m):
    date_code=str(display_date.year)+'%02.0f' % display_date.month
    file_path='/Users/paulchamberlain/Data/SOCCOM/SEA_ICE/NOAAG02135/'+str(display_date.strftime("%B"))+'/shp_extent/extent_S_'+date_code+'_polyline/extent_S_'+date_code+'_polyline'
    prj_file = open(file_path+'.prj', 'r')
    prj_txt = prj_file.read()
    srs = osr.SpatialReference()
    srs.ImportFromESRI([prj_txt])

    shpProj = pyproj.Proj(srs.ExportToProj4())
    mapProj = pyproj.Proj(m.proj4string)
    sf = shapefile.Reader(file_path)
    shapes = sf.shapes()
    di = pd.DataFrame(columns=['Lon','Lat'])
    for n in range(len(shapes)):
        shpX = [px[0] for px in shapes[n].points]
        shpY = [px[1] for px in shapes[n].points]
        lonlat = np.array(shpProj(shpX,shpY,inverse=True)).T
        di_new = pd.DataFrame(lonlat,columns=['Lon','Lat'])
        di = pd.concat([di,di_new])
        ice_data = np.array(mapProj(lonlat[:,0],lonlat[:,1])).T
        m.plot(ice_data[:,0],ice_data[:,1],linewidth=.9,color='m')
    return di
    
def newfig(): 
	plt.figure()
	m = Basemap(projection='spstere',boundinglat=-45,lon_0=180,resolution='l')
	m.fillcontinents(color='coral',lake_color='aqua')
	m.drawmapboundary(fill_color='aqua')
	m.drawcoastlines(linewidth=0.25)
	return m

def checkmonth():
	prev_date = display_date - time_advance
	return prev_date.month != display_date.month

##### Plot Setup ####
display_date = start_date
m = newfig()
df = gather_float_data()

while display_date < end_date:
#	if checkmonth():
	plt.close()
	m = newfig()
	di = ice_map(m)
	place_marker()
	plot_float_data()
	plt.title('Ocean Data on '+str(display_date))
	plt.savefig('../Plots/'+str(display_date)+'.png')
	print display_date
	display_date = display_date + time_advance