from numpy import array
from itertools import groupby
from operator import itemgetter

def sequential(name):
	data_int, interp_list = parse_file(name)
	mark = 0
	index_num = 0
	seq_list=[]
	for k, g in groupby(enumerate(interp_list), lambda (i,x):i-x):
		seq_list.append(map(itemgetter(1), g))
	return seq_list

def parse_file(name):
	temp = open(name,'r')
	data = temp.readlines()
	rows = [line.strip().split() for line in str(data).split('\\n')]
	rows = rows[4:-1]
	ar = array(rows)
	col_index = [2,3,4,6,7,8]
	data = ar[:,col_index]
        data_int = []
	for row in data: 
		row = map(float,row)
		data_int.append(row)
	data_int = array(data_int)
	data_int,interp_list = ice_parser(data_int)

	return data_int, interp_list


def ice_parser(data_int):
	try:
		interp_list = data_int[data_int[:,5] == 8,1]
		return data_int, interp_list
	except IndexError:
		print 'No under sea ice interpolation detected'

def float_parse(data_int):
	try: 
		interp_list = [data_int[4*x+2:4*(x+1)] for x in range(int(round(len(a)/4)))]
		return data_int,interp_list
	except IndexError:
		print 'The parser to seperate float data is broken'	

def parse_latlon(name, seq_list):
	data_int, interp_list=parse_file(name)
	# print data_int
	a = list(data_int[:,1])
	b = a.index(seq_list[-1])
	c = a.index(seq_list[0])
	tstart,ystart,xstart = data_int[c-1,[2,3,4]]
	tend,yend,xend = data_int[b+1,[2,3,4]]
	# print 'Index begining at ', int(seq_list[0])-3
	print xstart, ystart
	print xend, yend
	return tstart,xstart,ystart,tend,xend,yend