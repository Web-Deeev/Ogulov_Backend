from django.db.models import Prefetch  
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import (
    CallbackLead, 
    ClinicAward, 
    ClinicGallery, 
    Doctor, 
    MedicalMethod,  
    BannerSlide,
    ClinicAbout,
)

from .serializers import (
    CallbackLeadSerializer,
    ClinicAwardSerializer,
    ClinicGallerySerializer,
    DoctorSerializer,
    MedicalMethodSerializer,
    BannerSlideSerializer,
    ClinicAboutSerializer,
)



class ClinicAboutView(APIView):
    """
    Отдает только активную информацию о клинике. 
    Исключаем N+1 через prefetch_related для галереи.
    """
    def get(self, request):
        about_data = ClinicAbout.objects.filter(is_active=True).prefetch_related('gallery_images').first()
        if not about_data:
            return Response({"detail": "Контент еще не заполнен"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClinicAboutSerializer(about_data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для чтения профилей врачей.
    Оптимизирован для ликвидации N+1 запросов во вложенных связях галерей методик.
    """
    # ИСПРАВЛЕНО: Глубокий prefetch через __ подтягивает галереи ВНУТРИ методик доктора в 1 запрос
    queryset = Doctor.objects.all().prefetch_related(
        "gallery", 
        Prefetch("methods", queryset=MedicalMethod.objects.prefetch_related("gallery"))
    )
    serializer_class = DoctorSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


class MedicalMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для чтения медицинских методик клиники.
    """
    queryset = MedicalMethod.objects.all().prefetch_related("gallery")
    serializer_class = MedicalMethodSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


class ClinicAwardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра дипломов и сертификатов Огулов Центра.
    """
    queryset = ClinicAward.objects.all()
    serializer_class = ClinicAwardSerializer
    permission_classes = [AllowAny]


class BannerSlideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BannerSlide.objects.filter(is_active=True)
    serializer_class = BannerSlideSerializer
    permission_classes = [AllowAny]


class ClinicGalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра общей интерьерной галереи клиники.
    """
    queryset = ClinicGallery.objects.all()
    serializer_class = ClinicGallerySerializer
    permission_classes = [AllowAny]


class CallbackLeadCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Эндпоинт для публичной отправки заявок на приём с фронтенд-форм.
    Защищен валидацией в сериализаторе.
    """
    queryset = CallbackLead.objects.all()
    serializer_class = CallbackLeadSerializer
    permission_classes = [AllowAny]
