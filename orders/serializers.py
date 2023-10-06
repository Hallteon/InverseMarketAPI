from rest_framework import serializers
from orders.models import *
from products.serializers import ProductReadDetailSerializer


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('id', 'name', 'status_type')


class OrderProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'amount')


class OrderProductReadSerializer(serializers.ModelSerializer):
    product = ProductReadDetailSerializer()

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'amount')


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_products', 'order_datetime', 'delivery_time', 'delivery_address', 'delivery_price', 'total_price', 'total_weight', 'fast', 'status', 'need_change')


class OrderReadSerializer(serializers.ModelSerializer):
    order_products = OrderProductReadSerializer(required=False, many=True)
    status = OrderStatusSerializer()

    class Meta:
        model = Order
        fields = ('id', 'order_products', 'order_datetime', 'delivery_time', 'delivery_address', 'delivery_price', 'total_price', 'total_weight', 'fast', 'status', 'need_change')