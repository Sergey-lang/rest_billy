from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from billy.models import Profile
from order.models import Order
from order.pagination import OrderAPIPagination
from order.serializers import OrderSerializer, UpdateOrderStatusSerializer
from product.models import Product


def take_received_points_from_order_creator(request, sent_points):
    sender_id = request.user.id
    sender_profile = Profile.objects.get(pk=sender_id)
    received = sender_profile.received_points

    sender_profile.received_points = received - sent_points
    sender_profile.save()


def add_received_points_to_order_creator(recipient_id, new_points):
    recipient_profile = Profile.objects.get(pk=recipient_id)
    recipient_profile.received_points = recipient_profile.received_points + new_points
    recipient_profile.save()


class APIOrders(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderAPIPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            # For the administrator, we return all orders
            return Order.objects.all()
        else:
            # For the average user, we return only his own orders
            return Order.objects.filter(creator=user.profile)

    def post(self, request, *args, **kwargs):
        user = self.request.user

        total_user_points = user.profile.received_points
        product_id = int(request.data.get('product'))

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product_amount = product.amount
        # Does the user have enough points to purchase?
        if total_user_points < product_amount:
            return Response({'error': 'You don\'t have enough points'}, status=status.HTTP_400_BAD_REQUEST)

        take_received_points_from_order_creator(request, product_amount)

        return self.create(request, *args, **kwargs)


class APIOrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        user = self.request.user
        if not user.is_superuser and obj.creator != user.profile:
            self.permission_denied(self.request)

        return obj


class APIUpdateOrderStatus(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderStatusSerializer

    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            return Order.objects.none()

    def put(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']

        new_order_status = request.data.get('status')

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if new_order_status == order.status:
            return Response({'message': 'The order status has been successfully changed'}, status=status.HTTP_200_OK)

        order.status = new_order_status
        order.save()

        if order.status == 'Declined':
            # who create order?
            recipient_id = order.creator.id
            # how match points
            order_amount = order.product.amount
            # return points to creator.
            add_received_points_to_order_creator(recipient_id, order_amount)

        return Response({'message': 'The order status has been successfully changed'}, status=status.HTTP_200_OK)
