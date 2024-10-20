from django.urls import path
from .views import CustomTokenObtainPairView,RegisterUserView,UserProfileView,profile_view,VisitView,WeatherView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/upload/<int:user_id>/', profile_view, name='upload_photo'),
     path('api/profile/profilevisits/<int:user_id>/', VisitView.as_view(), name='visit-list-create'),
     path('api/weather/', WeatherView.as_view(), name='weather'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
