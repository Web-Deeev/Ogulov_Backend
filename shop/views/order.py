from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from shop.models import Order
from shop.serializers.order import OrderCreateSerializer

class OrderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]  # Оформить заказ без регистрации может любой гость
