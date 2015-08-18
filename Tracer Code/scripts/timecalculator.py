import datetime
def timecalculator(tstart,tend):
#accepts as input 2 text inputs and converts to datetime 
	start = datetime.date(int(tstart[:4]),int(tstart[4:6]),int(tstart[6:8]))
	end = datetime.date(int(tend[:4]),int(tend[4:6]),int(tend[6:8]))
	runtime = end-start
	print runtime.total_seconds()
	return int(runtime.total_seconds())
	# return 86400*5