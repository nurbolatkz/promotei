from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'sender',
            'receiver',
            'contact',
            'is_read',
            'msg_content',
            'created_at', 
            'is_archived'
        ]