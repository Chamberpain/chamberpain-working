init_file = 'NML.TEST_0000'
dt = 43200
dump_mult = 4


def make_config(start_time,run_length,position_init_file,npts,b):
#	sose_start = datetime.datetime(2005,01,01)
#	sose_end= datetime.datetime(2010,12,31)
#	end_data_time = start_time-sose_start
#	max_time = sose_end-start_time
	#if max_time.total_seconds() < run_length:
	#	run_length = int(max_time.total_seconds())
	#else:
	#	run_length = run_length+int(end_data_time.total_seconds())
	init_data = ['&PARAM\n', 
	"casename='"+b+"',\n", 
	"path2uvw='../data/',\n", 
	"fn_UVEL='UVEL.0000000100.data',\n", 
	"fn_VVEL='VVEL.0000000100.data',\n", 
	"fn_WVEL='WVEL.0000000100.data',\n", 
	"fn_THETA='THETA.0000000100.data',\n", 
	"fn_SALT='SALT.0000000100.data',\n", 
	"fn_GAMMA='GAMMA.0000000100.data',\n", 
	"fn_PHIHYD='',\n", 
	"fn_parti_init='"+position_init_file+"',\n", 
	'target_density=0,\n', 	#needs to be zero if choosing depth level
	'vel_stationary=.False.,\n', 
	'Npts='+str(npts)+',\n', 	#number of points released
	'dt_reinit=-1,\n', 
	'dt_mld='+str(dt*10)+'.,\n', 
	'dt='+str(dt)+',\n', 	#dt
	#'tstart='+str(int(end_data_time.total_seconds())) +'.,\n', 		#time start
	#'tend='+str(run_length) +'.,\n', 	#time end 
	'tstart='+str(start_time)+'.,\n', 		#time start
	'tend='+str(start_time+run_length)+'.,\n', 	#time end 
	'NPP=1,\n', 				#number of times particles are released
	'dt_case=864000,\n',        #frequency at which particles are released
	'pickup=0.,\n', 
	'dumpFreq='+str(dt*dump_mult)+'.,\n', 
	'diagFreq='+str(10*dt*dump_mult)+'.,\n', 
	'pickupFreq=7776000.,\n', 
	'saveTSG=.TRUE.,\n', 
	'useMLD=.TRUE.,\n', 
	'useKh=.TRUE.,\n', 
	'Khdiff=25.0,\n', 
	'Kvdiff=1e-5,\n', 
	'/\n']
	temp = open(init_file,'w')
	temp.writelines(init_data)
	temp.close()