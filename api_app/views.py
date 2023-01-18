from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PortfolioDataSerializer
import csv
import dateutil.parser
from django.db.models import Q
import datetime
import pandas as pd
from calculation.utils import handle_uploaded_file,Load_CSV, Validate_Read_CSV, remove_percent_symbole, Cal_Index, Rerun_Dbdata, DateTime, save_input_file, Rerun_Dbdata1
from calculation.models import PortfolioDescription, PortfolioComposition, TaxRate


class GetPortfolioView(APIView):
	def get(self, request, format=None):
		serializer_val = PortfolioDataSerializer()
		ser_data = serializer_val.get_saved_portfolio()
		prortfolio = PortfolioDescription.objects.all()
		return Response(ser_data['data'], status= status.HTTP_200_OK)

class RerunPortfolioView(APIView):
	def post(self, request, format=None):
		D_Index ={}
		portfolio_id = request.POST.get('portfolio_id')
		portfolio = PortfolioDescription.objects.filter(id=portfolio_id)
		get_composition = PortfolioComposition.objects.filter(portfolio_id=portfolio_id)
		if portfolio:
			for portfolio_data in portfolio:
				D_Index["Identifier"] = portfolio_data.identifier
				D_Index["IV"] = int(portfolio_data.index_value_pr)
				D_Index["MV"] = int(portfolio_data.market_value_pr)
				D_Index["Currency"] = portfolio_data.currency
				D_Index["Adjustment"] = portfolio_data.spin_off_treatment
				D_Index["DCFO"] = portfolio_data.constituents_file_download
				start_date =str(dateutil.parser.parse(str(portfolio_data.start_date)).date())
				end_date = request.POST.get('end_date')
				start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
				end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
				file_name = portfolio_data.file_name
				data = pd.read_excel('./static/backtest-file/rerun_input_files/'+str(file_name), header=None)
				a = data.values.tolist()
				first_period=a[1][0]
				last_period = portfolio_data.period
				Period ={}
				Period["First"] = first_period
				Period["Last"] = last_period
				rerun_date = Rerun_Dbdata1(D_Index,file_name,end_date)
				data = {
						'status': True,
						'success': 'Index file and Constituents file is created please download.',
						'index_file': rerun_date['index_value_file'],
						'constituents_file': rerun_date['constituents_file']
					}
				return Response(data, status= status.HTTP_200_OK)
		else:
			data = {
				'status': False,
				'error': 'Portfolio and composition is not created please enter valid details!'
				}
			return Response(data, status= status.HTTP_400_BAD_REQUEST)



class RunPortfolioView(APIView):
	def post(self, request, format=None):
		try:
			print(request.POST.get('confirmbox'))
			print(request.FILES.get('protfolio_file'))
			D_Index = {}
			portfolioName=''
			if request.method =='POST':
				confirmbox = request.POST.get('confirmbox')
				input_file=request.FILES.get('protfolio_file')
				file_name = handle_uploaded_file(request.FILES.get('protfolio_file'), confirmbox)
				print(file_name)
				if confirmbox =="":
					tax_file = handle_uploaded_file(request.FILES.get('tax_rate'), confirmbox)
				identifier = request.POST.get('identifier')
				currency = request.POST.get('currency')
				save_data = request.POST.get('save_data')
				if save_data == 'yes':
					file_with_location= save_input_file(input_file)
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
					taxFileName ='./static/backtest-file/input/'+str(tax_file)
				if confirmbox =='':
					csv_data = Validate_Read_CSV('./static/backtest-file/input/'+file, identifier,taxFileName)
				else:
					csv_data = Load_CSV('./static/backtest-file/input/'+file,taxFileName)
				if csv_data['error']:
					data = {
							'status': False,
							'error': csv_data['error']
							}
				elif csv_data['warning'] and confirmbox =='':
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
					if save_data == 'yes':
						portfolioName = request.POST.get('name')+'_'+str(datetime.datetime.now())
						portfolio = create_portfolio(request, save_inputfile, csv_data, last_Period)
						composition = portfolio_composition(csv_data, currency, portfolio, last_Period, csv_data['quote_data'])
					D_Index["Identifier"] = identifier
					D_Index["IV"] = float(request.POST.get('index_vlaue'))
					D_Index["MV"] = float(request.POST.get('market_value'))
					D_Index["Currency"] = currency
					D_Index["Adjustment"] = request.POST.get('spin_off')
					D_Index["DCFO"] = request.POST.get('download')
					Tax_Rate = csv_data["Tax_Rate"]
					save_file = Cal_Index(D_Index, csv_data)
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
				return Response(data, status= status.HTTP_200_OK)
		except Exception as inst:
			data = {
				'status': False,
				'error': 'Please check you file.'+str(inst)
				}
		return Response(data, status= status.HTTP_400_BAD_REQUEST)



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