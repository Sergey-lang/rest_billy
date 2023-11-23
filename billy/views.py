from django.db.models import Sum
from rest_framework import viewsets, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

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


class PointTransactionViewSet(generics.ListCreateAPIView):
    queryset = PointTransaction.objects.all()
    serializer_class = PointTransactionSerializer
    pagination_class = ProductAPIPagination


class ProfileListTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class APIGetTransactionSumm(APIView):
    def get(self, request, pk):
        summ = PointTransaction.objects.filter(sender_id=request.user.id, recipient_id=pk).aggregate(
            total_points=Sum('points_count'))['total_points']
        return Response({'summ': summ}, status=status.HTTP_200_OK)
