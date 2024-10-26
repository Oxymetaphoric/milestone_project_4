from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_catalogue_items, name='catalogue'),
]
