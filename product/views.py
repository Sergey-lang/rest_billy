from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics

from .models import Product
from .pagination import ProductAPIPagination
from .serializers import ProductSerializer


class ProductViewSet(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # Фильтровать будем по полю amount модели Product
    filterset_fields = ['amount']
    search_fields = ['^name']
    ordering_fields = ['amount', 'name']
    ordering = ['created_at',]
