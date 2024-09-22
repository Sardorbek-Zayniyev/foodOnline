from django.contrib import admin

from orders.models import Payment, Order, OrderedFood

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'address', 'payment_method', 'total', 'status', 'order_placed_to', 'is_ordered')
    inlines = [OrderedFoodInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)