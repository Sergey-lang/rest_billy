from django.db.models import Sum
from rest_framework import serializers
from django.db.models import Q
from django.utils.timezone import now
from .models import Product, PointTransaction, Profile, Order


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        exclude = []


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


class PointTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PointTransaction
        fields = ['id', 'sender', 'recipient', 'points_count', 'created_at']

    def get_sender(self, obj):
        return self.context['request'].user.id

    def validate_points_count(self, value):
        if value > 100:
            raise serializers.ValidationError({'error': 'Ты не можешь никому отправить больше 100 баллов'})
        return value

    def validate(self, data):
        x = data['recipient'].id
        if self.context['request'].user.id == data['recipient'].id:
            raise serializers.ValidationError(
                {'error': 'Ты не можешь отправлять баллы себе'})
        return data

    def create(self, validated_data):
        # auth user = 2
        sender_id = self.context['request'].user.id
        # profile user = 2
        recipient_id = self.validated_data['recipient'].id
        points_count = self.validated_data['points_count']

        # Get recipient profile
        recipient = Profile.objects.get(pk=recipient_id)

        if not recipient:
            raise serializers.ValidationError({'error': 'Пользователь не найден'})
        # получить сумму переданных баллов между авторизованным юзером и получателем за текущий месяц
        current_month = now().month
        result = PointTransaction.objects.filter(
            Q(sender_id=sender_id, recipient_id=recipient_id) & Q(created_at__month=current_month)).aggregate(
            total_points=Sum('points_count'))
        # проверить None если не найдено ничего
        summ = result['total_points'] if result['total_points'] is not None else 0

        # проверить лимит баллов к 1 пользователю перед созданием транзакции
        if points_count + summ > 100:
            raise serializers.ValidationError({'error': 'Ты не можешь отправить 1 пользователю больше 100 баллов'})

        validated_data['sender_id'] = sender_id
        point_transaction = super().create(validated_data)
        return point_transaction
