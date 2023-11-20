from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductView(APIView):
    pagination_class = CustomPagination()

    def get(self, request, pk=None):
        try:
            if pk:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data)

            products = Product.objects.all()
            paginated_queryset = self.pagination_class.paginate_queryset(products, request, self)
            serializer = ProductSerializer(paginated_queryset, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        try:
            product = Product.objects.get(pk=pk)

            serializer = ProductSerializer(product, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
