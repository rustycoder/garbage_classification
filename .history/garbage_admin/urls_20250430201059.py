from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.members, name='members'),
]