from django.urls import path, include
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.cust_dashboard, name='customer'),
    path('profile/', views.customer_profile, name='customer_profile'),

   
    

]
