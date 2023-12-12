from django.contrib import admin
from .models import Product, Profile, PointTransaction, Order

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(PointTransaction)
admin.site.register(Order)
