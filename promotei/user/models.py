from django.db import models
from django.contrib.auth.models import AbstractUser
from document.models import IdentityNumber
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
    
# Create your models here.
class CustomUser(AbstractUser):
    class UserRolesEnum(models.TextChoices):
        NEW_USER = 'NEW_USER',
        ADMIN = 'ADMIN',
        SUPER_ADMIN = 'SUPER_ADMIN',
        USER = 'USER'
        RENTER = 'RENTER'
        RENT_RECEIVER = 'RENT_RECEIVER'
        
    username_validator = UnicodeUsernameValidator()
    email =  models.EmailField(unique=True, null=False)
    phone_number = models.CharField(("phone number"), validators=[RegexValidator(regex=r"^\+?77(\d{9})$", message=("Неправильный номер телефона"))], max_length=50, unique=True,blank=True)
    password = models.CharField(max_length=100)
    role = ArrayField(models.CharField(max_length=20, choices=UserRolesEnum.choices), default=list, blank=True)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", 'password']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
    user = models.OneToOneField(CustomUser, related_name='profile',unique=True, on_delete=models.CASCADE)
    indentity_number = models.ForeignKey(IdentityNumber, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    first_name =  models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    
    