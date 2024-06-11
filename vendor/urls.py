from django.urls import path, include
from . import views
from accounts import views as AccountViews 

urlpatterns = [
    path('', AccountViews.vendor_dashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),

]
