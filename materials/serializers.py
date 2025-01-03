from rest_framework import serializers
from .models import Material, Order, OrderItem

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['material', 'quantity', 'price', 'discount', 'discount_type']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','status', 'created_at', 'total_price', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.calculate_total_price()
        return order

