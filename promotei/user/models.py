from django.db import models
from document.models import IdentityNumber
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, phone_number, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not phone_number:
            raise ValueError(_('Users must have a phone_number'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          phone_number= phone_number,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, phone_number,**extra_fields)
    
    
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_("phone number"), validators=[RegexValidator(regex=r"^\+?77(\d{9})$", message=("Неправильный номер телефона"))], max_length=50, unique=True,blank=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_secure = models.BooleanField(_("secure"), default=False)
    is_superuser = models.BooleanField(default=False)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", 'password']
    
    objects = CustomUserManager()
   
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    class UserRolesEnum(models.TextChoices):
        RENTER = 'RENTER'
        RENT_RECEIVER = 'RENT_RECEIVER'
        
    
    class GenderChoices(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        
        
    user = models.OneToOneField(CustomUser, related_name='profile',unique=True, on_delete=models.CASCADE)
    indentity_number = models.ForeignKey(IdentityNumber, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    role = models.CharField(max_length=30, choices=UserRolesEnum.choices, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    
    