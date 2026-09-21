from django.contrib import admin
from .models import Product, Box, Order, OrderItem

# Register your models here.

admin.site.register(Product)
admin.site.register(Box)
admin.site.register(Order)
admin.site.register(OrderItem)
