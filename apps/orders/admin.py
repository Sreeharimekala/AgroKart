
# Register your models here.
from django.contrib import admin
from .models import Cart, CartItem
from .models import Order, OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
