from django.db import models
from django.contrib.auth.models import AbstractUser

# 🛡️ ИСПРАВЛЕНО: Полностью удален импорт UserAdmin, который валил сборку
# Все кастомные поля клиники Огулова объявлены здесь напрямую в БД

class User(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес доставки")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
