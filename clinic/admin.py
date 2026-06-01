from django.contrib import admin
# Импортируем все три модели
from .models import Doctor, DoctorGallery, MedicalMethod, MethodGallery, ClinicAward, ClinicGallery 

# 1. СОЗДАЕМ ИНЛАЙН-КЛАСС НАСТРОЙКИ (Django нужен именно он)
class MethodGalleryInline(admin.TabularInline):
    model = MethodGallery
    extra = 3  # Сколько пустых полей для загрузки фото показывать по умолчанию
    fields = ('image',)


@admin.register(MedicalMethod)
class MedicalMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    
    inlines = [MethodGalleryInline]


class DoctorGalleryInline(admin.TabularInline):
    model = DoctorGallery
    extra = 3
    fields = ('image',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Добавил 'role' в список отображения, чтобы видеть должность в таблице
    list_display = ('name', 'exp', 'slug')
    # Добавил 'role' в поиск, чтобы можно было искать, например, всех кардиологов
    search_fields = ('name',)
    list_filter = ('exp',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('methods',)

    inlines = [DoctorGalleryInline]
    
    
@admin.register(ClinicAward)
class ClinicAwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'award_type', 'created_at')
    list_filter = ('award_type',)
    search_fields = ('title',)


@admin.register(ClinicGallery)
class ClinicGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
