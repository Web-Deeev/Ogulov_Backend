from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, MedicalMethodViewSet, ClinicAwardViewSet , ClinicGalleryViewSet

# Инициализируем роутер DRF
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'methods', MedicalMethodViewSet, basename='method')
router.register(r'awards', ClinicAwardViewSet, basename='award')
router.register(r'clinic-gallery', ClinicGalleryViewSet, basename='clinic-gallery')

urlpatterns = [
    path('', include(router.urls)),
]
