from rest_framework import viewsets
from .models import Doctor, MedicalMethod
from .serializers import DoctorSerializer, MedicalMethodSerializer

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка врачей и детальной информации.
    """
    # prefetch_related оптимизирует SQL-запросы, подтягивая связанные методики
    queryset = Doctor.objects.all().prefetch_related('methods')
    serializer_class = DoctorSerializer
    lookup_field = 'slug'


class MedicalMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API эндпоинт для просмотра списка методик и детальной страницы методики.
    """
    # ИСПРАВЛЕНО: Добавлен prefetch_related('gallery'), чтобы Django отдавал массив картинок из инлайна
    queryset = MedicalMethod.objects.all().prefetch_related('gallery')
    serializer_class = MedicalMethodSerializer
    lookup_field = 'slug'
