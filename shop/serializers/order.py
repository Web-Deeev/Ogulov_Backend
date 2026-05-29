from rest_framework import serializers
from django.db import transaction
from shop.models import Order, OrderItem, Product

# =========================================================================
# 1. СЛОЙ ЗАПИСИ (WRITE-ONLY) — Создание заказа (1 клик / Корзина)
# =========================================================================

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    customer_name = serializers.CharField(source='name', write_only=True)
    
    delivery_method = serializers.CharField(write_only=True, required=False, default='BISHKEK')
    delivery_address = serializers.CharField(write_only=True, required=False, default='')
    comment = serializers.CharField(write_only=True, required=False, default='')
    delivery_amount = serializers.IntegerField(write_only=True, required=False, default=0)
    total_amount = serializers.IntegerField(write_only=True, required=False, default=0)
    currency = serializers.CharField(write_only=True, required=False, default='KGS')

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'phone', 'address', 'items', 'created_at',
            'delivery_method', 'delivery_address', 'comment', 'delivery_amount', 
            'total_amount', 'currency'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        delivery_method = validated_data.pop('delivery_method', 'BISHKEK')
        delivery_address = validated_data.pop('delivery_address', '')
        comment = validated_data.pop('comment', '')
        delivery_amount = validated_data.pop('delivery_amount', 0)
        total_amount = validated_data.pop('total_amount', 0)
        
        method_title = "Самовывоз" if delivery_method == "PICKUP" else f"Доставка ({delivery_method})"
        full_address = f"[{method_title}] Адрес: {delivery_address}. Доставка: {delivery_amount} KGS. Итого: {total_amount} KGS. Комментарий: {comment}"
        
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                name=validated_data['name'],
                phone=validated_data['phone'],
                address=full_address
            )
            
            for item_data in items_data:
                product = item_data['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    price=product.price
                )
                
        return order


# =========================================================================
# 2. СЛОЙ ЧТЕНИЯ (READ-ONLY) — Вывод истории в Личном Кабинете
# =========================================================================

class OrderItemReadSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_title', 'product_image', 'quantity', 'price']


class OrderHistorySerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'status_display', 'address', 'phone', 'items', 'created_at']
