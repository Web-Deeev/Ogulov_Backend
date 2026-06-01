from django.db.models import Prefetch  # ИСПРАВЛЕНО: Добавлен объект для глубокого пресэмплинга
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import CallbackLead, ClinicAward, ClinicGallery, Doctor, MedicalMethod
from .serializers import (
    CallbackLeadSerializer,
    ClinicAwardSerializer,
    ClinicGallerySerializer,
    DoctorSerializer,
    MedicalMethodSerializer,
)


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
