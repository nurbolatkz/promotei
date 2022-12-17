from django.db import models

# Create your models here.
class IdentityNumber(models.Model):
    indentity_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_place = models.TextField()
    

class Esp(models.Model):
    indentity_number = models.ForeignKey(IdentityNumber,on_delete=models.CASCADE)
    esp = models.FileField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField()
