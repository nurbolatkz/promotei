from django.db import models
import hashlib

# Create your models here.
class IdentityNumber(models.Model):
    indentity_number = models.CharField(max_length=12, unique=True)
    date_of_birth = models.DateField(null=True)
    first_name =  models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)

class Esp(models.Model):
    indentity_number = models.ForeignKey(IdentityNumber,on_delete=models.CASCADE)
    esp = models.FileField()
    hash = models.CharField(default=None, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        md5 = hashlib.md5()
        content = bytes(self.esp.read())
        md5.update(content)
        self.hash =  md5.hexdigest()
        super(Esp, self).save(*args, **kwargs)
