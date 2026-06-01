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
    methods = models.ManyToManyField(
        MedicalMethod, 
        related_name="doctors", 
        verbose_name="Практикуемые методики", 
        blank=True
    )

    # ИСПРАВЛЕНО: Мета-класс и сортировка возвращены законному владельцу — модели Doctor
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ['id'] 

    def __str__(self):
        return self.name



class DoctorGallery(models.Model):
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name="gallery",
        verbose_name="Врач"
    )
    image = models.ImageField(upload_to='doctors/gallery/', verbose_name="Дополнительное фото")

    class Meta:
        verbose_name = "Фотография галереи врача"
        verbose_name_plural = "Галерея картинок врача"
        ordering = ['id']
  
    def __str__(self):
        try:
            if self.doctor and self.doctor.name:
                return f"Фото для врача: {self.doctor.name}"
        except (Doctor.DoesNotExist, AttributeError):
            pass
        return f"Фото в галерее (ID: {self.id or 'Новое'})"


class ClinicAward(models.Model):
    TYPE_CHOICES = [
        ('diploma', 'Диплом'),
        ('gratitude', 'Сертификаты'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Название награды/диплома")
    image = models.ImageField(upload_to='awards/', verbose_name="Скан/Фотография награды")
    award_type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='diploma', 
        verbose_name="Тип документа"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"
        ordering = ['-created_at'] # Новые награды выводятся первыми

    def __str__(self):
        return f"[{self.get_award_type_display()}] {self.title}"


class ClinicGallery(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name="Описание фото (необязательно)")
    image = models.ImageField(upload_to='clinic/gallery/', verbose_name="Фотография центра")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фотография центра"
        verbose_name_plural = "Галерея: О клинике"
        ordering = ['-created_at']

    def __str__(self):
        return self.title if self.title else f"Фото центра #{self.id}"
    
    


class CallbackLead(models.Model):
    """
    Модель для хранения заявок на прием (Лидов) с фронтенд-форм.
    """
    name = models.CharField(
        max_length=150, 
        verbose_name="Имя пациента"
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name="Номер телефона"
    )
    comment = models.TextField(
        blank=True, 
        default="", 
        verbose_name="Комментарий пациента"
    )
    
    # Поля для связи с сущностью (Врач или Методика)
    target_type = models.CharField(
        max_length=100, 
        verbose_name="Тип сущности (Врач/Методика)"
    )
    target_id = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="ID сущности"
    )
    
    # Системные поля автоматизации
    is_processed = models.BooleanField(
        default=False, 
        db_index=True, 
        verbose_name="Обработано администратором"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        db_index=True, 
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Заявка на прием"
        verbose_name_plural = "Заявки на прием"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка от {self.name} ({self.phone}) — {self.created_at.strftime('%d.%m.%Y %H:%M')}"
