from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.register_user, name='register_user'),
    path('register-vendor/', views.register_vendor, name='register_vendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.my_account, name='my_account'),
    path('cust-dashboard/', views.cust_dashboard, name='cust_dashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    

]
