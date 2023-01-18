import csv
import pandas as pd
import pyodbc
from datetime import datetime
from datetime import datetime, timedelta

def read_csv_columns(file_path):
	columns = []
	connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=65.0.33.214;DATABASE=FDS_Datafeeds;UID=sa;PWD=Indxx@1234',connect_timeout=1200000)
	cursor = connection.cursor()
	dataframe1 = pd.read_excel(file_path)
	for index, row in dataframe1.iterrows():
		period = row['Period'] 
		isin = row['ISIN']
		weights = row['Weights']
		start_date = rem_time(row['Start date'])
		end_date =  rem_time(row['End date'])
		country  =  row['Country']
		Query =  "select * from sec_check('"+isin+"','"+start_date+"','"+end_date+"','"+country+"')"
		cursor.execute(Query)
		for row in cursor:
			if row[0] !=isin:
				message = "Please check ISIN "+isin+" not found"
				return message
			elif row[1] != 1:
				message  = "Please check price for start date "+start_date+" not found for "+isin
				return message
			# elif row[2]!= 1:
			# 	print("Please check end date "+end_date+" not found for "+isin)
			elif row[3]!= 1:
				message = "Please check country "+country+" not found for "+isin
				return message
			else:
				message = "Input file data is successfully validate."
				return message

def rem_time(d):
    s = ''
    s = str(d.year) + '-' + str(d.month) + '-' + str(d.day)
    return s

file_path =  "001078-BAC.xlsx"

read_csv_columns(file_path)


def is_yesterday(date_string):
    given_date = datetime.strptime(date_string, "%Y-%m-%d")
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    if given_date.date() == yesterday:
    	True
    else:
    	False