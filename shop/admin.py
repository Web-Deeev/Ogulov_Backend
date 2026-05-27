from django.contrib import admin
from django.utils.safestring import mark_safe
from django.apps import apps

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

    def img_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" style="border-radius: 4px;" />')
        return "Нет фото"
    img_preview.short_description = "Фото"
