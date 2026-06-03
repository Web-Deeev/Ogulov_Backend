import os
from django.db import models

#слайдер 
class ClinicAbout(models.Model):

    title = models.CharField(max_length=200, default="О клинике")
    description = models.TextField(help_text="Основной текст описания")
    
    # Блок основателя
    founder_name = models.CharField(max_length=200, default="Огулов Александр Тимофеевич")
    founder_photo = models.ImageField(upload_to="clinic/founders/", blank=True, null=True)
    founder_description = models.TextField(help_text="Описание достижений основателя")
    
    # Медиа
    video_url = models.URLField(help_text="Ссылка на YouTube видео")
    video_preview = models.ImageField(upload_to="clinic/video/", blank=True, null=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "О клинике (Главная)"
        verbose_name_plural = "О клинике (Главная)"

    def __str__(self):
        return f"{self.title} (Обновлено: {self.updated_at.strftime('%d.%m.%Y')})"


class ClinicGalleryImage(models.Model):
    """
    Галерея изображений. Принцип OCP: можем добавлять сколько угодно фото 
    без изменения модели самой клиники.
    """
    about_clinic = models.ForeignKey(ClinicAbout, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="clinic/gallery/")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Для SEO оптимизации")
    order = models.PositiveIntegerField(default=0, db_index=True, help_text="Сортировка")

    class Meta:
        ordering = ['order']



# методики
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
    
    # поле для кастомной сортировки в слайдере
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,  
        verbose_name="Порядок в слайдере",
        help_text="Чем меньше число, тем раньше фото отобразится в слайдере"
    )

    class Meta:
        verbose_name = "Фотография галереи"
        verbose_name_plural = "Галерея картинок методики"
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"Слайд №{self.sort_order} для методики: {self.method.title}"



#Специалисты
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



#Награды
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
    


class BannerSlide(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок слайда")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Надзаголовок (подзаголовок)")
    text = models.TextField(verbose_name="Описание / Текст слайда")
    image = models.ImageField(upload_to="clinic/banners/", verbose_name="Фоновое изображение")
    button_text = models.CharField(max_length=100, default="Подробнее", verbose_name="Текст кнопки")
    link = models.CharField(max_length=255, default="/contacts", verbose_name="Ссылка для кнопки")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Слайд баннера"
        verbose_name_plural = "Слайды баннера"
        ordering = ['order']

    def __str__(self):
        return self.title

    
    

#Форма записи
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
