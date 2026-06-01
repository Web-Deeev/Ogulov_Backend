from django.contrib import admin

from .models import (
    CallbackLead,  # ИСПРАВЛЕНО: Добавлен импорт новой модели лидов
    ClinicAward,
    ClinicGallery,
    Doctor,
    DoctorGallery,
    MedicalMethod,
    MethodGallery,
)


# =========================================================================
# ГАЛЕРЕЯ КАРТИНОК ДЛЯ МЕТОДИК (INLINE)
# =========================================================================
class MethodGalleryInline(admin.TabularInline):
    model = MethodGallery
    extra = 3  # Сколько пустых полей для загрузки фото показывать по умолчанию
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
    filter_horizontal = ("methods",)  # Удобный UI для выбора связей ManyToMany
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


# =========================================================================
# ИНТЕРФЕЙС УПРАВЛЕНИЯ ЗАЯВКАМИ ПАЦИЕНТОВ (CALLBACK LEADS)
# =========================================================================
@admin.register(CallbackLead)
class CallbackLeadAdmin(admin.ModelAdmin):
    # Поля, которые администратор видит сразу в таблице
    list_display = (
        "name", 
        "phone", 
        "target_type", 
        "is_processed", 
        "created_at"
    )
    
    # Клик по чекбоксу "Обработано" доступен прямо из общего списка без захода внутрь
    list_editable = ("is_processed",)
    
    # Быстрые фильтры в правой панели админки
    list_filter = ("is_processed", "target_type", "created_at")
    
    # Живой поиск по ключевым данным пациента
    search_fields = ("name", "phone", "comment")
    
    # Защита данных: администратор может читать заявку, но дата создания фиксируется базой
    readonly_fields = ("created_at",)
