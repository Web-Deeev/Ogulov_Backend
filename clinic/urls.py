from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet, 
    MedicalMethodViewSet, 
    ClinicAwardViewSet , 
    ClinicGalleryViewSet, 
    CallbackLeadCreateViewSet,
    BannerSlideViewSet,
    ClinicAboutView,
)


router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'methods', MedicalMethodViewSet, basename='method')
router.register(r'awards', ClinicAwardViewSet, basename='award')
router.register(r'clinic-gallery', ClinicGalleryViewSet, basename='clinic-gallery')
router.register(r'leads', CallbackLeadCreateViewSet, basename='lead') 
router.register(r'banner', BannerSlideViewSet, basename='clinic-banner')

urlpatterns = [
    path('clinic-info/', ClinicAboutView.as_view(), name='clinic-info'),
    path('', include(router.urls)),
]
