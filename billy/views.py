from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from .models import Product, PointTransaction
from .serializers import ProductSerializer, PointTransactionSerializer


class ProductAPIPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes_per_method = {
    #     "list": [permissions.IsAuthenticated],
    #     "retrieve": [permissions.IsAuthenticated],
    #     "update": [permissions.IsAdminUser],
    #     "partial_update": [permissions.IsAdminUser],
    #     "destroy": [permissions.IsAdminUser],
    #     "create": [permissions.IsAdminUser],
    # }
    pagination_class = ProductAPIPagination


class PointTransactionViewSet(generics.CreateAPIView):
    queryset = PointTransaction.objects.all()
    serializer_class = PointTransactionSerializer

    # permission_classes_per_method = {
    #     "create": [permissions.IsAuthenticated],
    # }


