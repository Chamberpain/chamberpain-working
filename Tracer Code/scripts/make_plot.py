from numpy import fromfile
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from pylab import get_cmap

def shoot(lon, lat, azimuth, maxdist=None):
    """Shooter Function
    Original javascript on http://williams.best.vwh.net/gccalc.htm
    Translated to python by Thomas Lecocq
    """
    glat1 = lat * np.pi / 180.
    glon1 = lon * np.pi / 180.
    s = maxdist / 1.852
    faz = azimuth * np.pi / 180.
 
    EPS= 0.00000000005
    if ((np.abs(np.cos(glat1))<EPS) and not (np.abs(np.sin(faz))<EPS)):
        alert("Only N-S courses are meaningful, starting at a pole!")
 
    a=6378.13/1.852
    f=1/298.257223563
    r = 1 - f
    tu = r * np.tan(glat1)
    sf = np.sin(faz)
    cf = np.cos(faz)
    if (cf==0):
        b=0.
    else:
        b=2. * np.arctan2 (tu, cf)
 
    cu = 1. / np.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1. + np.sqrt(1. + c2a * (1. / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1. - x
    c = (x * x / 4. + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1
    while (np.abs (y - c) > EPS):
 
        sy = np.sin(y)
        cy = np.cos(y)
        cz = np.cos(b + y)
        e = 2. * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4. - 3.) * y * cz * d / 6. + x) *
              d / 4. - cz) * sy * d + tu
 
    b = cu * cy * cf - su * sy
    c = r * np.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = (np.arctan2(d, c) + np.pi) % (2*np.pi) - np.pi
    c = cu * cy - su * sy * cf
    x = np.arctan2(sy * sf, c)
    c = ((-3. * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = ((glon1 + x - (1. - c) * d * f + np.pi) % (2*np.pi)) - np.pi    
 
    baz = (np.arctan2(sa, b) + np.pi) % (2 * np.pi)
 
    glon2 *= 180./np.pi
    glat2 *= 180./np.pi
    baz *= 180./np.pi
 
    return (glon2, glat2, baz)

def equi(m, centerlon, centerlat, radius, *args, **kwargs):
    glon1 = centerlon
    glat1 = centerlat
    X = []
    Y = []
    for azimuth in range(0, 360):
        glon2, glat2, baz = shoot(glon1, glat1, azimuth, radius)
        X.append(glon2)
        Y.append(glat2)
    X.append(X[0])
    Y.append(Y[0])
 
    #m.plot(X,Y,**kwargs) #Should work, but doesn't...
    X,Y = m(X,Y)
    plt.plot(X,Y,**kwargs)

def make_plot(b,file_pointer,npts,xstart,ystart,xend,yend,runtime,k):
	fig = plt.figure()
	opt=fromfile(file_pointer,'>f4').reshape(-1,3,npts)
	x,y=opt[:,0,:],opt[:,1,:] #this is in model grid index coordinate, convert to lat-lon using x=x/6.0;y=y/6.0-77.875
	x=x/6.0;y=y/6.0-77.875
	rows,cols =  np.shape(y)
	lllat=min([y.min(),ystart,yend])-0.25
	urlat=max([y.max(),ystart,yend])+0.25
	lllon=min([xstart,xend,x.min()])-0.25
	urlon=max([x.max(),xstart,xend])+0.25
	m = Basemap(projection='cyl',llcrnrlat=lllat,urcrnrlat=urlat,llcrnrlon=lllon,urcrnrlon=urlon,resolution='c')
#	m.fillcontinents(color='coral',lake_color='aqua')
#	m.drawmapboundary(fill_color='aqua')
	m.drawcoastlines(linewidth=0.25)
	cm = get_cmap('gist_rainbow')
	for i in range(rows):
		color = cm(1.*i/rows)
		xtrans,ytrans = m(x[i,:],y[i,:])
		m.plot(xtrans,ytrans,color = color,marker = 'o',markersize = 2, linewidth=0)
	x2, y2 = (-90, 10)
	xpos,ypos = m(xstart,ystart)
	m.plot(xpos,ypos,'k*',markersize = 10)
	plt.annotate('Day = 0', xy=(xpos, ypos),  xycoords='data',
                xytext=(x2, y2), textcoords='offset points',
                color='r',
                arrowprops=dict(arrowstyle="fancy", color='g'))
	xpos,ypos = m(xend,yend)
	m.plot(xpos,ypos,'k*',markersize = 10)
	plt.annotate('Day = '+str(int(runtime/86400)), xy=(xpos, ypos),  xycoords='data',
            xytext=(x2, y2), textcoords='offset points',
            color='r',
            arrowprops=dict(arrowstyle="fancy", color='g'))
	plt.title('Total runtime is '+str(runtime)+' Seconds for Float '+b)
	parallels = np.arange(-90,0,1.)
	m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
	meridians = np.arange(0,360.,1.)
	m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
	# f= 2 * 7.2921 * 10**(-5)*2*np.pi*abs(np.sin(ystart))
	# print f
	# l_r = np.sqrt(9.8*4000)/f
	# print l_r
	# equi(m, xstart, ystart, l_r,lw=2.)
	#Need to calculate the first baroclinic rossby radius.
	plt.savefig('../Plots/'+b+'.png')
	plt.close(fig)