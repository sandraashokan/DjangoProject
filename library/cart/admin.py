from django.contrib import admin

# Register your models here.
from cart.models import Cart,account,order

admin.site.register(Cart)
admin.site.register(account)
admin.site.register(order)