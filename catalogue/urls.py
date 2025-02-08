from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.display_catalogue_items, name='catalogue'),
    path('search/', views.search_catalogue, name='search_catalogue'),
    path('item/<str:BibNum>/', views.book_info, name='book_info'),
    path('check_in/', views.check_in, name='check_in'),
    path('check_out/', views.check_out, name='check_out'),
    path('lost_item/', views.lost_item, name='lost_item'),
    path('display_customer_details/<uuid:user_id>/', user_views.display_customer_details, name='display_customer_details')
]
