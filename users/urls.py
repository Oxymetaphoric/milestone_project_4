from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.find_users, name='find_users'),
    path('new/add/', views.add_library_customer, name='add_library_customer'),
    path('edit/<str:user_id>/', views.edit_library_customer, name='edit_library_customer'),
    path('delete/<str:user_id>/', views.delete_library_customer, name='delete_library_customer'),
    path('search/', views.search_users, name='search_users'),
    re_path(r'^(?P<user_id>[A-Za-z0-9]+)/$', views.display_customer_details, name='display_customer_details'),
]
