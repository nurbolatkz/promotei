from django.db import models
from user.models import UserProfile
from contract.models import Contract

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='message_receiver')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='message_contract')
    msg_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
       get_latest_by = '-created_at'