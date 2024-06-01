from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.registerUser, name='register_user'),
    path('register-vendor/', views.registerVendor, name='register_vendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.myAccount, name='my_account'),
    path('cust-dashboard/', views.custDashboard, name='cust_dashboard'),
    path('vendor-dashboard/', views.vendorDashboard, name='vendor_dashboard'),
]
