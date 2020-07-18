from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('ecpay/', views.ecpay_view, name='ecpay_view'),
    path('ecpay/<int:order_id>/', views.pay_from_index, name='pay_from_index'),
    path('result/', views.result, name='result'),
    path('receive_from_ecpay/', views.receive_from_ecpay, name='receive_from_ecpay'),
    path('cancel/<int:order_id>/', views.cancel, name='cancel'),
]