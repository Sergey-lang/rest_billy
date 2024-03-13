from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.shortcuts import redirect

from billy.views import *
from order.views import APIOrderDetail, APIOrders, APIUpdateOrderStatus
from product.views import ProductViewSet
from transaction.views import APITransaction

router = routers.DefaultRouter()

urlpatterns = [
    path('', lambda request: redirect('admin/')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api/v1/product/', ProductViewSet.as_view()),
    path('api/v1/transaction/', APITransaction.as_view()),
    path('api/v1/order/<int:pk>/', APIOrderDetail.as_view(), name='order-detail'),
    path('api/v1/order/', APIOrders.as_view(), name='order-list'),
    path('api/v1/order/<int:pk>/status/', APIUpdateOrderStatus.as_view(), name='order-status'),
    path('api/v1/profile/', APIProfile.as_view()),
]
