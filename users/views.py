from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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
    permission_classes = [AllowAny]

    def patch(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        data = request.data

        # 🛡️ 1. ЕСЛИ ПОЛЬЗОВАТЕЛЬ АВТОРИЗОВАН — ОБНОВЛЯЕМ ЧЕРЕЗ СЕРИАЛИЗАТОР
        if request.user and request.user.is_authenticated:
            current_user = request.user
            from .serializers import UserProfileSerializer  
            serializer = UserProfileSerializer(current_user, data=data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # 🟢 ДОБАВЛЕНО: Генерируем токен, чтобы у фронтенда не ломалась сессия!
            refresh = RefreshToken.for_user(current_user)
            
            return Response({
                "detail": "Профиль успешно обновлен!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        else:
            raw_username = data.get('username') or data.get('phone') or data.get('email')
            if not raw_username:
                return Response({"detail": "Необходимо передать логин, телефон или email!"}, status=status.HTTP_400_BAD_REQUEST)

            username = "".join(c for c in str(raw_username) if c.isalnum() or c in ['.', '-', '_']).lower()
            password = data.get('password') or "OgulovClinic2026"

            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                current_user = User.objects.get(username=username)
                if data.get('password'):
                    current_user.set_password(password)
            else:
                current_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=data.get('email', '')
                )

            current_user.first_name = data.get('first_name', current_user.first_name)
            current_user.last_name = data.get('last_name', current_user.last_name)
            
            if hasattr(current_user, 'phone'):
                current_user.phone = data.get('phone', current_user.phone)
            if hasattr(current_user, 'address'):
                current_user.address = data.get('address', current_user.address)
                
            current_user.save() 
            
            refresh = RefreshToken.for_user(current_user)
            return Response({
                "detail": "Личные данные успешно сохранены в базе данных клиники!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                    "first_name": current_user.first_name,
                    "last_name": current_user.last_name,
                    "phone": getattr(current_user, 'phone', ''),
                    "address": getattr(current_user, 'address', '')
                }
            }, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from .serializers import ChangePasswordSerializer  
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
