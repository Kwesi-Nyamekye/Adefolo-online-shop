from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

#class OrderItemAdmin(admin.ModelAdmin):
 #   list_display = ['id', 'order', 'product', 'price', 'quantity', 'get_cost']
 #   list_filter = ['order', 'product']

admin.site.register (Order, OrderAdmin)