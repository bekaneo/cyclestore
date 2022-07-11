from rest_framework import serializers

from orders.models import Order, OrderItems
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'address', 'items', 'total', 'status']

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data)
        total = 0
        for item in items:
            OrderItems.objects.create(order=order, product=item['product'],
                                      quantity=item['quantity'])
            total += item['product'].price * item['quantity']
        order.total = total
        order.save()
        return order
