from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from .catalog import Product  # Чистый импорт модели товара из соседнего файла

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+996XXXXXXXXX' или '+7XXXXXXXXXX'."
    )

    # Связь с пользователем (null=True — разрешено для гостей сайта без регистрации)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders', 
        verbose_name="Пользователь"
    )
    
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(validators=[phone_validator], max_length=17, verbose_name="Телефон")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес доставки")  # Будет пустым для заказа в 1 клик
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} — {self.name} ({self.get_status_display()})"


class OrderItem(models.Model):
    """Связующая таблица для фиксации товаров и цен на момент покупки"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена при заказе")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
