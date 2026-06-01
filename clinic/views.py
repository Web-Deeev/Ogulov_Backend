from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Doctor, MedicalMethod, ClinicAward, ClinicGallery
from .serializers import DoctorSerializer, MedicalMethodSerializer, ClinicAwardSerializer, ClinicGallerySerializer

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Doctor.objects.all().prefetch_related('gallery', 'methods')
    serializer_class = DoctorSerializer
    lookup_field = 'slug'


class MedicalMethodViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = MedicalMethod.objects.all().prefetch_related('gallery')
    serializer_class = MedicalMethodSerializer
    lookup_field = 'slug'


class ClinicAwardViewSet(viewsets.ReadOnlyModelViewSet):
 
    queryset = ClinicAward.objects.all()
    serializer_class = ClinicAwardSerializer
    permission_classes = [AllowAny]


class ClinicGalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClinicGallery.objects.all()
    serializer_class = ClinicGallerySerializer
    permission_classes = [AllowAny]