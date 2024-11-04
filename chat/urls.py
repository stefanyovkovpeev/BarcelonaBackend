from django.urls import path
from .views import MessageViewSet, ChatBotResponseView,ChatMessagesViewSet

urlpatterns = [
    path('api/chatbot/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list-create'),
    path('api/chatbot/response/', ChatBotResponseView.as_view(), name='chatbot-response'),
    path('api/chatroom/messages/', ChatMessagesViewSet.as_view({'get': 'list','post': 'create'}), name='chatroom-get'),
    
]