from django.db import models

class MedicalMethod(models.Model):
    slug = models.SlugField(unique=True, max_length=255, verbose_name="SEO Slug методики")
    title = models.CharField(max_length=255, verbose_name="Название методики")
    image = models.ImageField(upload_to='methods/', verbose_name="Изображение для карточки методики")
    short_desc = models.TextField(verbose_name="Краткое описание")
    full_desc = models.TextField(verbose_name="Полное описание для страницы методики", blank=True, null=True)

    class Meta:
        verbose_name = "Методика"
        verbose_name_plural = "Методики"

    def __str__(self):
        return self.title


# ИСПРАВЛЕНО: Модель вынесена из класса Meta на корневой уровень файла
class MethodGallery(models.Model):
    method = models.ForeignKey(
        MedicalMethod, 
        on_delete=models.CASCADE, 
        related_name="gallery", 
        verbose_name="Методика"
    )
    image = models.ImageField(upload_to='methods/gallery/', verbose_name="Дополнительное фото")

    class Meta:
        verbose_name = "Фотография галереи"
        verbose_name_plural = "Галерея картинок методики"

    # ИСПРАВЛЕНО: Метод __str__ теперь корректно возвращает информацию о фото методики
    def __str__(self):
        return f"Фото для методики: {self.method.title}"


class Doctor(models.Model):
    slug = models.SlugField(unique=True, max_length=255, verbose_name="SEO Slug врача")
    name = models.CharField(max_length=255, verbose_name="ФИО Врача")
    exp = models.CharField(max_length=50, verbose_name="Стаж работы")
    desc = models.TextField(verbose_name="Короткое интро для карточки")
    full_bio = models.TextField(verbose_name="Развернутая биография")
    image = models.ImageField(upload_to='doctors/', verbose_name="Фотография")
    video_url = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID видео YouTube")
    
    # Связь с методиками
    methods = models.ManyToManyField(MedicalMethod, related_name="doctors", verbose_name="Практикуемые методики", blank=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ['id'] 

    def __str__(self):
        return self.name
