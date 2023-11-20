from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # get first 3
    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #
    #     if not pk:
    #         return Product.objects.all()[:3]
    #
    #     return Product.objects.filter(pk=pk)

    @action(methods=['get'], detail=False)
    def list_id(self, request, pk=None):
        ids = Product.objects.all().values_list('id', flat=True)
        return Response(ids)
