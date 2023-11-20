from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.desc = validated_data.get('desc', instance.desc)
    #     instance.amount = validated_data.get('amount', instance.amount)
    #     instance.save()
    #     return instance
    #
    # def delete(self, instance):
    #     instance.delete()
