from django.urls import path
from .views import display_customer_details

urlpatterns = [
    path('<str:user_id>/', display_customer_details, name='display_customer_details'),
]
