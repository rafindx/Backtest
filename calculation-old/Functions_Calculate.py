import csv
from itertools import chain
import random
import datetime
import pandas as pd
import xlsxwriter
from zipfile import ZipFile
import calculation.Query as Q
import os 

def Print_XLSX_Reports(Index_List,Constituents_List):
    try:
        #new_list = [['first', 'second'], ['third', 'four'], [1, 2, 3, 4, 5, 6]]
        random_name = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        outFileName1="./static/backtest-file/output/"+random_name+"_index_value_file.xlsx"
        outFileName2="./static/backtest-file/output/"+random_name+"_constituents_file.xlsx"
        #print(Index_List)
        df = pd.DataFrame(Index_List)
        writer1 = pd.ExcelWriter(outFileName1, engine='xlsxwriter')
        df.to_excel(writer1, sheet_name='index_value', index=False,header = False)
        writer1.save()
        Size_Per_File=1000000
        #Size_Per_File=10000000
        Final_List = []
        dataLength = len(Constituents_List)
        #print(dataLength)
        cfileName=''
        #Constituents_List.append(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
        if dataLength > Size_Per_File:        
            i=1
            while dataLength >Size_Per_File:
                list1 =list()
                tempList =[]
                list1.append(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
                tempList = Constituents_List[:Size_Per_File]
                #print(len(tempList))
                list1.extend(tempList)
                #print(tempList)
                Constituents_List = Constituents_List[Size_Per_File:]
                dataLength = len(Constituents_List)
                #print(dataLength)
                outFileName="./static/backtest-file/output/"+random_name+"_constituents_file_"+str(i)+".xlsx"
                
                df1 = pd.DataFrame(list1)
                writer2 = pd.ExcelWriter(outFileName, engine='xlsxwriter')
                df1.to_excel(writer2, sheet_name='constituents_value', index=False,header = False)
                writer2.save()
                i=i+1
                Final_List.append(outFileName)
                if dataLength <Size_Per_File:
                    list1 =list()
                    list1.append(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
                    #print(len(tempList))
                    list1.extend(Constituents_List)
                    outFileName="./static/backtest-file/output/"+random_name+"_constituents_file_"+str(i)+".xlsx"
                    df1 = pd.DataFrame(list1)
                    writer2 = pd.ExcelWriter(outFileName, engine='xlsxwriter')
                    df1.to_excel(writer2, sheet_name='constituents_value', index=False,header = False)
                    writer2.save()
                    Final_List.append(outFileName)
            
            #print('TotalFile::::::')
            #print(len(Final_List))
            cfileName = "./static/backtest-file/output/"+random_name+"_constituents_zip.zip"
            with ZipFile(cfileName,'w') as zip: 
                # writing each file one by one 
                for file in Final_List: 
                    zip.write(file)
        else:
            list1 =list()
            list1.append(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
            list1.extend(Constituents_List)
            df2 = pd.DataFrame(list1)
            writer2 = pd.ExcelWriter(outFileName2, engine='xlsxwriter')
            df2.to_excel(writer2, sheet_name='constituents_value', index=False,header = False)
            writer2.save()
            cfileName = outFileName2    

        file_names = {'index_value_file':outFileName1,'constituents_file':cfileName}
        print('Print_XLSX_Reports End at Function_Calculate')
        return file_names
    except Exception as e:
        print('indxx-03', e)
        return e


def GetFlag(option,currentDate,endDate):
    try:
        if option =="ND":
            return 0
        elif option =="CD":
            return 1
        elif option =="EDD":
           
            if endDate.weekday()==6:
                endDate = endDate -  datetime.timedelta(days=2)
            elif endDate.weekday()==5:
                endDate = endDate -  datetime.timedelta(days=1)
            if endDate == currentDate:
                return 1
            else :
                return 0
    except Exception as e:
        print('indxx-04', e)
        return e 


def Print_Reports(Index_List,Constituents_List):
    try:
        random_name = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        outFileName1="./static/backtest-file/output/"+random_name+"_index_value_file.csv"
        outFileName2="./static/backtest-file/output/"+random_name+"_constituents_file.csv"
        with open(outFileName1, 'w', newline='') as csvfile:
            writer1 = csv.writer(csvfile)
            writer1.writerow(["S.No","Date","Index Value PR","Index Value TR","Index Value NTR"])
            writer1.writerows(Index_List)
        with open(outFileName2, 'w', newline='') as csvfile:
            writer2 = csv.writer(csvfile)
            writer2.writerow(["S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","Index PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin"])
            writer2.writerows(Constituents_List)
        file_names = {'index_value_file':outFileName1,'constituents_file':outFileName2}
        return file_names
    except Exception as e:
        print('indxx-05', e)
        return e



def Adjust_Dividend(divList,isinRow,Tax_Rate,D_ISIN_Currency,Ex_Rate,date,Latest_Price):
    try:
        isin = isinRow[1]
        country = isinRow[5]
        countryTax = Tax_Rate[country]/100
        toCurrency = D_ISIN_Currency[isin];
        aFactor_PR,aFactor_TR,aFactor_NTR = 1,1,1
        Dividend = ''
        sDividend = ''
        amount_PR=0
        amount_TR=0
        amount_NTR=0
        for row in divList:
            amount = row[1]
            amount_Tax = amount*(1-countryTax) 
            fromCurrency = row[3]
            divCode=row[4]
            exRate = Get_Ex_Rate(fromCurrency,toCurrency,Ex_Rate,date)
            if divCode in ('11','134'):
                sDividend += str(amount) + fromCurrency
                amount_PR  += amount*exRate
            else:
                Dividend += str(amount) + fromCurrency
            
            amount_TR  += amount*exRate
            amount_NTR += amount_Tax*exRate

        aFactor_PR =  (1 - (amount_PR/Latest_Price[isin][0]))
        aFactor_TR =  (1 - (amount_TR/Latest_Price[isin][0]))
        aFactor_NTR = (1 - (amount_NTR/Latest_Price[isin][0]))
        return aFactor_PR,aFactor_TR,aFactor_NTR,Dividend,sDividend
    except Exception as e:
        print('indxx-06', e)
        return e

def Adjust_Spin(divList,isinRow,Tax_Rate,D_ISIN_Currency,Ex_Rate,date,Latest_Price):
    try:
        isin = isinRow[1]
        country = isinRow[5]
        countryTax = Tax_Rate[country]/100
        toCurrency = D_ISIN_Currency[isin];
        aFactor_PR,aFactor_TR,aFactor_NTR = 1,1,1
        Spin = ''
        amount_PR=0
        amount_TR=0
        amount_NTR=0
        for row in divList:
            amount = row[1]
            fromCurrency = row[3]       
            Spin += str(amount) + fromCurrency
            exRate = Get_Ex_Rate(fromCurrency,toCurrency,Ex_Rate,date)
                     
            amount_PR  += amount*exRate
            amount_TR  += amount*exRate
            amount_NTR += amount*exRate

        aFactor_PR  =  aFactor_PR*(1 - (amount_PR/Latest_Price[isin][0]))
        aFactor_TR  =  aFactor_TR*(1 - (amount_TR/Latest_Price[isin][0]))
        aFactor_NTR =  aFactor_NTR*(1 - (amount_NTR/Latest_Price[isin][0]))
        return aFactor_PR,aFactor_TR,aFactor_NTR,Spin
    except Exception as e:
        print('indxx-07', e)
        return e


def Adjust_Split(splitList):
    try:
        sFactor_PR,sFactor_TR,sFactor_NTR = 1,1,1
        for row in splitList:
            sFactor_PR =  1/row[2]
            sFactor_TR =  1/row[2]
            sFactor_NTR =  1/row[2]    
        return sFactor_PR,sFactor_TR,sFactor_NTR,row[2]
    except Exception as e:
        print('indxx-08', e)
        return e        

def Adjust_CA(D_Index,D_CA,isin_Data_Row,date,Tax_Rate,D_ISIN_Currency,Ex_Rate,Latest_Price):
    try:
        dFactorPR,dFactorTR,dFactorNTR,sdFactorPR,sdFactorTR,sdFactorNTR =1,1,1,1,1,1
        spinFactorPR,spinFactorTR,spinFactorNTR,splitFactorPR,splitFactorTR,splitFactorNTR = 1,1,1,1,1,1
        Dividend,sDividend,Spin,Split = 0,0,0,0
        #date = date.strftime("%d-%m-%Y") 
        var = isin_Data_Row[1]+'_'+Q.DeteToStr(date)
        
        dFactorPR,dFactorTR,dFactorNTR = 1,1,1
        sFactorPR,sFactorTR,sFactorNTR = 1,1,1
        if var in D_CA["Dividend"]:
            div_list = D_CA["Dividend"][var]
            dFactorPR,dFactorTR,dFactorNTR,Dividend,sDividend = Adjust_Dividend(div_list,isin_Data_Row,Tax_Rate,D_ISIN_Currency,Ex_Rate,date,Latest_Price)
       
        if var in D_CA["Spin"]:
            spin_list = D_CA["Spin"][var]
            spinFactorPR,spinFactorTR,spinFactorNTR,Spin = Adjust_Spin(spin_list,isin_Data_Row,Tax_Rate,D_ISIN_Currency,Ex_Rate,date,Latest_Price)
            
        if var in D_CA["Split"]:
            split_list = D_CA["Split"][var]
            splitFactorPR,splitFactorTR,splitFactorNTR,Split = Adjust_Split(split_list)
            
        CA= {}
        CA["PriceFactor_PR"] = dFactorPR*spinFactorPR/splitFactorPR
        CA["PriceFactor_TR"] = dFactorTR*spinFactorTR/splitFactorTR
        CA["PriceFactor_NTR"] = dFactorNTR*spinFactorNTR/splitFactorNTR

        CA["ShareFactor_PR"] = splitFactorPR
        CA["ShareFactor_TR"] = splitFactorTR
        CA["ShareFactor_NTR"] = splitFactorNTR
            
        if D_Index["Adjustment"] =="SA":
            CA["ShareFactor_PR"] *= 1/spinFactorPR
            CA["ShareFactor_TR"] *= 1/spinFactorTR
            CA["ShareFactor_NTR"] *= 1/spinFactorNTR
            
        CA["Dividend"] = Dividend
        CA["sDividend"] = sDividend
        CA["Spin"] = Spin
        CA["Split"] = Split        
        return CA
    except Exception as e:
        print('indxx-09', e)
        return e

def Delist(Clist,date1,D_LastDate,E_Date,MISSING_RIC_ISIN_LIST,D_ISIN_RIC):
    try:
        #print('inside Delist at Function_Calculate')

        #date = date.strftime("%d-%m-%Y")
        #E_Date = E_Date.strftime("%d-%m-%Y")    
        date1 = date1.date()
        E_Date = E_Date.date()
        for row in Clist:
            lastDate = D_LastDate[row[1]]
            '''if row[1]=='C21242-R':            
                print(D_LastDate[row[1]])
                print(lastDate <=date1)
                print(E_Date)'''
            #lasteDate = D_LastDate[row[1]].strftime("%d-%m-%Y")
            #print (datetime.fromisoformat(lasteDate))
            #if lastDate <=date1 and lastDate != E_Date:
            
            if lastDate <date1 and lastDate != E_Date and date1 != E_Date:
                print(row[1]+ '  Remoned')
                Clist.remove(row)
                if row[1]  in MISSING_RIC_ISIN_LIST:
                    print(row[1]+ '  Remoned from ric missing list')
                    MISSING_RIC_ISIN_LIST.remove(row[1])
                if row[1]  in D_ISIN_RIC:
                    D_ISIN_RIC.pop(row[1])
                    print(row[1]+ '  Remoned from isin_ric list')
    except Exception as e:
        print('indxx-10', e)
        return e
            
def Cal_Index_Open(D_Index,Clist,Latest_Price,Latest_Ex_Rate,date,Tax_Rate,D_ISIN_Currency,Ex_Rate,D_CA):
    try:
        Constituents_List = list()
        M_CAP_PR,M_CAP_TR,M_CAP_NTR = 0,0,0
        Dividend,sDividend,Spin,Split = 0,0,0,0
        Index_Value_PR,Index_Value_TR,Index_Value_NTR = D_Index["Index_Value_PR"],D_Index["Index_Value_TR"],D_Index["Index_Value_NTR"]
        #if date=='01-11-2016':# or date=='01-11-2016':
        '''if date=='11/01/16':
            print('Values at  Open before :' +str(date))
            print(D_Index["M_Cap_PR"])
            print(D_Index["Index_Value_PR"])
            print(D_Index["Divisor_PR"])
            print('End Open')'''
        for inputRow in Clist:
            CA ={}
            isin = inputRow[1]
            CA = Adjust_CA(D_Index,D_CA,inputRow,date,Tax_Rate,D_ISIN_Currency,Ex_Rate,Latest_Price)
            Adjusted_Price_PR  = Latest_Price[isin][0]*CA["PriceFactor_PR"]
            Adjusted_Price_TR  = Latest_Price[isin][0]*CA["PriceFactor_TR"]
            Adjusted_Price_NTR = Latest_Price[isin][0]*CA["PriceFactor_NTR"]
            shares_PR = inputRow[7]*CA["ShareFactor_PR"]
            shares_TR = inputRow[8]*CA["ShareFactor_TR"]
            shares_NTR = inputRow[9]*CA["ShareFactor_NTR"]
            inputRow[7] = shares_PR
            inputRow[8] = shares_TR
            inputRow[9] = shares_NTR
            inputRow[13] = inputRow[7]*Adjusted_Price_PR*Latest_Ex_Rate[isin]
            inputRow[14] = inputRow[8]*Adjusted_Price_TR*Latest_Ex_Rate[isin]
            inputRow[15] = inputRow[9]*Adjusted_Price_NTR*Latest_Ex_Rate[isin]
            M_CAP_PR  += inputRow[13]
            M_CAP_TR  += inputRow[14]
            M_CAP_NTR += inputRow[15]
            inputRow[16] = CA["Dividend"]
            inputRow[17] = CA["sDividend"]
            inputRow[18] = CA["Split"]
            inputRow[19] = CA["Spin"]
        print(D_Index)
        # D_Index["M_Cap_PR"]  = M_CAP_PR
        # D_Index["M_Cap_TR"]  = M_CAP_TR
        # D_Index["M_Cap_NTR"] = M_CAP_NTR
        # print(D_Index)
        Divisor_PR  = D_Index["M_Cap_PR"]/Index_Value_PR
        Divisor_TR  = D_Index["M_Cap_TR"]/Index_Value_TR
        Divisor_NTR = D_Index["M_Cap_NTR"]/Index_Value_NTR

        D_Index["Divisor_PR"]  = Divisor_PR
        D_Index["Divisor_TR"]  = Divisor_TR
        D_Index["Divisor_NTR"] = Divisor_NTR

        '''if date=='11/01/16':
            print('Values at  Open :' +str(date))
            print(D_Index["M_Cap_PR"])
            print(D_Index["Index_Value_PR"])
            print(D_Index["Divisor_PR"])
            print('End Open')'''
        for row in Clist:
            print(row)
            print(row[13])
            print(row[14])
            print(row[15])
            '''row[10] = (row[13]*100)/D_Index["M_Cap_PR"]
            row[11] = (row[14]*100)/D_Index["M_Cap_TR"]
            row[12] = (row[15]*100)/D_Index["M_Cap_NTR"]'''
            row[10] = (row[13])/D_Index["M_Cap_PR"]
            row[11] = (row[14])/D_Index["M_Cap_TR"]
            row[12] = (row[15])/D_Index["M_Cap_NTR"]
    except Exception as e:
        print('indxx-11', e)
        return e
           
def Cal_Index_Close(D_Index,Clist,Latest_Price,Latest_Ex_Rate,date1,Constituents_List_Final,period,Tax_Rate,D_ISIN_Currency,print_flag):
    Constituents_List = list()
    date = Q.DeteToStr(date1)
    M_CAP_PR,M_CAP_TR,M_CAP_NTR = 0,0,0
    Index_Value_PR,Index_Value_TR,Index_Value_NTR = 0,0,0
    Divisor_PR = D_Index["Divisor_PR"]
    Divisor_TR = D_Index["Divisor_TR"]
    Divisor_NTR = D_Index["Divisor_NTR"]
    
    for row in Clist:
        isin = row[1]
        print(Latest_Ex_Rate)
        print(isin)
        print(Latest_Price[isin][0])
        print(Latest_Ex_Rate[isin])
        row[13] = row[7]*Latest_Price[isin][0]*Latest_Ex_Rate[isin]
        row[14] = row[8]*Latest_Price[isin][0]*Latest_Ex_Rate[isin]
        row[15] = row[9]*Latest_Price[isin][0]*Latest_Ex_Rate[isin]
       
        M_CAP_PR  += row[13]
        M_CAP_TR  += row[14]
        M_CAP_NTR += row[15]
        
    D_Index["M_Cap_PR"]  =M_CAP_PR
    D_Index["M_Cap_TR"]  =  M_CAP_TR
    D_Index["M_Cap_NTR"] = M_CAP_NTR
    
    Index_Value_PR  = D_Index["M_Cap_PR"]/Divisor_PR
    Index_Value_TR  = D_Index["M_Cap_TR"]/Divisor_TR
    Index_Value_NTR = D_Index["M_Cap_NTR"]/Divisor_NTR

    D_Index["Index_Value_PR"]  = Index_Value_PR
    D_Index["Index_Value_TR"]  = Index_Value_TR
    D_Index["Index_Value_NTR"] = Index_Value_NTR

    for row in Clist:
        print('row')
        print(row)
        print('row')
        row[10] = (row[13])/D_Index["M_Cap_PR"]
        row[11] = (row[14])/ D_Index["M_Cap_TR"]
        row[12] = (row[15])/D_Index["M_Cap_NTR"]
        if print_flag==1:
            Fill_Constituents_List(D_Index,Constituents_List,row,period,date1,D_ISIN_Currency,Tax_Rate,Latest_Price,Latest_Ex_Rate)
    Constituents_List_Final.extend(Constituents_List)
    
def Cal_Shares(D_Index,list,Latest_Price,Latest_Ex_Rate,date1,Constituents_List,period,Tax_Rate,D_ISIN_Currency,print_flag,j):
    try:
        M_Cap = D_Index["MV"]
        date = Q.DeteToStr(date1) 
        ISIN_Shares = {}
        for inputRow in list:
            weight = inputRow[2]    
            isin = inputRow[1]
            shares = (weight*M_Cap)/(Latest_Price[isin][0]*Latest_Ex_Rate[isin])
            
            '''Shares(7,8,9)'''
            inputRow.append(shares)
            inputRow[7] = (shares)
            inputRow.append(shares)
            inputRow[8] = (shares)
            inputRow.append(shares)
            inputRow[9] = (shares)
            '''Weights(10,11,12)'''
            inputRow.append(weight)
            inputRow[10] = (weight)
            inputRow.append(weight)
            inputRow[11] = (weight)
            inputRow.append(weight)
            inputRow[12] = (weight)
            '''MCap(13,14,15)'''
            
            inputRow.append(weight*M_Cap)
            inputRow[13] = (weight*M_Cap)
            inputRow.append(weight*M_Cap)
            inputRow[14] = (weight*M_Cap)
            inputRow.append(weight*M_Cap)
            inputRow[15] = (weight*M_Cap)
            
            '''CA(16,17,18)'''
            inputRow.append('')
            inputRow.append('')
            inputRow.append('')
            inputRow.append('')
            #print('inputRow',inputRow)
            if print_flag==1 :#and j==0:             
                Fill_Constituents_List(D_Index,Constituents_List,inputRow,period,date1,D_ISIN_Currency,Tax_Rate,Latest_Price,Latest_Ex_Rate)
    except Exception as e:
        print('indxx-13', e)
        return e 
   
def Cal_Shares1(D_Index,list,Latest_Price,Latest_Ex_Rate,date1,Constituents_List,period,Tax_Rate,D_ISIN_Currency,print_flag,j):
    try:
        M_Cap_PR = D_Index["M_Cap_PR"]
        M_Cap_TR = D_Index["M_Cap_TR"]
        M_Cap_NTR = D_Index["M_Cap_NTR"]
        M_Cap_PR_Test = 0;
        date = Q.DeteToStr(date1) 
        ISIN_Shares = {}
        for inputRow in list:
            weight = inputRow[2]    
            isin = inputRow[1]
            shares_PR = (weight*M_Cap_PR)/(Latest_Price[isin][0]*Latest_Ex_Rate[isin])
            shares_TR = (weight*M_Cap_TR)/(Latest_Price[isin][0]*Latest_Ex_Rate[isin])
            shares_NTR = (weight*M_Cap_NTR)/(Latest_Price[isin][0]*Latest_Ex_Rate[isin])
            
            '''Shares(7,8,9)'''
            inputRow.append(shares_PR)
            inputRow.append(shares_TR)
            inputRow.append(shares_NTR)
            '''Weights(10,11,12)'''
            inputRow.append(weight)
            inputRow.append(weight)
            inputRow.append(weight)
            '''MCap(13,14,15)'''
            
            inputRow.append(weight*M_Cap_PR)
            inputRow.append(weight*M_Cap_TR)
            inputRow.append(weight*M_Cap_NTR)
            M_Cap_PR_Test += inputRow[13]
            '''CA(16,17,18)'''
            inputRow.append('')
            inputRow.append('')
            inputRow.append('')
            inputRow.append('')
            if print_flag==1 :#and j==0:             
                Fill_Constituents_List(D_Index,Constituents_List,inputRow,period,date1,D_ISIN_Currency,Tax_Rate,Latest_Price,Latest_Ex_Rate)
    except Exception as e:
        print('indxx-14', e)
        return e

def Fill_Constituents_List(D_Index,Constituents_List,row,period,date,D_ISIN_Currency,Tax_Rate,Latest_Price,Latest_Ex_Rate):
    try:
        Out_Row = [0]*32
        Out_Row[0] = period
        Out_Row[1] = date.date()
        
        Out_Row[2] = round(D_Index["Index_Value_PR"],13)
        Out_Row[3] = round(D_Index["M_Cap_PR"],13)
        Out_Row[4] = round(D_Index["Divisor_PR"],13)
        Out_Row[5] = round(D_Index["Index_Value_TR"],13)
        Out_Row[6] = round(D_Index["M_Cap_TR"],13)
        Out_Row[7] = round(D_Index["Divisor_TR"],13)
        Out_Row[8] = round(D_Index["Index_Value_NTR"],13)
        Out_Row[9] = round(D_Index["M_Cap_NTR"],13)
        Out_Row[10] = round(D_Index["Divisor_NTR"],13)
        '''ISIN'''
        Out_Row[11] = row[1]
        '''Currency'''
        Out_Row[12] = D_ISIN_Currency[row[1]]
        '''Country'''
        Out_Row[13] = row[5]
        '''Tax'''
        Out_Row[14] = Tax_Rate[row[5]]
        '''Shares'''
        Out_Row[15] = row[7]
        Out_Row[16] = row[8]
        Out_Row[17] = row[9]

        '''Local Price'''
        Out_Row[18] = Latest_Price[row[1]][0]
        '''Index Level Price'''
        Out_Row[19] = Latest_Price[row[1]][0]*Latest_Ex_Rate[row[1]]
        #MCap
        Out_Row[20] = row[13]
        Out_Row[21] = row[14]
        Out_Row[22] = row[15]

        '''Ex Rate'''
        Out_Row[23] = Latest_Ex_Rate[row[1]]
        '''Price Date'''
        Out_Row[24] = Latest_Price[row[1]][1]
        #Weights
        Out_Row[25] = row[10]
        Out_Row[26] = row[11]
        Out_Row[27] = row[12]
        #CA
        Out_Row[28] = row[16]   
        Out_Row[29] = row[17]
        Out_Row[30] = row[18]
        Out_Row[31] = row[19]
        
        Constituents_List.append(Out_Row)
    except Exception as e:
        print('indxx-15', e)
        return e
      

def Fill_Index_Report_Data(D_Index,Index_List,period,S_Date):
    try:
        row = []
        row.append(period)
        row.append(S_Date.date())
        row.append(D_Index["Index_Value_PR"])
        row.append(D_Index["Index_Value_TR"])
        row.append(D_Index["Index_Value_NTR"])                
        Index_List.append(row)
       #print('row......',row)
    except Exception as e:
        print('indxx-16', e)
        return e
    
def Set_Latest_Price(list,D_Price,Latest_Price,date):
    try:
        date = Q.DeteToStr(date)
        for row in list:
            var1 = row[1]+'_'+date
            if var1 in D_Price:            
                price = D_Price[var1]
                Row = []
                Row.append(price)
                Row.append(date)
                Latest_Price[row[1]] = Row
    except Exception as e:
        print('indxx-17', e)
        return e

'''def Get_Price(ISIN,D_Price,date,Latest_Price):
    date = date.strftime("%d-%m-%Y")
    var1 = ISIN+'_'+date
    if var1 in D_Price:            
        price = D_Price[var1]
        return price
    else:
        return Latest_Price[ISIN][0]'''
        
def Get_Ex_Rate(fromCurrency,toCurrency,Ex_Rate,date):
    try:
        date = Q.DeteToStr(date)
        var1 = fromCurrency +'_'+date
        if var1 in Ex_Rate:
            fromRate = (Ex_Rate[var1])
            if toCurrency =="USD":
                toRate = 1
            else:
                toRate = (Ex_Rate[toCurrency+'_'+date])
            ex_Rate = toRate/fromRate
            return ex_Rate
        else:
            return 1
    except Exception as e:
        print('indxx-18', e)
        return e
    
def Set_Latest_Ex_Rate(Index_Currency,list,Ex_Rate,Latest_Ex_Rate,date,D_ISIN_Currency):
    try:
        date = Q.DeteToStr(date)
        for row in list:
            fromCurrency = D_ISIN_Currency[row[1]]
            var2 = fromCurrency +'_'+date
            if var2 in Ex_Rate:
                fromRate = (Ex_Rate[fromCurrency+'_'+date])
                if Index_Currency =="USD":
                    toRate = 1
                else:
                    toRate = (Ex_Rate[Index_Currency+'_'+date])
                ex_Rate = toRate/fromRate
                Latest_Ex_Rate[row[1]] = ex_Rate
            else:
                if Index_Currency =="USD" and fromCurrency=="USD":
                    Latest_Ex_Rate[row[1]] = 1
    except Exception as e:
        print('indxx-19', e)
        return e

