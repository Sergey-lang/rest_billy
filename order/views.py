from rest_framework import generics
from order.models import Order
from order.pagination import OrderAPIPagination
from order.serializers import OrderSerializer, UpdateOrderStatusSerializer


class APIOrders(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderAPIPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Для администратора, возвращаем все заказы
            return Order.objects.all()
        else:
            # Для обычного пользователя, возвращаем только его собственные заказы
            return Order.objects.filter(creator=user.profile)


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
    # todo: only admin
