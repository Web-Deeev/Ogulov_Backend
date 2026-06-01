from rest_framework import serializers
from .models import Doctor, DoctorGallery, MedicalMethod, MethodGallery, ClinicAward, ClinicGallery 


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
        # ИСПРАВЛЕНО: Убрано лишнее поле image_personal, из-за которого сервер выдавал 500
        fields = [
            'id', 'slug', 'name', 'exp', 'desc', 'full_bio', 
            'image', 'video_url', 'gallery', 'methods'
        ]


class ClinicAwardSerializer(serializers.ModelSerializer):
    # DRF автоматически сделает пути к изображениям абсолютными (http://127.0.0...)
    class Meta:
        model = ClinicAward
        fields = ['id', 'title', 'image', 'award_type']


class ClinicGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicGallery
        fields = ['id', 'image', 'title']