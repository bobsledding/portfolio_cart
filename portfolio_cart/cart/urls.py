from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_to_cart, name='add'),
    path('remove/', views.remove_from_cart, name='remove'),
]