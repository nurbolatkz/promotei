from rest_framework import serializers
from message.models import Message
from user.serializers import UserProrfileShortInfoSerializer
from contract.serializers import ContractSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProrfileShortInfoSerializer(read_only=True)
    #receiver = UserProrfileShortInfoSerializer(read_only=True)
    contract = ContractSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'contract',
            'is_read',
            'msg_content',
            'created_at', 
            'is_archived'
        ]