from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now
from rest_framework import serializers

from billy.models import Profile
from .models import PointTransaction


class PointTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PointTransaction
        fields = ['id', 'sender', 'recipient', 'points_count', 'created_at']

    def get_sender(self, obj):
        return self.context['request'].user.id

    def validate_points_count(self, value):
        if value > 100:
            raise serializers.ValidationError({'error': 'You can\'t send more than 100 points per month to anyone.'})
        return value

    def validate(self, data):
        recipient_id = data['recipient'].id
        if self.context['request'].user.id == recipient_id:
            raise serializers.ValidationError(
                {'error': 'What the hell? You can\'t send points to yourself!'})
        return data

    def create(self, validated_data):
        sender_id = self.context['request'].user.id
        recipient_id = self.validated_data['recipient'].id
        # points_count = self.validated_data['points_count']

        # Get recipient profile
        recipient = Profile.objects.get(pk=recipient_id)

        if not recipient:
            raise serializers.ValidationError({'error': 'Пользователь не найден'})
        # get the amount of points transferred between the authorized user and the recipient for the current month
        # current_month = now().month
        # result = PointTransaction.objects.filter(
        #     Q(sender_id=sender_id, recipient_id=recipient_id) & Q(created_at__month=current_month)).aggregate(
        #     total_points=Sum('points_count'))
        # # check None if nothing is found
        # summ = result['total_points'] if result['total_points'] is not None else 0
        #
        # # check the points limit to 1 user before creating a transaction
        # if points_count + summ > 100:
        #     raise serializers.ValidationError({'error': 'You can\'t send more than 100 points per month to anyone.'})

        validated_data['sender_id'] = sender_id
        point_transaction = super().create(validated_data)
        return point_transaction
