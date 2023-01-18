from django.shortcuts import render
from decimal import Decimal
from calculation.models import PortfolioDescription, PortfolioComposition, TaxRate
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from calculation.utils import handle_uploaded_file,Load_CSV, Validate_Read_CSV, remove_percent_symbole, Cal_Index, Rerun_Dbdata, DateTime, save_input_file, Rerun_Dbdata1
from django.http import JsonResponse
from django.views import View
import csv
import dateutil.parser
from django.db.models import Q
import datetime
import pandas as pd

# look template in 'root folder'
# The folder 'templates' is not checked inside the 'configuration folder'
# But it is checked inside the 'app' folder


class PortfolioView(View):
    """
    ** POST DATA **
    """
    def post(self, request):
        try:
            D_Index = {}
            portfolioName=''
            print('Submit Button Clicked at ' + str(datetime.datetime.now()))
            if request.method =='POST':
                confirmbox = request.POST.get('confirmbox')
                input_file=request.FILES.get('protfolio_file')
                file_name = handle_uploaded_file(request.FILES.get('protfolio_file'), confirmbox)
                #print('file_name::',file_name)
                if confirmbox =="":
                    tax_file = handle_uploaded_file(request.FILES.get('tax_rate'), confirmbox)
                identifier = request.POST.get('identifier')
                currency = request.POST.get('currency')
                save_data = request.POST.get('save_data')
                if save_data == 'yes':
                    file_with_location= save_input_file(input_file)
                    # print('file_with_location:',file_with_location)
                    save_inputfile = file_with_location.get('save_inputfile')
                    file_location = file_with_location.get('input_file_location')

                latest_file = request.POST.get('latest_file')
                if confirmbox:
                    tax_file = request.POST.get('tax_file_name')
            
                if latest_file:
                    file = latest_file

                else:
                    file = file_name
                taxFileName=''
                if tax_file not in (None, ""):
                    print('taxfile is not null')
                    #print(tax_file)
                    taxFileName ='./static/backtest-file/input/'+str(tax_file)

                if confirmbox =='':
                    print('File Validation Started at ' + str(datetime.datetime.now()))
                    csv_data = Validate_Read_CSV('./static/backtest-file/input/'+file, identifier,taxFileName)
                    print( csv_data['warning'])
                    print('File Validation Ends at ' + str(datetime.datetime.now()))
                else:
                    print('Load CSV Started at ' + str(datetime.datetime.now()))
                    csv_data = Load_CSV('./static/backtest-file/input/'+file,taxFileName)
                    print('Load CSV Ends at ' + str(datetime.datetime.now()))
                if csv_data['error']:
                    data = {
                        'status': False,
                        'error': csv_data['error']
                        }
                elif csv_data['warning'] and confirmbox =='':
                    #print('tax_file:',tax_file)
                    data = {
                        'status': True,
                        'warning': csv_data['warning'],
                        'file_name': file_name,
                        'tax_file_name': tax_file
                        }
                    
                else:
                    last_Period = csv_data['Period']["Last"]
                    Quote_Data = csv_data['quote_data']
                    index_vlaue = request.POST.get('index_vlaue')
                    market_value = request.POST.get('market_value')
        
                    if market_value==0 or index_vlaue==0:
                        index_vlaue= 1000
                        market_value=100000
                    if market_value < index_vlaue:
                        data = {
                            'status': False,
                            'error_msg': 'Market Value should be greater then Index Value.'
                            }
                        return JsonResponse(data)
                    if save_data:
                        print('Save Portfolio Started at ' + str(datetime.datetime.now()))
                        portfolioName = request.POST.get('name')+'_'+str(datetime.datetime.now())
                        portfolio = create_portfolio(request, save_inputfile, csv_data, last_Period)
                        composition = portfolio_composition(csv_data, currency, portfolio, last_Period, csv_data['quote_data'])
                        print('Save Portfolio Ends at ' + str(datetime.datetime.now()))
                    D_Index["Identifier"] = identifier
                    D_Index["IV"] = float(request.POST.get('index_vlaue'))
                    D_Index["MV"] = float(request.POST.get('market_value'))
                    D_Index["Currency"] = currency
                    D_Index["Adjustment"] = request.POST.get('spin_off')
                    D_Index["DCFO"] = request.POST.get('download')
                    Tax_Rate = csv_data["Tax_Rate"]
                    #print('Tax_Rate:',Tax_Rate)
                    #print('D_Index',D_Index)
                    print('Index Calculation Started at ' + str(datetime.datetime.now()))
                    #save_file = Cal_Index(D_Index, csv_data['D_Data'], csv_data['D_ISIN'], csv_data['D_Date'], Quote_Data,csv_data['Period'],csv_data['ISIN_LIST'],Tax_Rate)
                    save_file = Cal_Index(D_Index, csv_data)
                    print('inviews')
                    #print('save_file',save_file)
                    print('Index Calculation Ends at ' + str(datetime.datetime.now()))
                    message =''
                    if portfolioName not in (None, ""):
                        message = 'Portfolio has been saved with name as '+portfolioName+' . Index file and Constituents file is created successfully!'
                    else:
                        message = 'Index file and Constituents file is created successfully!'
                    data = {
                        'status': True,
                        'wrng': save_file['warningMessage'],
                        'success': message,
                        'index_file': save_file['index_value_file'],
                        'constituents_file': save_file['constituents_file']
                        }
                    #print('data:',data)
                return JsonResponse(data)
        except Exception as inst:
            print('INSIDE EXCEPTION')
            print(type(inst))
            print(inst.args)
           
            data = {
                'status': False,
                'error': 'Please check you file.'+str(inst)
                }
            return JsonResponse(data)

def create_portfolio(request, save_inputfile, data, last_Period):
    start_date = str(last_Period)+'_START'
    end_date = str(last_Period)+'_END'
    #date_start = DateTime(data['D_Date'][start_date])
    #date_end = DateTime(data['D_Date'][end_date])
    date_start = data['D_Date'][start_date]
    date_end = data['D_Date'][end_date]

    portfolio_obj = PortfolioDescription.objects.create(
        name = request.POST.get('name')+'_'+str(datetime.datetime.now()),
        currency = request.POST.get('currency'),
        identifier = request.POST.get('identifier'),
        spin_off_treatment = request.POST.get('spin_off'),
        index_value_pr = Decimal(request.POST.get('index_vlaue')),
        market_value_pr = Decimal(request.POST.get('market_value')),
        constituents_file_download = request.POST.get('download'),
        file_name = save_inputfile,
        period = data['Period']['Last'],
        start_date = date_start,
        end_date = date_end

        )
    last_obj = PortfolioDescription.objects.last()    
    return last_obj

def portfolio_composition(data, currency, portfolio, last_Period, quote_data):
    for comp_data in data['D_Data'][last_Period]:
        isin = comp_data[1]
        #print('quote_data+++++++++++++++++++++++++++++++++++++++++',quote_data)
        if isin in quote_data.keys():
            quote_id = quote_data[isin]
        else:
            quote_id = 0
        weights = comp_data[2]
        composition_obj = PortfolioComposition.objects.create(
            portfolio= portfolio,
            isin = comp_data[1],
            ric = comp_data[6],
            weights = weights,
            shares = 0,
            currency = currency,
            country = comp_data[5],
            quote_id = quote_id,
            )
        last_composition = PortfolioDescription.objects.last()
    return last_composition

class GetPortfolioView(View):
    """docstring for GetPortfolioView"""
    def post(self, request):
        if request.method =='POST':
            portfolio_id = request.POST.get('id')
            portfolio_list = PortfolioDescription.objects.filter(id=portfolio_id)
            for portfolio in portfolio_list:
                start_date = dateutil.parser.parse(str(portfolio.start_date)).date()
                end_date = dateutil.parser.parse(str(portfolio.end_date)).date()
                data = {
                    'status': True,
                    'start_date':start_date,
                    'end_date': end_date
                    }
            return JsonResponse(data)


class RerunPortfolio(View):
    """docstring for ClassName"""
    def post(self, request):
        if request.method == 'POST':
            D_Index ={}
            portfolio_id = request.POST.get('portfolio_id')
            portfolio = PortfolioDescription.objects.filter(id=portfolio_id)
            get_composition = PortfolioComposition.objects.filter(portfolio_id=portfolio_id)

            for portfolio_data in portfolio:
                D_Index["Identifier"] = portfolio_data.identifier
                D_Index["IV"] = int(portfolio_data.index_value_pr)
                D_Index["MV"] = int(portfolio_data.market_value_pr)
                D_Index["Currency"] = portfolio_data.currency
                D_Index["Adjustment"] = portfolio_data.spin_off_treatment
                D_Index["DCFO"] = portfolio_data.constituents_file_download
                start_date =str(dateutil.parser.parse(str(portfolio_data.start_date)).date())
                end_date = request.POST.get('end_date')
                print('end_date@@@',end_date)
                start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
                print('end_date###',end_date)
                #print(start_date)
                #print(end_date)

                file_name = portfolio_data.file_name
                data = pd.read_excel('./static/backtest-file/rerun_input_files/'+str(file_name), header=None)   
                a = data.values.tolist()
                first_period=a[1][0]
                last_period = portfolio_data.period
                Period ={}
                Period["First"] = first_period
                Period["Last"] = last_period

            #rerun_date = Rerun_Dbdata(D_Index, start_date, end_date, Period, get_composition)
            rerun_date = Rerun_Dbdata1(D_Index,file_name,end_date)
            data = {
                    'status': True,
                    'success': 'Index file and Constituents file is created please download.',
                    'index_file': rerun_date['index_value_file'],
                    'constituents_file': rerun_date['constituents_file']
                }
        else:
            data = {
                'status': False,
                'error': 'Portfolio and composition is not created please enter valid details!'
                }
        return JsonResponse(data)

class getTax(View):
    """docstring for ClassName"""
    def get(self, request):
        tax_data = TaxRate.objects.all()
        return render(request, 'tax_file.html', {'tax_object': tax_data})


        
class AddNewTax(View):
    """docstring for ClassName"""
    def post(self, request):
        if request.method=='POST':
            country = request.POST.get('country')
            tax = request.POST.get('tax')
            tax_obj = TaxRate.objects.create(
                country=country,
                tax=tax
                )
            response ={'status': True, 'message':'Tax Rate successfully added.'}        
        return JsonResponse(response)

class updateTax(View):
    def post(self, request):
        if request.method=='POST':
            tax_id = request.POST.get('id')
            tax = request.POST.get('tax')
            TaxRate.objects.filter(id=tax_id).update(tax=tax)
            response ={'status': True, 'message':'Tax Rate successfully updated.', 'tax': tax}        
        return JsonResponse(response)


