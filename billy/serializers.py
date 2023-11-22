from django.db.models import Sum
from rest_framework import serializers

from .models import Product, PointTransaction, Profile


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        exclude = []


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'received_points')


class PointTransactionSerializer(serializers.ModelSerializer):
    total_send = serializers.SerializerMethodField()

    class Meta:
        model = PointTransaction
        fields = ['id', 'sender', 'recipient', 'points_count', 'total_send']

    def get_total_send(self, obj):
        sender_id = self.initial_data['sender']
        recipient_id = self.initial_data['recipient']
        summ = PointTransaction.objects.filter(sender_id=sender_id, recipient_id=recipient_id).aggregate(
            total_points=Sum('points_count'))['total_points']
        return int(summ)

    def create(self, validated_data):
        sender_id = self.initial_data['sender']
        recipient_id = self.initial_data['recipient']
        points_count = self.initial_data['points_count']

        # Get recipient profile
        recipient = Profile.objects.get(pk=recipient_id)

        if not recipient:
            raise serializers.ValidationError({'error': 'Нет такого юзера'})

        summ = PointTransaction.objects.filter(sender_id=sender_id, recipient_id=recipient_id).aggregate(
            total_points=Sum('points_count'))['total_points']

        if int(points_count) + summ >= 100:
            raise serializers.ValidationError({'error': 'Слишком много отправил'})

        # Send point to recipient profile
        recipient.received_points = recipient.received_points + points_count
        recipient.save()

        return validated_data
