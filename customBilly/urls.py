from django.contrib import admin
from django.urls import path, include
from billy.views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # path('admin/product', ProductAPIList.as_view()),
    # path('admin/product/<int:pk>', ProductAPIList.as_view()),
]
