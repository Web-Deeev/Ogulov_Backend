from rest_framework import serializers
# ИСПРАВЛЕНО: Добавлен импорт MethodGallery
from .models import Doctor, MedicalMethod, MethodGallery 


class MethodGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodGallery
        fields = ['id', 'image']


class MedicalMethodSerializer(serializers.ModelSerializer): 
    gallery = MethodGallerySerializer(many=True, read_only=True)

    class Meta:
        model = MedicalMethod
        fields = ['id', 'slug', 'title', 'image', 'short_desc', 'full_desc', 'gallery']


class DoctorSerializer(serializers.ModelSerializer):
    methods = MedicalMethodSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'slug', 'name', 'exp', 'desc', 'full_bio', 'image', 'video_url', 'methods']
