from rest_framework import serializers
from shop.models import Order, OrderItem, Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)  # Принимаем список товаров

    class Meta:
        model = Order
        fields = ['id', 'name', 'phone', 'address', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Автоматически проверяем, залогинен ли пользователь на фронтенде
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        
        # Создаем основной заказ
        order = Order.objects.create(user=user, **validated_data)
        
        # Сохраняем товары и жестко фиксируем цену из нашей БД
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price  # Защита от подмены цены на фронтенде!
            )
            
        return order
