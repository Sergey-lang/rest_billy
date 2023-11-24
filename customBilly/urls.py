from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from billy.views import *

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
# router.register(r'/v1/api/profile', ProfileListTransactionViewSet)

urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),
    path('api/v1/transaction/', point_transaction_list, name='point_transaction_list'),
    path('api/v1/profile/', profile_list, name='profile_list'),
]
