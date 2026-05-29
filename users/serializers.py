from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.apps import apps  # 🛡️ ПУЛЕНЕПРОБИВАЕМО: Работаем напрямую через реестр приложений

class UserProfileSerializer(serializers.ModelSerializer):
    # Явно объявляем строковые поля для сериализации фронтенда
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    address = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        # 🟢 РАЗРЫВ ЦИКЛА 5.0+: Достаем класс модели динамически по строке.
        # Никаких get_user_model() на уровне модуля — сервер больше никогда не упадет при старте!
        model = apps.get_model('users', 'User')
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['id', 'email']

    def to_representation(self, instance):
        """
        🛡️ ПУЛЕНЕПРОБИВАЕМОЕ ЧТЕНИЕ: Забираем данные напрямую из полей кастомной 
        модели User, исключая поиск несуществующих связанных профилей.
        """
        data = super().to_representation(instance)
        data['phone'] = getattr(instance, 'phone', '') or ''
        data['address'] = getattr(instance, 'address', '') or ''
        return data

    def update(self, instance, validated_data):
        phone_data = validated_data.pop('phone', None)
        address_data = validated_data.pop('address', None)

        with transaction.atomic():
            # Собираем все поля, прилетевшие с фронта, в один payload
            update_fields = {}
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                update_fields[attr] = value
            
            if phone_data is not None:
                instance.phone = phone_data
                update_fields['phone'] = phone_data
                
            if address_data is not None:
                instance.address = address_data
                update_fields['address'] = address_data

            if update_fields:
                # Твой оптимизированный SQL UPDATE без вызова сигналов сохранения
                user_model_class = type(instance)
                user_model_class.objects.filter(id=instance.id).update(**update_fields)
            
            instance.refresh_from_db()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        # 🛡️ ЗАЩИТА 1: Безопасно извлекаем request из контекста, исключая KeyError
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Системная ошибка: отсутствует контекст запроса.")

        user = request.user
        
        # 🛡️ ЗАЩИТА 2: Проверяем, авторизован ли пользователь, исключая AttributeError
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Сессия устарела. Пожалуйста, авторизуйтесь заново.")

        # 🛡️ ЗАЩИТА 3: Проверяем сам старый пароль
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль введен неверно.")
            
        return value