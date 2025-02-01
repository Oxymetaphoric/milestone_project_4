from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_catalogue_items, name='catalogue'),
    path('search/', views.search_catalogue, name='search_catalogue'),
    path('item/<str:BibNum>/', views.book_info, name='book_info'),
    path('check_in/', views.book_info, name='check_in'),
    path('check_out/', views.book_info, name='check_out'),
]
