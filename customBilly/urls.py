from django.contrib import admin
from django.urls import path
from billy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product/', views.ProductView.as_view()),
    path('api/v1/product/<int:pk>/', views.ProductView.as_view()),
]
