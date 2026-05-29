from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from shop.models import Order
from shop.serializers.order import OrderCreateSerializer, OrderHistorySerializer

class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        # Оформить заказ (POST) может любой гость без токена
        if self.action == 'create':
            return [AllowAny()]
        # Посмотреть историю (GET) — только авторизованный клиент по JWT
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderHistorySerializer

    def perform_create(self, serializer):
        # Автоматическая привязка заказа к юзеру, если он залогинен
        if self.request.user and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def get_queryset(self):
        # База данных SQLite отдает заказы только текущего пользователя
        user = self.request.user
        if not user or not user.is_authenticated:
            return Order.objects.none()
            
        return Order.objects.filter(user=user).prefetch_related('items__product')
