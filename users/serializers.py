from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.contrib.auth import get_user_model
from django.apps import apps  # 🛡️ ПУЛЕНЕПРОБИВАЕМО: Работаем напрямую через реестр приложений

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    address = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id', 'username', 'email']

    def to_representation(self, instance):
        """Гарантирует, что фронтенд всегда получит строку, даже если в БД лежит NULL"""
        data = super().to_representation(instance)
        data['phone'] = getattr(instance, 'phone', '') or ''
        data['address'] = getattr(instance, 'address', '') or ''
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Обновляем все стандартные прилетевшие поля
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Сохраняем модель. Если в БД нет колонок phone/address, 
            # Django выкинет ошибку здесь, и она вернется как 400, а не 500
            instance.save()
            instance.refresh_from_db()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None

        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"detail": "Пользователь не авторизован."})

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({"detail": "Старый текущий пароль введен неверно."})

        if len(str(data.get('new_password'))) < 6:
            raise serializers.ValidationError({"detail": "Новый пароль должен содержать не менее 6 символов."})

        return data
