from django.urls import path, include
from . import views
from accounts import views as AccountViews 

urlpatterns = [
    path('', AccountViews.vendor_dashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/categories/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # FoodItem CRUD
    path('menu-builder/category/<int:pk>/food/add/', views.add_food, name='add_food'),
    # path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    #OpeningHour CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),
    
    path('my-orders/', views.my_orders, name='vendor_my_orders'),
    path('order-detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    
    

    


]
