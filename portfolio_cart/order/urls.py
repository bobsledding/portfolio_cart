from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('ecpay/', views.ecpay_view, name='ecpay_view'),
    path('result/', views.result, name='result'),
    path('detail/', views.detail, name='detail'),
    path('receive_from_ecpay/', views.receive_from_ecpay, name='receive_from_ecpay'),
]