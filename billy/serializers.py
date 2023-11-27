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
        fields = ('id', 'first_name', 'last_name', 'received_points', 'points')


class PointTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = PointTransaction
        fields = ['id', 'sender', 'recipient', 'points_count']

    def get_sender(self, obj):
        return self.context['request'].user.id

    def create(self, validated_data):
        sender_id = self.context['request'].user.id
        recipient_id = self.validated_data['recipient'].id
        points_count = self.validated_data['points_count']

        # Get recipient profile
        recipient = Profile.objects.get(pk=recipient_id)

        if sender_id == recipient_id:
            raise serializers.ValidationError({'error': 'Ты не можешь отправлять баллы себе'})

        if points_count > 100:
            raise serializers.ValidationError({'error': 'Ты не можешь никому отправить больше 100 баллов'})

        if not recipient:
            raise serializers.ValidationError({'error': 'Пользователь не найден'})
        # получить сумму переданных баллов между авторизованным юзером и получателем
        summ = PointTransaction.objects.filter(sender_id=sender_id, recipient_id=recipient_id).aggregate(
            total_points=Sum('points_count'))['total_points']
        # проверить лимит баллов к 1 пользователю перед созданием транзакции
        if points_count + summ >= 1200:
            raise serializers.ValidationError({'error': 'Ты не можешь отправить 1 пользователю больше 100 баллов'})

        validated_data['sender_id'] = sender_id
        point_transaction = super().create(validated_data)
        return point_transaction
