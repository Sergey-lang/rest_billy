from django.db.models import Sum
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
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


# class PointTransactionViewSet(generics.ListCreateAPIView):
#     queryset = PointTransaction.objects.all()
#     serializer_class = PointTransactionSerializer
#     pagination_class = ProductAPIPagination


@api_view(['GET', 'POST'])
def point_transaction_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    if request.method == 'POST':
        serializer = PointTransactionSerializer(data=request.data, many=False, context={'request': request})
        if serializer.is_valid():
            recipient_id = serializer.validated_data.get('recipient').id
            new_points = serializer.validated_data.get('points_count')

            recipient = Profile.objects.get(pk=recipient_id)
            recipient.received_points = recipient.received_points + new_points

            recipient.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    transactions = PointTransaction.objects.all()
    result_page = paginator.paginate_queryset(transactions, request)
    serializer = PointTransactionSerializer(result_page, many=True, context={'request': request})

    return Response(
        {
            'results': serializer.data,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link()
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def profile_list(request):
    transactions = Profile.objects.all()
    serializer = ProfileSerializer(transactions, many=True)
    return Response(serializer.data)


# class ProfileListTransactionViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class APIGetTransactionSumm(APIView):
    def get(self, request, pk):
        summ = PointTransaction.objects.filter(sender_id=request.user.id, recipient_id=pk).aggregate(
            total_points=Sum('points_count'))['total_points']
        return Response({'summ': summ}, status=status.HTTP_200_OK)
