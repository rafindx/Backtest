from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.urls import path
from api_app import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static

urlpatterns = [
    url(r'get-portfolio/', views.GetPortfolioView.as_view(), name='get-portfolio'),
    url(r'rerun-portfolio/', views.RerunPortfolioView.as_view(), name='rerun-portfolio'),
    url(r'run-portfolio/', views.RunPortfolioView.as_view(), name='rerun-portfolio'),

]