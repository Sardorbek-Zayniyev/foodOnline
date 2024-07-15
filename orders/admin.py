from django.contrib import admin

from orders.models import Payment, Order, OrderedFood

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'address', 'payment_method', 'total', 'status',)



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)