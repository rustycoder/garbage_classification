from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='garbage_admin_dashboard'),
    path('login', views.admin_login, name='garbage_admin_login'),
    path('register', views.admin_register, name='garbage_admin_register'),
    path('logout', views.admin_logout, name='garbage_admin_logout'),
    path('forgot_password', views.admin_forgot_password, name='garbage_admin_forgot_password'),
    path('reset_password', views.admin_reset_password, name='garbage_admin_reset_password'),

    path('profile', views.profile, name='garbage_admin_profile'),
    path('update_profile', views.profile_update, name='garbage_admin_profile_update'),
    path('token_transactions', views.token_transactions, name='garbage_admin_profile_update'),
    path('buy_token', views.buy_token, name='garbage_admin_profile_update'),
    
    path('buy_tokens', views.buy_tokens, name='garbage_admin_buy_token'),
]