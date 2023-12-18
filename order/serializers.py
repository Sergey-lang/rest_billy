from rest_framework import serializers
from billy.serializers import ProfileSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = []

    def create(self, validated_data):
        creator = self.context['request'].user.profile
        validated_data['creator'] = creator
        order = super().create(validated_data)
        return order


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
