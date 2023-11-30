from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from billy.views import *

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api/v1/transaction/', APITransaction.as_view()),
    path('api/v1/profile/', APIProfile.as_view()),
]
