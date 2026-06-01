import re  # ИСПРАВЛЕНО: Добавлен обязательный импорт для работы валидации телефона

from rest_framework import serializers

from .models import (
    CallbackLead,
    ClinicAward,
    ClinicGallery,
    Doctor,
    DoctorGallery,
    MedicalMethod,
    MethodGallery,
)


# 1. Сериализатор галереи картинок МЕТОДИКИ
class MethodGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodGallery
        fields = ['id', 'image']


# 2. Сериализатор МЕТОДИК
class MedicalMethodSerializer(serializers.ModelSerializer): 
    gallery = MethodGallerySerializer(many=True, read_only=True)

    class Meta:
        model = MedicalMethod
        fields = ['id', 'slug', 'title', 'image', 'short_desc', 'full_desc', 'gallery']


# 3. Сериализатор галереи картинок ВРАЧА
class DoctorGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorGallery
        fields = ['id', 'image']


# 4. ГЛАВНЫЙ СЕРИАЛИЗАТОР ВРАЧА
class DoctorSerializer(serializers.ModelSerializer):
    methods = MedicalMethodSerializer(many=True, read_only=True)
    gallery = DoctorGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'slug', 'name', 'exp', 'desc', 'full_bio', 
            'image', 'video_url', 'gallery', 'methods'
        ]


# 5. Сериализатор наград клиники
class ClinicAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAward
        fields = ['id', 'title', 'image', 'award_type']


# 6. Сериализатор общей галереи клиники
class ClinicGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicGallery
        fields = ['id', 'image', 'title']


# 7. Сериализатор лидов / заявок на прием
class CallbackLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackLead
        fields = [
            "id", 
            "name", 
            "phone", 
            "comment", 
            "target_type", 
            "target_id", 
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def validate_phone(self, value):
        """
        Очистка номера телефона от мусора и проверка длины (KISS/SOLID).
        """
        # Очищаем от скобок, пробелов и тире, оставляем только цифры
        clean_phone = re.sub(r"\D", "", value)
        
        # Защита: телефон должен содержать от 10 до 15 цифр
        if not (10 <= len(clean_phone) <= 15):
            raise serializers.ValidationError(
                "Некорректный формат номера телефона. Введите от 10 до 15 цифр."
            )
            
        return clean_phone
