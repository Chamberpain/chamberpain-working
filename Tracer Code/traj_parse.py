import os
import sys
import glob
from numpy import *
import datetime
from subprocess import call

sys.path.append(os.path.abspath("../scripts"))
# from make_plot import * 
from lat_lon_parser import * 
from parti_init import * 
from net_cdf_reader import *
from make_config import * 
from file_match import * 
from timecalculator import *
from glue_opt_data import *
############# init ###########
npts = 100
position_init_file = 'particle_init.bin'


##############################

file_names = glob.glob('../data/SOCCOM_trajectory/*.txt')
for name in file_names[6:]:
	seq_list = sequential(name)
	try:
		for i,seq_name in enumerate(seq_list):
			tstart,xstart,ystart,tend,xend,yend = parse_latlon(name,seq_name)
			tstart = str(tstart)
			print 'tstart = ',tstart
			tend = str(tend)
			print 'tend = ',tend
			runtime = timecalculator(tstart,tend) 
			print 'runtime = ',runtime
			a = name.split('/')

			for k in range(60):
				b = a[-1]
				b = b[:-4]+'_'+str(i)+'_month_'+str(k)
				print b
				starttime = k*86400*30
				make_init_file(xstart*6,(ystart+77.875)*6,npts,position_init_file)
				make_config(starttime,runtime,position_init_file,npts,b)
				os.system("make")
				os.system("./opt.ensemble < NML.TEST_0000")
				try:
					glue(b,npts)
					make_plot(b,npts,xstart,ystart,xend,yend,runtime,k)
				except ValueError: 
					continue
	except TypeError:
		continue