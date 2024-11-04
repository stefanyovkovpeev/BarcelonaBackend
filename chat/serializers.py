from rest_framework import serializers
from .models import Message,ChatMessage

class BotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user','id', 'content', 'sender', 'timestamp']
        
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['user','id', 'content', 'sender', 'timestamp']