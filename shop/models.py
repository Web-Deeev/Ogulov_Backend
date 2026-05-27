from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="ID категории (Slug)")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories',
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.title} ({self.slug})"


class Product(models.Model):
    slug_id = models.SlugField(max_length=100, unique=True, verbose_name="ID товара (например, banks-1)")
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='products',
        verbose_name="Категория"
    )
    title = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущая цена (числом)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Старая цена (если есть)")
    image = models.ImageField(upload_to='product/', verbose_name="Главное изображение")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    label = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ярлык (например: Скидка, Хит)")
    description = models.TextField(blank=True, null=True, verbose_name="Описание товара")
    specs = models.TextField(blank=True, null=True, verbose_name="Характеристики товара")
    is_hit = models.BooleanField(default=False, verbose_name="Хит продаж")
    is_recommend = models.BooleanField(default=False, verbose_name="Рекомендованно") 
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='product/gallery/', verbose_name="Доп. фото")

    class Meta:
        verbose_name = "Дополнительное фото товара"
        verbose_name_plural = "Дополнительные фото товаров"
