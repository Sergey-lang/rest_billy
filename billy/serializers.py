from rest_framework import serializers

from .models import Profile, Order


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'received_points', 'points')


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
