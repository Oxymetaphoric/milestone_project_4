from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_catalogue_items, name='catalogue'),
    path('search/', views.search_catalogue, name='search_catalogue'),
    path('item/<str:BibNum>/', views.book_info, name='book_info'),  # Changed from 'edit' to match view name
]
