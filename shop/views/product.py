from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # 🟢 ДОБАВЛЕНО: Права открытого доступа для гостей
from django.db.models import Q
from shop.models import Category, Product  # Модульный импорт из пакета моделей
from shop.serializers import CategorySerializer, ProductSerializer  # Модульный импорт из пакета сериализаторов


# 1. Представление для категорий
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  # Указываем напрямую вместо get_serializer_class

    # 🟢 ИСПРАВЛЕНО: Открываем дерево категорий для гостей без авторизации
    def get_permissions(self):
        return [AllowAny()]


# 2. Представление для товаров
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # Добавляем СРАЗУ И prefetch_related И select_related
    queryset = Product.objects.all().select_related('category').prefetch_related('additional_images')
    serializer_class = ProductSerializer
    
    # Железобетонный фикс деталки: поиск индивидуального товара по строковому slug_id!
    lookup_field = 'slug_id'

    # 🟢 ИСПРАВЛЕНО: Открываем витрину товаров для гостей без авторизации
    def get_permissions(self):
        return [AllowAny()]

    def get_queryset(self):
        # 🎯 Сеньор-оптимизация: берем уже оптимизированный базовый кверисет (с джоинами)
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            # Умный фильтр DRF: подтягивает товары категории и её подкатегорий
            queryset = queryset.filter(
                Q(category__slug=category_slug) | 
                Q(category__parent__slug=category_slug)
            )
        return queryset
