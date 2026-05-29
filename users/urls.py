from django.urls import path
from .views import UserProfileView, ChangePasswordView, UserLoginView
from rest_framework_simplejwt.views import TokenRefreshView 

urlpatterns = [
    
    path('profile/', UserProfileView.as_view(), name='user-profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    
    
    path('login/', UserLoginView.as_view(), name='user-custom-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
