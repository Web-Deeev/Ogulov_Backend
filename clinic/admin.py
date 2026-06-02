from django.contrib import admin

from .models import (
    CallbackLead, 
    ClinicAward,
    ClinicGallery,
    Doctor,
    DoctorGallery,
    MedicalMethod,
    MethodGallery,
    BannerSlide,
    ClinicAbout,         # 1. Импортируем модель описания
    ClinicGalleryImage,    # 2. Импортируем модель картинок галереи
)


# =========================================================================
# ИНФОРМАЦИЯ О КЛИНИКЕ И ЕЕ ГАЛЕРЕЯ (INLINE)
# =========================================================================
class ClinicGalleryImageInline(admin.TabularInline):
    """Позволяет загружать фотографии галереи прямо со страницы 'О клинике'"""
    model = ClinicGalleryImage
    extra = 4  # Сразу показываем 4 поля для загрузки (под твою сетку на фронте)
    fields = ("image", "alt_text", "order")


@admin.register(ClinicAbout)
class ClinicAboutAdmin(admin.ModelAdmin):
    list_display = ("title", "founder_name", "is_active", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("title", "founder_name")
    inlines = [ClinicGalleryImageInline]
    
    # Разделяем поля на логические блоки для удобства администрирования
    fieldsets = (
        ("Главный блок", {
            "fields": ("title", "description", "is_active")
        }),
        ("Основатель клиники", {
            "fields": ("founder_name", "founder_photo", "founder_description")
        }),
        ("Медиа контент", {
            "fields": ("video_url", "video_preview")
        }),
    )


# =========================================================================
# ГАЛЕРЕЯ КАРТИНОК ДЛЯ МЕТОДИК (INLINE)
# =========================================================================
class MethodGalleryInline(admin.TabularInline):
    model = MethodGallery
    extra = 3  
    fields = ("image",)


@admin.register(MedicalMethod)
class MedicalMethodAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MethodGalleryInline]


# =========================================================================
# ГАЛЕРЕЯ КАРТИНОК ДЛЯ ДОКТОРОВ (INLINE)
# =========================================================================
class DoctorGalleryInline(admin.TabularInline):
    model = DoctorGallery
    extra = 3
    fields = ("image",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "exp", "slug")
    search_fields = ("name",)
    list_filter = ("exp",)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("methods",)  
    inlines = [DoctorGalleryInline]


# =========================================================================
# НАГРАДЫ И ЛИЦЕНЗИИ КЛИНИКИ
# =========================================================================
@admin.register(ClinicAward)
class ClinicAwardAdmin(admin.ModelAdmin):
    list_display = ("title", "award_type", "created_at")
    list_filter = ("award_type", "created_at")
    search_fields = ("title",)


# =========================================================================
# ОБЩАЯ ГАЛЕРЕЯ ФОТО КЛИНИКИ ("О КЛИНИКЕ")
# =========================================================================
@admin.register(ClinicGallery)
class ClinicGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)


@admin.register(BannerSlide)
class BannerSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


# =========================================================================
# ИНТЕРФЕЙС УПРАВЛЕНИЯ ЗАЯВКАМИ ПАЦИЕНТОВ (CALLBACK LEADS)
# =========================================================================
@admin.register(CallbackLead)
class CallbackLeadAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "phone", 
        "target_type", 
        "is_processed", 
        "created_at"
    )
    list_editable = ("is_processed",)
    list_filter = ("is_processed", "target_type", "created_at")
    search_fields = ("name", "phone", "comment")
    readonly_fields = ("created_at",)
