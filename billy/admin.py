from django.contrib import admin
from .models import Product, Profile, PointTransaction

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(PointTransaction)
