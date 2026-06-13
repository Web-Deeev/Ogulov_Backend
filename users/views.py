from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from .serializers import UserProfileSerializer, ChangePasswordSerializer

User = get_user_model()

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        data = request.data
        raw_phone = data.get('username') or data.get('phone')
        password = data.get('password')

        if not raw_phone or not password:
            return Response({"detail": "Введите номер телефона и пароль!"}, status=status.HTTP_400_BAD_REQUEST)

        username = "".join(c for c in str(raw_phone) if c.isalnum()).lower()

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone": getattr(user, 'phone', '')
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Неверный пароль. Попробуйте еще раз."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь с таким номером телефона не найден."}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    # Строгая авторизация. Битые/отсутствующие токены DRF сам отсечет со статусом 401
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        current_user = request.user
        
        # Инициализируем сериализатор с контекстом
        serializer = UserProfileSerializer(current_user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Сохраняем данные. Любая ошибка СУБД (длина строки, ограничения) падает в 400 Bad Request
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {"detail": f"Ошибка базы данных при сохранении профиля: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Перевыпускаем JWT-токены, чтобы у фронтенда не протухала сессия после апдейта
        refresh = RefreshToken.for_user(current_user)
        
        return Response({
            "detail": "Профиль успешно обновлен!",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": serializer.data
        }, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
