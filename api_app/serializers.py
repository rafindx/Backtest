from rest_framework import serializers
from django.core.serializers import serialize
from django.core import serializers as core_serializers
from django.http import JsonResponse
from calculation.models import PortfolioDescription, PortfolioComposition, TaxRate

class PortfolioDataSerializer(serializers.ModelSerializer):
    
    def get_saved_portfolio(self):
        try:
            portfolio_data = PortfolioDescription.objects.all().values()
            return {'data':portfolio_data, 'message':f'Success', 'status': 1}
        except:
            logger.error(f'{traceback.format_exc()}')
            return {'message': 'Error fetching data.', 'status': 0}