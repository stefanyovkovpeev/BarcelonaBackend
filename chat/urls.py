from django.urls import path
from .views import MessageViewSet

urlpatterns = [
    path('api/chatbot/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list-create'),
]