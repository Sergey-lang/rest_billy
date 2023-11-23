from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from billy.views import *

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'profile', ProfileListTransactionViewSet)

urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/transaction/', PointTransactionViewSet.as_view()),
    path('api/v1/transaction/<int:pk>/', APIGetTransactionSumm.as_view()),
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
