from rest_framework import viewsets
from .models import Message,ChatMessage
from .serializers import BotMessageSerializer,ChatMessageSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = BotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        time_threshold = timezone.now() - timezone.timedelta(days=1)
        return Message.objects.filter(user=self.request.user, timestamp__gte=time_threshold).order_by('timestamp')
    
# import logging

# logger = logging.getLogger(__name__)

class ChatMessagesViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        time_threshold = timezone.now() - timezone.timedelta(days=1)
        return ChatMessage.objects.filter(timestamp__gte=time_threshold).order_by('timestamp')

    def perform_create(self, serializer):
        instance = serializer.save()
        

        logger.info("Message saved and perform_create called with data: %s", serializer.data)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat_room",
            {
                "type": "chat_message",
                "message": serializer.data  
            }
        )
    
class ChatBotResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user_message = request.data.get("content", "")
        
        if "hello" in user_message.lower():
            bot_response = "Hello! How can I assist you today?"
        elif "bye" in user_message.lower():
            bot_response = "Goodbye! Have a great day!"
        else:
            bot_response = "I'm here to help you. Please ask me anything."
        return Response({"content": bot_response, "sender": "bot"}, status=status.HTTP_200_OK)