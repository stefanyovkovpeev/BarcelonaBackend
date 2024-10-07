from django.urls import path
from .views import CustomTokenObtainPairView,RegisterUserView,UserProfileView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
]