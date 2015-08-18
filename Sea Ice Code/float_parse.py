import glob
import pandas as pd
from dateutil import parser
def f_parse(float_name,date_inp): 
	df = pd.read_csv(float_name,sep='\t',skiprows=16,error_bad_lines=False,warn_bad_lines=False,usecols = [3,5,6])
	col = list(df.columns)
	col[0] = 'Date'
	col[1] = 'Lon'
	col[2] = 'Lat'
	df.columns = col
	df.Date = pd.to_datetime(df['Date'])
	df = df.drop_duplicates(subset='Date')
	return df