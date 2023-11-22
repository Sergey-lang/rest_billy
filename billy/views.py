from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from .models import Product, PointTransaction, Profile
from .serializers import ProductSerializer, ProfileSerializer, PointTransactionSerializer


class ProductAPIPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductAPIPagination


class PointTransactionViewSet(generics.CreateAPIView):
    queryset = PointTransaction.objects.all()
    serializer_class = PointTransactionSerializer


class ProfileListTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
