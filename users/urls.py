from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:user_id>/', views.display_customer_details, name='display_customer_details'),
    path('user/add/', views.add_library_customer, name='add_library_customer'),
    path('user/edit/<str:user_id>/', views.edit_library_customer, name='edit_library_customer'),
    path('user/delete/<str:user_id>/', views.display_customer_details, name='delete_library_customer'),
]
