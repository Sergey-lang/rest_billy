from django.contrib import admin
from django.urls import path, include, re_path
from billy.views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/transaction/', PointTransactionViewSet.as_view()),
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
