from rest_framework import serializers
from toy_shop.models import Cart, CartItem, Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'created_at', 'updated_at', 'items']


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = (
            'name', 'brand', 'category', 'article',
            'description_short', 'description_full',
            'price', 'old_price', 'stock', 'age_min',
            'age_max', 'material', 'dimensions', 'weight',
            'rating', 'created_at'
        )
