import datetime
import calculation.Query as Q
import pyodbc as ms
import pandas as pd
import csv 


def Validate_Columns_Order(line):
    line = [str(i) for i in line]
    try:
        if len(line)<7:

            # print('gh')
            return 1
        csvColStr = line[0].replace(' ','')+'_'+line[1].replace(' ','')+'_'+line[2].replace(' ','')+'_'+line[3].replace(' ','')+'_'+line[4].replace(' ','')+'_'+line[5]+'_'+line[6]
        validColStr="Period_ISIN_Weights_Startdate_Enddate_Country_RIC"

        if csvColStr!=validColStr:
            #print(csvColStr)
            #print(validColStr)
            #print('ghasf')
            return 1
        else:
            #print('ghda')
            return 0

    except ValueError:
        errorMessage = "Oops!  That was no valid data.  Try again..."
        final_data = {'error': errorMessage, 'warning': warningMessage}
        return final_data

def Validate_Data(line,D_Date,last_Period):
    #print(D_Date)
    errorMessage = ""
    line1 = line[:5]
    data = pd.Series(line1)
    #print(data)
    try:
        if data.isnull().any():
            errorMessage =  "Please check your portfolio. Few Securities does not have proper period, proper ISIN, proper weight , proper Start Date and End Date or proper country."
        else:
            startDate= line[3]
            endDate  = line[4]
            period = line[0]
            #print(D_Date[str(period)+'_START'])
            #print(startDate)
            #print(D_Date[str(period)+'_END'])
            #print(endDate)
            if (str(period)+'_START' in D_Date and D_Date[str(period)+'_START']!= startDate) or (str(period)+'_END' in D_Date and D_Date[str(period)+'_END']!= endDate):
                errorMessage =  "Please check your$$$$$ portfolio.Start date and End date for all the securities of same perioed should be same."
            if last_Period != period and (str(last_Period)+'_END' in D_Date and D_Date[str(last_Period)+'_END']!= startDate):
                errorMessage =  "Please check your!!!! portfolio.Start date of a period should be equal to end date of previous period."
            #print(errorMessage)
        return errorMessage 
    except ValueError:
        errorMessage = "Oops!  That was no valid data.  Try again..."
        final_data = {'error': errorMessage, 'warning': warningMessage}
        return final_data 

def Delisting_Check(cur, ISIN_LIST, E_DATE, IDentifier):
    try:   
        delistedISINs=""    
        S_DATE = E_DATE - datetime.timedelta(days=5)
        Query= Q.Query_Price(IDentifier, ISIN_LIST, S_DATE, E_DATE)
        cur.execute(Query)
        dir1 = {}
        delistedISINs
        for row in cur:
            dir1[row[0]] = row[2]
        for ISIN in ISIN_LIST:
            if ISIN not in dir1:
                delistedISINs += ISIN +","
        return delistedISINs
    except Exception as e:
        print(e)
        return e 

def Check_Ric(ric_data):
    try:
        ric_list_data = list(ric_data.values())
        #ricList = str(ric_list_data)[1:-1]
        ric_active_data= {}
        connection = ms.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=3.7.99.191;DATABASE=TR_Datafeeds;UID=sa;PWD=Indxx@1234')
        cursor = connection.cursor()
        Query= Q.Query_TR_Equity(ric_list_data)
        cursor.execute(Query)
        ric_active_data ={}
        isin_quote_data ={}
        for row in cursor:
            ric_active_data[row[0]] = row[1]
        cursor.commit()
        cursor.close()
        connection.close()
        #ric_active = getList(ric_active_data)
        inValidRICS =""
        #print('AA_________________________________________AA')
        #print(ric_active_data)
        #print('AA_________________________________________AA')
        for isin in ric_data:
            ric = ric_data[isin]
            if ric not in ric_active_data:
                inValidRICS += ric +","
            else:
                quoteId=ric_active_data[ric]
                isin_quote_data[isin] = quoteId
        
        if inValidRICS not in (None, ""):
            #response = {"status":False, "message":"Please check your csv file you have added invalid RIC '" +inValidRICS+"'"}
            response = {"status":False, "isin_quote_data":isin_quote_data,"INValidRICS":inValidRICS}
        else:
            #response = {"status":True, "isin_quote_data":isin_quote_data}'''
            response = {"status":True, "isin_quote_data":isin_quote_data,"INValidRICS":inValidRICS}
        return response
    except Exception as e:
        print(e)
        return e

def Load_Data(line,d1,d2,D_Data,D_Date,D_ISIN,ISIN_LIST):
    try:
        S_Date = line[3]
        E_Date = line[4]
        print('D_Date:::',D_Date)
        '''if S_Date.weekday()==5:
                S_Date = S_Date - datetime.timedelta(days=1)
        elif S_Date.weekday()==6:
                S_Date = S_Date - datetime.timedelta(days=2)
        if E_Date.weekday()==5:
                E_Date = E_Date - datetime.timedelta(days=1)
        elif E_Date.weekday()==6:
                E_Date = E_Date - datetime.timedelta(days=2)'''
        if line[1] not in ISIN_LIST: 
                ISIN_LIST.append(line[1])
        line[3]=S_Date
        line[4]=E_Date
        period = line[0]
        weight = line[2]
        if str(period)+'_START' not in D_Date:
            #print('D_Date;;;;;;;;;;;',D_Date)
            D_Date[str(period)+'_START'] = S_Date
        if str(period)+'_END' not in D_Date:
            D_Date[str(period)+'_END'] = E_Date
        if period not in D_Data:
            #print('D_Data::',D_Data)
            D_Data[period] = list()
        if len(line) == 6:
            line.append('')
        D_Data[period].append(line)
        if period not in D_ISIN:
            D_ISIN[period] = list()
        D_ISIN[period].append(line[1])
        if period in d1:
            d1[period] += weight
        else:
            d1[period] = weight
        if weight > .05:
            if period in d2:
                d2[period] += weight
            else:
                d2[period] = weight
    except Exception as e:
        print(e)
        return e

def Read_Tax(tax_file_Name):
    try:
        Tax_Rate = {}
        if tax_file_Name in (None, ""):
             Tax_Rate = Get_TAX()
        else:
            with open(tax_file_Name,'r') as csvfile:
                csvreader = csv.reader(csvfile)
                i=0
                for line in csvreader:
                    if i!=0:
                        Tax_Rate[line[0]] = float(line[1].strip()[0:-1])
                    i=i+1
                #print('Tax_Rate',Tax_Rate)
        return Tax_Rate
    except Exception as e:
        print(e)
        return e

    
def Get_TAX():
    try:
        connection = ms.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=15.207.231.163;DATABASE=Backtest;UID=sa;PWD=Indxx@1234')
        taxCur = connection.cursor()
        
        taxCur.execute('SELECT * from tax_rate ')
        dir = {}
        for row in taxCur:
            dir[row[1]] = float(row[2].strip()[0:-1])
        taxCur.commit()
        taxCur.close()
        connection.close()
        return dir
    except Exception as e:
        print(e)
        return e

def Get_CA(cur,ISIN_LIST,S_DATE,E_DATE,IDentifier):
    try:
        D_CA ={}
        D_CA_Dividend = {}
        D_CA_S_Dividend = {}
        D_CA_Spin = {}
        D_CA_Split ={}
        Query= Q.Query_Divident(IDentifier,ISIN_LIST,S_DATE,E_DATE)
        cur.execute(Query)
        '''for row in cur:
            var = row[0] + '_' + Q.DeteToStr(row[5])
            print(var)
            if var not in D_CA_Dividend:
                D_CA_Dividend[var] = list()
                D_CA_Dividend[var].append(row)
            else:
                divco1=row[4]
                print('1.from DB::::::::'+str(divco1))
                calist = D_CA_Dividend[var]
                flag=True
                for array in calist:
                    divcod2=array[4]
                    print(array[4])
                    if divcod2 not in (None,''):
                        print('2.from map::::::'+str(divcod2))
                        if divcod2 == divco1:
                            print('code matched')
                            flag=False
                            #array[1] = row[1]
                        else:
                            print('code not matched')
                if flag:
                    D_CA_Dividend[var].append(row)
                D_CA_Dividend[var] = calist
        print( D_CA_Dividend)
        D_CA["Dividend"] = D_CA_Dividend'''

        for row in cur:
            var = row[0] + '_' + Q.DeteToStr(row[5])
            if var not in D_CA_Dividend:
                D_CA_Dividend[var] = list()
            D_CA_Dividend[var].append(row)
        D_CA["Dividend"] = D_CA_Dividend
        #print('CA::::::::::::::;')
        Query= Q.Query_Spin(IDentifier,ISIN_LIST,S_DATE,E_DATE)
        cur.execute(Query)
        for row in cur:
            var = row[0] + '_' + Q.DeteToStr(row[5])
            if var not in D_CA_Spin:
                D_CA_Spin[var] = list()

            D_CA_Spin[var].append(row)
        D_CA["Spin"] = D_CA_Spin
        
        Query= Q.Query_Split(IDentifier,ISIN_LIST,S_DATE,E_DATE)
        cur.execute(Query)
        for row in cur:
            var = row[0]+'_'+Q.DeteToStr(row[1])
            if var not in D_CA_Split:
                D_CA_Split[var] = list()
            D_CA_Split[var].append(row)
        D_CA["Split"] = D_CA_Split
        
        return D_CA
    except Exception as e:
        print(e)
        return e


def Get_PRICE(cur,ISIN_LIST,S_DATE,E_DATE,IDentifier):
    try:
        Query= Q.Query_Price(IDentifier,ISIN_LIST,S_DATE,E_DATE)
        currency_list = []
        cur.execute(Query)
        D_Price = {}
        D_ISIN_Currency ={}
        D_LastDate = {}    
        for row in cur:
            D_Price[row[0]+'_'+Q.DeteToStr(row[1])] = row[2]
            D_ISIN_Currency[row[0]] = row[3]
            D_LastDate[row[0]] = row[1]
            if row[3] not in currency_list: 
                currency_list.append(row[3])
        return D_Price,D_LastDate,currency_list,D_ISIN_Currency
    except Exception as e:
        print(e)
        return e

def Set_TR_Price(D_Date,D_ISIN_Quote,last_Period,D_Price):
    try:
        today = datetime.datetime.now()    
        if today.weekday()==0:
            yesterday = today -  datetime.timedelta(days=3)
        elif today.weekday()==6:
            yesterday = today -  datetime.timedelta(days=2)
        else:
            yesterday = today -  datetime.timedelta(days=1)
        E_Date = D_Date[str(last_Period)+'_END']
        #print(E_Date)
        if D_ISIN_Quote:
            #print('inside')
            TR_Price = Get_TR_PRICE(list(D_ISIN_Quote.values()),E_Date)
            #print(TR_Price)
            for isin in D_ISIN_Quote:
                quote = D_ISIN_Quote[isin]
                var1 = D_ISIN_Quote[isin]+'_'+Q.DeteToStr(E_Date)
                var2 = isin+'_'+Q.DeteToStr(E_Date)        
                if var1 in TR_Price:            
                    trPrice = TR_Price[var1]
                    if var2 not in D_Price:
                        print('Not There')
                        D_Price[var2] = trPrice
                        print(D_Price[var2])
                    #else:
                        #print('Already There')
                        #print(D_Price[var2])
    except ValueError:
        errorMessage = "Oops!  That was no valid number.  Try again..."
        final_data = {'error': errorMessage, 'warning': warningMessage}
        return final_data

def Get_TR_PRICE(QUOTE_LIST,date):
    try:
        #print(QUOTE_LIST)
        #print(date)
        #LIST = str(QUOTE_LIST)[1:-1]
        #print(LIST)
        #Date = date.strftime("%Y-%m-%d") 
        connection = ms.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=3.7.99.191;DATABASE=TR_Datafeeds;UID=sa;PWD=Indxx@1234')
        cursor = connection.cursor()
        #quoteIds = str(QUOTE_LIST)[1:-1]

        Query= Q.Query_TR_Price(QUOTE_LIST,date)
        cursor.execute(Query)
        D_TR_Price = {}
        for row in cursor:
            D_TR_Price[row[0]+'_'+Q.DeteToStr(row[2])] = row[3]
        cursor.commit()
        cursor.close()
        connection.close()
        
        return D_TR_Price
    except Exception as e:
        print(e)
        return e

def Get_Currency(cur,C_list,sd,ed):
    try:
        clist = str(C_list)[1:-1]
        S_DATE = Q.DeteToStr(sd)
        E_DATE = Q.DeteToStr(ed)
        
        Query="SELECT RTS.iso_currency, RTS.exch_date, RTS.exch_rate_usd, RTS.exch_rate_per_usd FROM FDS_DataFeeds.ref_v2.econ_fx_rates_usd AS RTS WHERE RTS.exch_date between '"+S_DATE+"' and '"+E_DATE+"' and RTS.iso_currency in ("+clist +") ORDER BY RTS.exch_date"
        cur.execute(Query)
        dir = {}
        for row in cur:
            dir[row[0]+'_'+Q.DeteToStr(row[1])] = (row[3])
            dir['USD_'+Q.DeteToStr(row[1])] = 1
        return dir
    except Exception as e:
        print(e)
        return e
