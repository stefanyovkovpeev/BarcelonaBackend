from django.urls import path
from .views import CustomTokenObtainPairView,RegisterUserView,UserProfileView,profile_view
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/upload/<int:user_id>/', profile_view, name='upload_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
