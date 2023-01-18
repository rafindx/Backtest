import calculation.Functions_db as f
import pyodbc 
import calculation.Functions_Calculate as f_c
from itertools import chain
import datetime
import csv 
import pandas as pd

class Calculation:

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=65.0.33.214;DATABASE=FDS_Datafeeds;UID=sa;PWD=Indxx@1234',connect_timeout=1200000)
        #self.conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=65.0.33.214;DATABASE=FDS_Datafeeds;UID=Crypto_user;PWD=Crypto@user', connect_timeout=1200000)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        
    def __exit__(self, *args):
        if self.conn:
            #self.cursor.commit()
            self.cursor.close()
            self.conn.close()
            self.conn = None            
            
    def Load_CSV(self,file_Name,tax_file_Name):
        try:        
            d1 = {}
            d2 = {}
            D_Data= {}
            D_Date = {}
            D_ISIN = {}
            D_ISIN_RIC = {}
            quote_data = {}
            ISIN_LIST = []
            last_Period = 1
            First_Period = 1
            errorMessage = ""
            warningMessage = ""
            MISSING_RIC_ISIN_LIST = []
            i = 0
            data = pd.read_excel(file_Name, header=None)   
            a = data.values.tolist()
            # print('data:::::::',data)
            # print('a::::::',a)
            for line in a:
                if i!=0 :
                    last_Period = line[0]
                    #print('Start')
                    #print('allllllllllllllllllll:',line,'d1:',d1, 'd2:',d2,'D_Data:',D_Data,'D_Date:',D_Date,'D_ISIN:',D_ISIN,'ISIN_LIST:',ISIN_LIST)
                    f.Load_Data(line,d1,d2,D_Data,D_Date,D_ISIN,ISIN_LIST)
                    #print('End')
                i += 1
            
            yesterday = datetime.datetime.now()- datetime.timedelta(days=1)
            Last_Period_End_Date = D_Date[str(last_Period)+'_END']
            print('Last_Period_End_Date',Last_Period_End_Date)
            if yesterday.weekday()==5:
                    yesterday = yesterday - datetime.timedelta(days=1)
            elif yesterday.weekday()==6:
                    yesterday = yesterday - datetime.timedelta(days=2)
            #print('TR Check')
            #print(yesterday.date())
            #print(Last_Period_End_Date.date())
            '''if yesterday.date() == Last_Period_End_Date.date():
                #print('TR Check')
                for line in D_Data[last_Period]:
                    D_ISIN_RIC[line[1]]=line[6]
                if D_ISIN_RIC:
                    validate_ric = f.Check_Ric(D_ISIN_RIC)
                    quote_data = validate_ric['isin_quote_data']'''
            if yesterday.date() == Last_Period_End_Date.date():
                #print('TR Check')
                for line in D_Data[last_Period]:
                    data = pd.Series(line)
                    if data.isnull().any():
                        if line[1] not in MISSING_RIC_ISIN_LIST: 
                            MISSING_RIC_ISIN_LIST.append(line[1])
                    else:                        
                        D_ISIN_RIC[line[1]]=line[6]
            Period = {}
            Period["Last"] = last_Period
            Period["First"] = First_Period
            Tax_Rate = f.Read_Tax(tax_file_Name)
            #print(quote_data)
            final_data = {'error': errorMessage, 'warning': warningMessage, 'D_Data':D_Data, 'D_Date': D_Date, 'D_ISIN':D_ISIN, 'Period':Period, 'D_ISIN_RIC':D_ISIN_RIC, 'quote_data': quote_data,'ISIN_LIST':ISIN_LIST,'Tax_Rate':Tax_Rate}              
            final_data["MISSING_RIC_ISIN_LIST"] = MISSING_RIC_ISIN_LIST
            #print('MISSING_RIC_ISIN_LIST---------',MISSING_RIC_ISIN_LIST)
            return final_data
        except Exception as e:
            print(e)
            return e
    
    def Validate_Read_CSV(self,file_Name,IDentifier,tax_file_Name):       
        data = pd.read_excel(file_Name, header=None)   
        a = data.values.tolist()
        d1 = {}
        d2 = {}
        D_Data= {}
        D_Date = {}
        D_ISIN = {}
        D_ISIN_RIC = {}
        quote_data = {}
        ISIN_LIST = []
        MISSING_RIC_ISIN_LIST = []
        last_Period = 1
        First_Period = 1
        errorMessage = ""
        warningMessage = ""
        i=0
        try:
            for line in a:
                #print(line[2],i)
               
                if i==0 :
                    if int(f.Validate_Columns_Order(line)):
                        
                        errorMessage = "Please check your portfolio.Columns should be in order (Period, ISIN, Weights, Start date, End date, Country, RIC)."
                        response = {'error': errorMessage, 'warning': ''}
                        return response                     
                else:
                    S_Date = line[3]
                    E_Date = line[4]
                    #print('S_Date.weekday',S_Date.weekday())
                    if S_Date.weekday()==5:
                        S_Date = S_Date - datetime.timedelta(days=1)

                    elif S_Date.weekday()==6:
                        S_Date = S_Date - datetime.timedelta(days=2)

                    if E_Date.weekday()==5:
                        E_Date = E_Date - datetime.timedelta(days=1)

                    elif E_Date.weekday()==6:
                        E_Date = E_Date - datetime.timedelta(days=2)
                    line[3] = S_Date
                    line[4] = E_Date
                    errorMessage = f.Validate_Data(line,D_Date,last_Period)
                    if errorMessage not in (None, ""):
                        return {'error': errorMessage}                        
                    else:
                        #print('loaddata')
                        last_Period = line[0]                        
                        f.Load_Data(line,d1,d2,D_Data,D_Date,D_ISIN,ISIN_LIST)
                i += 1

            '''Check for Total sum of weights'''                      
            for key in d1:
                #print('d1........',d1[key])
                if d1[key]>1.0044 or d1[key]<.9950:
                    errorMessage += "Total weight of period " + str(key) +" is " + str(d1[key])+"."
            '''Check for Delisted Securities'''           
            for key in D_ISIN:
                isins=D_ISIN[key]
                startDate = D_Date[str(key)+'_START']
                #print(startDate)
                delistedISINs = f.Delisting_Check(self.cursor,isins,startDate,IDentifier)
                if delistedISINs not in (None, ""):
                    errorMessage += "Securities " + delistedISINs +" of period - "+str(key)+" is not trading start at the start of the period . "
                    #print(errorMessage)
            '''Check for Warning '''
            for key in d2:
                 if d2[key]>.45:
                     warningMessage +="Sum of weights of securities for period " + str(key) +" with greater than 5% weight is  " + str(d2[key])+"."
                     #print(warningMessage)
            yesterday = datetime.datetime.now()- datetime.timedelta(days=1)
            Last_Period_End_Date = D_Date[str(last_Period)+'_END']
            if yesterday.weekday()==5:
                    yesterday = yesterday - datetime.timedelta(days=1)
            elif yesterday.weekday()==6:
                    yesterday = yesterday - datetime.timedelta(days=2)
            #print('TR Check')
            #print(yesterday.date())
            #print(Last_Period_End_Date.date())
            if yesterday.date() == Last_Period_End_Date.date():
                #print('TR Check')
                for line in D_Data[last_Period]:
                    data = pd.Series(line)
                    #print(data.isnull().any())
                    #print(line1)
                    #print(data)
                    if data.isnull().any():
                        #print(line)
                        if line[1] not in MISSING_RIC_ISIN_LIST: 
                            MISSING_RIC_ISIN_LIST.append(line[1])
                        #errorMessage = "Please check your portfolio.Few Securities in last period does not have proper RIC."
                        #return {'error': errorMessage}                       
                    else:                        
                        D_ISIN_RIC[line[1]]=line[6]
                '''if D_ISIN_RIC:
                    validate_ric = f.Check_Ric(D_ISIN_RIC)
                    #print(validate_ric)
                    if validate_ric['status']== False:
                        errorMessage += validate_ric['message']
                    else:                    
                        quote_data = validate_ric['isin_quote_data']'''
                print('MISING RIC')
                print(MISSING_RIC_ISIN_LIST)
            if errorMessage not in (None, ""):
                errorMessage = "Please check your portfolio."+errorMessage
            Period = {}
            Period["Last"] = last_Period
            Period["First"] = First_Period
            Tax_Rate = f.Read_Tax(tax_file_Name)
            #print(quote_data)
            final_data = {'error': errorMessage, 'warning': warningMessage, 'D_Data':D_Data, 'D_Date': D_Date, 'D_ISIN':D_ISIN, 'Period':Period, 'D_ISIN_RIC':D_ISIN_RIC, 'quote_data': quote_data,'ISIN_LIST':ISIN_LIST,'Tax_Rate':Tax_Rate}              
            final_data["MISSING_RIC_ISIN_LIST"] = MISSING_RIC_ISIN_LIST
            #print('MISSING_RIC_ISIN_LIST-----------------------------------2',MISSING_RIC_ISIN_LIST)
            # print('final_data*****************', final_data)
            return final_data
        except ValueError:
            errorMessage = "Oops!  That was no valid number.  Try again..."
            final_data = {'error': errorMessage, 'warning': warningMessage}
            return final_data

    def Cal_Index(self,D_Index,csv_data):#D_Data,D_ISIN,D_Date,quote_data,Period,ISIN_LIST,Tax_Rate):
        try:
            warningMessage = ''
            D_Data = csv_data['D_Data']
            D_ISIN = csv_data['D_ISIN']
            D_Date = csv_data['D_Date']
            #Quote_Data = csv_data['quote_data']
            Period = csv_data['Period']
            ISIN_LIST = csv_data['ISIN_LIST']
            Tax_Rate = csv_data["Tax_Rate"]
            MISSING_RIC_ISIN_LIST = csv_data["MISSING_RIC_ISIN_LIST"]
            D_ISIN_RIC = csv_data["D_ISIN_RIC"]
            #print(D_Data)
            Index_List = list()
            Constituents_List = list()
            Index_List.append(["SNo","Date","Index Value PR","Index Value TR","Index Value NTR"])
            #Constituents_List.append(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
            
            First_Period = Period["First"]
            last_Period = Period["Last"]
            #print('Cal Starts'+str(datetime.datetime.now()))
            
            D_Index["M_Cap_PR"],D_Index["M_Cap_TR"],D_Index["M_Cap_NTR"]=D_Index["MV"],D_Index["MV"],D_Index["MV"]
            D_Index["Index_Value_PR"], D_Index["Index_Value_TR"],D_Index["Index_Value_NTR"]= D_Index["IV"],D_Index["IV"],D_Index["IV"]
            Divisor = D_Index["MV"]/D_Index["IV"]
            D_Index["Divisor_PR"], D_Index["Divisor_TR"],D_Index["Divisor_NTR"]=Divisor,Divisor,Divisor
            j=0
            #for period in D_Data:
            #Tax_Rate = D_Data["Tax_Rate"]#f.Get_TAX()
            Index_Currency = D_Index["Currency"]
            #format_str = '%m-%d-%Y'
            S_Date = D_Date[str(First_Period)+"_START"]
            E_Date = D_Date[str(last_Period)+"_END"]

            if S_Date.weekday()==5:
                S_Date = S_Date - datetime.timedelta(days=1)
               
            elif S_Date.weekday()==6:
                S_Date = S_Date - datetime.timedelta(days=2)
                
                    
            S_Date_Minus_Five = S_Date - datetime.timedelta(days=5)        
            
            #print(S_Date)
            #print(E_Date)
            print('Get Data Starts'+str(datetime.datetime.now()))
            D_Price,D_LastDate,currency_list,D_ISIN_Currency = f.Get_PRICE(self.cursor,ISIN_LIST,S_Date_Minus_Five,E_Date,D_Index["Identifier"])
            currency_list.append(Index_Currency)
            Ex_Rate = f.Get_Currency(self.cursor,currency_list,S_Date_Minus_Five,E_Date)
            D_CA = f.Get_CA(self.cursor,ISIN_LIST,S_Date,E_Date,D_Index["Identifier"])
            print('Get Data Ends'+str(datetime.datetime.now()))
            #print(D_Price)

            for period in D_Data:            
                S_Date = D_Date[str(period)+"_START"]            
                if S_Date.weekday()==5:
                    S_Date = S_Date - datetime.timedelta(days=1)

                elif S_Date.weekday()==6:
                    S_Date = S_Date - datetime.timedelta(days=2)
                  
                S_Date_Minus_Five = S_Date - datetime.timedelta(days=5)
                E_Date = D_Date[str(period)+"_END"]
                
                i=0
                #if period ==last_Period:
                    #print('TR  Data Starts'+str(datetime.datetime.now()))
                    #f.Set_TR_Price(D_Date,quote_data,last_Period,D_Price)
                    #print('TR  Data Ends'+str(datetime.datetime.now()))
                Latest_Price={}
                Latest_Ex_Rate={}
                #print(S_Date_Minus_Five)
                #print(E_Date)
                while S_Date_Minus_Five <= E_Date:
                    if S_Date_Minus_Five ==E_Date:
                        print('LAST DAY')
                        yesterday = datetime.datetime.now()- datetime.timedelta(days=1)
                        Last_Period_End_Date = D_Date[str(last_Period)+'_END']
                        if yesterday.weekday()==5:
                            yesterday = yesterday - datetime.timedelta(days=1)
                        elif yesterday.weekday()==6:
                            yesterday = yesterday - datetime.timedelta(days=2)
                        if yesterday.date() == Last_Period_End_Date.date():
                            if MISSING_RIC_ISIN_LIST:
                                str1 = "" 
                                for ele in MISSING_RIC_ISIN_LIST: 
                                    str1 += ele +","
                                warningMessage = "Ric was missing for ISIN: ("+str1+")."
                            if D_ISIN_RIC :
                                validate_ric = f.Check_Ric(D_ISIN_RIC)                        
                                if validate_ric["INValidRICS"] not in (None, ""):
                                    warningMessage += ' We found some invalid RIC as well('+validate_ric["INValidRICS"]+'). Please verify last day price at you end.'
                                print(warningMessage)
                                print(validate_ric["INValidRICS"])
                                quote_data = validate_ric['isin_quote_data']
                                #print('got to Functions_db for Set_TR_Price')
                                f.Set_TR_Price(D_Date,quote_data,last_Period,D_Price)

                    #print('inside')
                    #print('All Calculation start from Calcute.py to Functions_Calculate ')
                    f_c.Set_Latest_Ex_Rate(Index_Currency,D_Data[period],Ex_Rate,Latest_Ex_Rate,S_Date_Minus_Five,D_ISIN_Currency)
                    f_c.Set_Latest_Price(D_Data[period],D_Price,Latest_Price,S_Date_Minus_Five)
                    #print('D_Data[period]::::::::::::',D_Data[period])
                    # print(Latest_Price)
                    # print(Latest_Ex_Rate)
                    if S_Date_Minus_Five>=S_Date:
                        print_flag = f_c.GetFlag(D_Index["DCFO"],S_Date_Minus_Five,E_Date)
                        if i==0:
                            #print(S_Date_Minus_Five)
                            f_c.Cal_Shares(D_Index,D_Data[period],Latest_Price,Latest_Ex_Rate,S_Date_Minus_Five,Constituents_List,period,Tax_Rate,D_ISIN_Currency,print_flag,j)
                        else:
                            M_Cap = f_c.Cal_Index_Close(D_Index,D_Data[period],Latest_Price,Latest_Ex_Rate,S_Date_Minus_Five,Constituents_List,period,Tax_Rate,D_ISIN_Currency,print_flag)
                        if (i==0 and j==0) or (i!=0 and j != 0):
                            f_c.Fill_Index_Report_Data(D_Index,Index_List,period,S_Date_Minus_Five)
                        i += 1
                        j += 1                 
                    '''if S_Date_Minus_Five.weekday()==4:
                        S_Date_Minus_Five = S_Date_Minus_Five + datetime.timedelta(days=3)
                    else:'''
                    S_Date_Minus_Five = S_Date_Minus_Five + datetime.timedelta(days=1)
                    #print(S_Date_Minus_Five)
                    if S_Date_Minus_Five>S_Date and i!=0 and S_Date_Minus_Five <= E_Date:
                        #print('NextDate')
                        #print(S_Date_Minus_Five)
                        f_c.Delist(D_Data[period],S_Date_Minus_Five,D_LastDate,E_Date,MISSING_RIC_ISIN_LIST,D_ISIN_RIC)
                        #print('Execute Cal_Index_Open Function from Calcute to Functions_Calculate ')
                        f_c.Cal_Index_Open(D_Index,D_Data[period],Latest_Price,Latest_Ex_Rate,S_Date_Minus_Five,Tax_Rate,D_ISIN_Currency,Ex_Rate,D_CA)
                
            print('Cal_Index Ends'+str(datetime.datetime.now()))
            files = f_c.Print_XLSX_Reports(Index_List,Constituents_List)
            files["warningMessage"] = warningMessage
            #files = f_c.Print_Reports(Index_List,Constituents_List)
            return files
        except Exception as e:
            print(e)
            return e