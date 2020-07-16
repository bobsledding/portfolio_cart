from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('ecpay/', views.ecpay_view, name='ecpay_view'),
    path('result/', views.result, name='result'),
    path('receive_from_ecpay/', views.receive_from_ecpay, name='receive_from_ecpay'),
]