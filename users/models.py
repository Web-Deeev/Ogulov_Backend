from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Кастомная модель пользователя для клиники Огулова.
    Наследуем AbstractUser, чтобы сохранить встроенные механизмы Django (хэширование паролей, права),
    но добавляем уникальный номер телефона как главный идентификатор.
    """
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+996XXXXXXXXX' или '+7XXXXXXXXXX'."
    )

    phone = models.CharField(
        validators=[phone_validator], 
        max_length=17, 
        unique=True, 
        verbose_name="Телефон",
        null=True, 
        blank=True
    )
    
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        # Чтобы в админке клиники менеджеры сразу видели ФИО и телефон
        full_name = self.get_full_name()
        return f"{full_name if full_name else self.username} ({self.phone or 'Нет телефона'})"
