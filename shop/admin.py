from django.contrib import admin
from django.utils.safestring import mark_safe
from django.apps import apps
from shop.models import Category, Product, ProductImage, Order, OrderItem


# Безопасно достаем модели из ядра Django, чтобы избежать сбоев импорта
Category = apps.get_model('shop', 'Category')
Product = apps.get_model('shop', 'Product')
ProductImage = apps.get_model('shop', 'ProductImage')


# Настраиваем inline-вывод галереи картинок прямо внутри карточки товара
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество пустых слотов для загрузки доп. фото по умолчанию
    fields = ['image', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" style="border-radius: 5px;" />')
        return "Нет фото"
    preview.short_description = "Превью"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Что отображать в таблице категорий
    list_display = ['id', 'title', 'slug', 'parent']
    # По каким полям можно кликнуть, чтобы войти в редактирование
    list_display_links = ['id', 'title']
    # Поиск по названию и slug
    search_fields = ['title', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Отображаем товары в админке красивой таблицей с миниатюрой фото
    list_display = ['id', 'title', 'category', 'price', 'in_stock', 'is_hit', 'is_new', 'img_preview']
    list_display_links = ['id', 'title']
    # Фильтры в правой панели админки
    list_filter = ['category', 'in_stock', 'is_hit', 'is_new']
    # Поиск по названию и текстовому ID фронтенда
    search_fields = ['title', 'slug_id']
    # Подключаем галерею картинок прямо внутрь карточки товара
    inlines = [ProductImageInline]
    
    
    prepopulated_fields = {'slug_id': ('title',)}


    def img_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" style="border-radius: 4px;" />')
        return "Нет фото"
    img_preview.short_description = "Фото"


class OrderItemInline(admin.TabularInline):
    """
    Выводит список купленных товаров прямо внутрь карточки заказа.
    Менеджер клиники сразу видит, что именно купили.
    """
    model = OrderItem
    extra = 0  # Нам не нужно добавлять пустые строки товаров вручную
    # Запрещаем менять товары и цену уже оформленного заказа, чтобы не ломать фин. отчетность
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False  


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Колонки в общем списке заказов
    list_display = ('id', 'status', 'name', 'phone', 'has_user', 'created_at')
    list_display_links = ('id', 'name')
    # Удобные фильтры справа для обработки новых заявок
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'name', 'phone')
    inlines = [OrderItemInline]

    # Красивый boolean-индикатор (зеленая галочка/красный крестик) в общей таблице
    @admin.display(boolean=True, description="Из личного кабинета?")
    def has_user(self, obj):
        return obj.user is not None