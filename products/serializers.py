from rest_framework import serializers
from products.models import *


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = ('id', 'name')


class ShopSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    category = ShopCategorySerializer()

    class Meta:
        model = Shop
        fields = ('id', 'cover', 'name', 'category')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductReadListSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField()
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'cover', 'name', 'description', 'category', 'weight', 'start_price', 'current_price', 'amount')


class ProductReadDetailSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    category = ProductCategorySerializer()
    shop = ShopSerializer()

    class Meta:
        model = Product
        fields = ('id', 'cover', 'name', 'description', 'category', 'shop', 'calories', 'protein', 'fats', 'carbohydrates', 'weight', 'start_price', 'current_price', 'amount', 'compound', 'expiration')


class ProductWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'cover', 'name', 'description', 'category', 'shop', 'calories', 'protein', 'fats', 'carbohydrates', 'weight', 'start_price', 'current_price', 'amount', 'compound', 'expiration')