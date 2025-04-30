from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='weather_admin_dashboard'),
]