from django.db import models

# Create your models here.
from django.db import models
from document.models import IdentityNumber


# Create your models here.
class StatusChoices(models.TextChoices):
        SENDED = 'SENDED'
        RECEIVED = 'RECEIVED'
        ACCEPTED = "ACCEPTED"


class Contract(models.Model):
    renter = models.ForeignKey(IdentityNumber, on_delete=models.CASCADE, related_name='renter')
    receiver = models.ForeignKey(IdentityNumber, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.FileField()

