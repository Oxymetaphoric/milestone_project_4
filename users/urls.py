from django.urls import path, re_path
from . import views
from catalogue import views as catalogue_views

urlpatterns = [
    path('', views.find_users, name='find_users'),
    path('new/add/', views.add_library_customer, name='add_library_customer'),
    path('edit/<str:user_id>/', views.edit_library_customer, name='edit_library_customer'),
    path('delete/<str:user_id>/', views.delete_library_customer, name='delete_library_customer'),
    path('search/', views.search_users, name='search_users'),
    path('customer_loan_history/<str:user_id>/', views.customer_loan_history, name='customer_loan_history'),
    path('lost_item/', catalogue_views.lost_item, name='lost_item'),
    path('item/<str:BibNum>/', catalogue_views.book_info, name='book_info'),
    re_path(r'^(?P<user_id>[A-Za-z0-9]+)/$', views.display_customer_details, name='display_customer_details'),
] 
