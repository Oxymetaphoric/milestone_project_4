from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_catalogue_items, name='catalogue'),
    path('search/', views.search_catalogue, name='search_catalogue'),
    path('edit/<str:StockID>/', views.edit_stock_item, name='edit_library_customer'),
]
