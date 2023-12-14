from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from billy.views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api/v1/product/', ProductViewSet.as_view()),
    path('api/v1/transaction/', APITransaction.as_view()),
    path('api/v1/order/<int:pk>/', APIOrderDetail.as_view(), name='order-detail'),
    path('api/v1/order/', APIOrders.as_view(), name='order-list'),
    path('api/v1/profile/', APIProfile.as_view()),
]
