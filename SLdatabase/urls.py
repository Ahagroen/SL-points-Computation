from django.urls import path
from . import views

app_name = 'SLdatabase'
urlpatterns = [
    path('', views.index,name='index'),
    path('<str:driverName>/', views.driverPage,name="driverPage"), #change to driver name instead of ID?
]
