from django.db import models

# Create your models here.
from django.db import models
from user.models import CustomUser


# Create your models here.
class StatusChoices(models.TextChoices):
        SENDED = "SENDED"
        RECEIVED = "RECEIVED"
        ACCEPTED = "ACCEPTED"
        DECLINED = "DECLINED"
        CREATED = "CREATED"


class Contract(models.Model):
    renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='renter')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, null=True, blank=True, default='CREATED')
    is_signed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.FileField()

