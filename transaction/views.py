from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from billy.models import Profile

from .models import PointTransaction
from .serializers import PointTransactionSerializer


def take_point_from_sender(request, sent_points):
    sender_id = request.user.id
    sender_profile = Profile.objects.get(pk=sender_id)
    points = sender_profile.points

    if sent_points > points:
        remaining_points = sent_points - points
        sender_profile.points = sender_profile.points - (sent_points - remaining_points)
        sender_profile.received_points = sender_profile.received_points - remaining_points
        sender_profile.save()
    else:
        sender_profile.points = sender_profile.points - sent_points
        sender_profile.save()


def add_point_to_recipient(recipient_id, new_points):
    recipient_profile = Profile.objects.get(pk=recipient_id)
    recipient_profile.received_points = recipient_profile.received_points + new_points
    recipient_profile.save()


class APITransaction(APIView):
    def post(self, request):
        serializer = PointTransactionSerializer(data=request.data, many=False, context={'request': request})
        if serializer.is_valid():
            try:
                recipient_id = serializer.validated_data.get('recipient').id
                new_points = serializer.validated_data.get('points_count')
                sender_id = request.user.id
                sender_profile = Profile.objects.get(pk=sender_id)

                if sender_profile.points == 0 and sender_profile.received_points == 0:
                    raise ValueError('У тебя нет баллов для отправки view')

                take_point_from_sender(request, new_points)

                add_point_to_recipient(recipient_id, new_points)

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 20
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
