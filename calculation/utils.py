import csv
from django.db import connection
import datetime
import pyodbc
import random
import calculation.Functions_db as func_data
import calculation.Calculate as c
from itertools import chain
import glob
import os


#======Database Connections===========================#
#conn1 = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=65.0.33.214;DATABASE=FDS_Datafeeds;UID=sa;PWD=Indxx@1234')
#cur = conn1.cursor()

def Load_CSV(file_Name,tax_file_path):  
    #final_data = cal.Validate_Read_CSV(file_Name,IDentifier)  
    cal = c.Calculation()
    with cal:
        final_data = cal.Load_CSV(file_Name,tax_file_path)       
    return final_data

def Validate_Read_CSV(file_Name, IDentifier, tax_file_path):
    #print('Validate_Read_CSV start')  
    #final_data = cal.Validate_Read_CSV(file_Name,IDentifier)  
    cal = c.Calculation()
    with cal:
        final_data = cal.Validate_Read_CSV(file_Name,IDentifier,tax_file_path) 
        #print('final_data:',final_data)      
    return final_data
    
def Cal_Index(D_Index,csv_data):    
    #files = cal.Cal_Index(D_Index,D_Data,D_ISIN,D_Date,quote_data,last_Period,cur)
    files ={}
    cal = c.Calculation()
    with cal:
        files = cal.Cal_Index(D_Index,csv_data)
    return files


def handle_uploaded_file(file, confirmbox):

    if file:
        #print('file is there')
        #print(file)
        random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        file_name = random_id+'-'+file.name
        if confirmbox == '':     
            with open('./static/backtest-file/input/'+file_name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    print('handle_uploaded_file end')
        return file_name


# def save_input_file(input_file,save_data):
#     print('input_file save hare ')
#     file=input_file
#     random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
#     save_inputfile = random_id+'-'+file.name
#     print('save_file',save_inputfile)
#     if save_data=='yes':
#         with open('./static/backtest-file/input_file_save/'+save_inputfile, 'wb+') as destination:
#             for chunk in input_file.chunks():
#                 destination.write(chunk)
#     return True
def save_input_file(input_file):
    print('input_file save hare ')
    file=input_file
    random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    save_inputfile = random_id+'-'+file.name
    input_file_location = './static/backtest-file/rerun_input_files/'+save_inputfile

    with open('./static/backtest-file/rerun_input_files/'+save_inputfile, 'wb+') as destination:
        for chunk in input_file.chunks():
            destination.write(chunk)
    file_with_location={'save_inputfile':save_inputfile,'input_file_location':input_file_location}
    return file_with_location

def remove_percent_symbole(weight):
    weight = list(weight)
    weight =  weight[:-1]
    weight = ''.join([str(elem) for elem in weight])
    return weight

def Rerun_Dbdata(D_Index, start_date, end_date, Period, get_composition):
    D_Data ={}
    D_ISIN ={}
    D_Date ={}
    data = []
    D_RIC_ISIN = {}
    quote_data = {}
    
    st_date = str(Period["Last"])+"_START"
    en_date = str(Period["Last"])+"_END"
   
    D_Date[st_date] = start_date
    D_Date[en_date] = end_date
    comp_isin =[]
    outer_comp_list =[]
    for data_composition in get_composition:
        comp_data = []
        weights = data_composition.weights
        weights =  float(weights)
        comp_data.append(Period["Last"])
        comp_data.append(data_composition.isin)
        comp_data.append(weights)
        comp_data.append(start_date)
        comp_data.append(end_date)
        comp_data.append(data_composition.country)
        comp_data.append(data_composition.ric)
        outer_comp_list.append(comp_data)
        comp_isin.append(data_composition.isin)
        D_RIC_ISIN[data_composition.ric] = data_composition.isin
        quote_data[data_composition.isin] = data_composition.quote_id
    data.append(outer_comp_list)
    D_Data[str(Period["Last"])] = outer_comp_list
    D_ISIN [str(Period["Last"])] = comp_isin
    #save_file = Cal_Index(D_Index, D_Data, D_ISIN, D_Date, D_RIC_ISIN, period)
    #return save_file
    files ={}
    cal = c.Calculation()
    with cal:
        tax_Rate = func_data.Read_Tax('')
        #print(tax_Rate)
        #files = cal.Cal_Index(D_Index,D_Data,D_ISIN,D_Date,quote_data,Period,comp_isin,tax_Rate)
        csv_data={}
        csv_data['D_Data']=D_Data
        csv_data['D_ISIN']=D_ISIN
        csv_data['D_Date']=D_Date
        csv_data['Period']=Period
        csv_data['ISIN_LIST']=comp_isin
        csv_data["Tax_Rate"]=tax_Rate
        csv_data["MISSING_RIC_ISIN_LIST"]=''
        csv_data["D_ISIN_RIC"]=D_RIC_ISIN

        print('csv_data:',csv_data)
        files = cal.Cal_Index(D_Index,csv_data)

    return files


def Rerun_Dbdata1(D_Index,file_name,end_date):
    taxFileName=''
    csv_data1 = Load_CSV('./static/backtest-file/rerun_input_files/'+str(file_name),taxFileName)
    csv_data=csv_data1

    #print('csv_data in Rerun_Dbdata1:',csv_data)
    #print('csv_data[D_Date]',csv_data['D_Date'])
    a=csv_data['D_Date']
    last_peroid = list(csv_data['D_Date'])[-1]
    #dict = {last_peroid:date}
    dict = {last_peroid:end_date}
    #print('...',dict)
    a.update(dict)
    # print('update_dict',a)
    # print(csv_data['D_Date']['2_END'])
    # print('Updated_csv',csv_data)

    cal = c.Calculation()
    with cal:
        files = cal.Cal_Index(D_Index,csv_data)
    return files



def DateTime(current_time):
    date_time = datetime.datetime.strptime(current_time, "%m-%d-%Y")
    cr_date = date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    return cr_date