from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('line_total',)
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'grand_total', 'date')
    list_filter = ('status', 'date')
    search_fields = ('order_number', 'email', 'full_name')
    readonly_fields = ('order_number', 'date', 'order_total', 'delivery_cost', 'grand_total')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)