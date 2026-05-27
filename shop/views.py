from rest_framework import viewsets
from django.db.models import Q
from .models import Category, Product

# 1. Представление для категорий
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        from .serializers import CategorySerializer
        return CategorySerializer


# 2. Представление для товаров
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('additional_images')
    
    # Железобетонный фикс деталки: перенаправляем поиск индивидуального 
    # товара с дефолтного поля id на твой строковый slug_id!
    lookup_field = 'slug_id'

    def get_serializer_class(self):
        from .serializers import ProductSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(
                Q(category__slug=category_slug) | 
                Q(category__parent__slug=category_slug)
            )
        return queryset
