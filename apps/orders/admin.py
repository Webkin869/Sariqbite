from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity", "options_text", "line_total")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "total", "distance_km", "eta_minutes", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("full_name", "phone", "address", "telegram_chat_id")
    readonly_fields = ("created_at", "updated_at", "subtotal", "delivery_fee", "total")
    inlines = [OrderItemInline]
