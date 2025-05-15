from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Displays order items within an order in the admin panel."""

    model = OrderItem
    readonly_fields = ("line_total",)
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """Custom Admin Panel for Orders."""

    list_display = (
        "order_number",
        "user",
        "grand_total",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__username", "email")
    ordering = ("-created_at",)  # Show latest orders first
    inlines = [OrderItemInline]  # Shows order items inside orders

    actions = [
        "mark_as_paid",
        "mark_as_shipped",
        "mark_as_delivered",
        "mark_as_cancelled",
    ]

    def mark_as_paid(self, request, queryset):
        queryset.update(status="paid")
        self.message_user(request, "Selected orders marked as Paid.")

    mark_as_paid.short_description = "Mark selected orders as Paid"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="shipped")
        self.message_user(request, "Selected orders marked as Shipped.")

    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(request, "Selected orders marked as Delivered.")

    mark_as_delivered.short_description = "Mark selected orders as Delivered"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, "Selected orders marked as Cancelled.")

    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
