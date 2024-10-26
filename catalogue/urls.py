from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_stock_items, name='catalogue'),
]
