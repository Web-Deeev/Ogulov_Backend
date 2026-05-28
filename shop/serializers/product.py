from rest_framework import serializers
from shop.models import Category, Product, ProductImage  # Чистый импорт без костылей!

# 1. Сериализатор для категорий товара
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'parent']


# 2. Сериализатор для картинок из галереи
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


# 3. Главный сериализатор для товаров
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    additional_images = ProductImageSerializer(many=True, read_only=True)
    formatted_price = serializers.SerializerMethodField()
    formatted_old_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'slug_id', 'title', 'price', 'old_price',
            'formatted_price', 'formatted_old_price', 'category', 
            'image', 'additional_images', 'in_stock', 'label', 
            'description', 'specs', 'is_hit', 'is_new', 'created_at'
        ]

    def get_formatted_price(self, obj):
        if obj.price is None:
            return "0 сом"
        return f"{obj.price:,.0f}".replace(",", " ") + " сом"

    def get_formatted_old_price(self, obj):
        if not obj.old_price:
            return None
        return f"{obj.old_price:,.0f}".replace(",", " ") + " сом"
