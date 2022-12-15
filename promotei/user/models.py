from django.db import models
from document.models import IdentityNumber
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail

# Create your models here.
class AbstractUser(AbstractBaseUser, PermissionsMixin):
        class UserRolesEnum(models.TextChoices):
                NEW_USER = 'NEW_USER',
                ADMIN = 'ADMIN',
                SUPER_ADMIN = 'SUPER_ADMIN',
                USER = 'USER'
                RENTER = 'RENTER'
                RECEIVER = 'RECEIVER'
        
        username_validator = UnicodeUsernameValidator()

        username = models.CharField(
                ("username"),
                max_length=150,
                unique=True,
                help_text=(
                "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                ),
                validators=[username_validator],
                error_messages={
            "unique": ("A user with that username already exists."),
        },null=True)
             
        iin = models.ForeignKey(IdentityNumber, on_delete=models.CASCADE)
        password = models.CharField(max_length=100)
        phone_number = models.CharField(("phone number"), validators=[RegexValidator(regex=r"^\+?77(\d{9})$", message=("Неправильный номер телефона"))], max_length=50, unique=True,blank=True)
        first_name = models.CharField(("first name"), max_length=150, blank=True)
        last_name = models.CharField(("last name"), max_length=150, blank=True)
        email = models.EmailField(("email address"), blank=True)
        role = ArrayField(models.CharField(max_length=20, choices=UserRolesEnum.choices), default=list, blank=True)
        image = models.ImageField(upload_to='photos/', null=True, blank=True)
        date_joined = models.DateTimeField(("date joined"), default=timezone.now)
        
        is_staff = models.BooleanField(("staff status"),default=False,
                help_text=("Designates whether the user can log into this admin site."),)
        is_active = models.BooleanField(
                ("active"),
                default=True,
                help_text=("Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),)
        
        EMAIL_FIELD = "email"
        USERNAME_FIELD = "phone_number"
        REQUIRED_FIELDS = ["email", "username"]

        class Meta:
                verbose_name = ("user")
                verbose_name_plural = ("users")
                abstract = True

        def clean(self):
                super().clean()
                self.email = self.__class__.objects.normalize_email(self.email)

        def get_full_name(self):
                """
                Return the first_name plus the last_name, with a space in between.
                """
                full_name = "%s %s" % (self.first_name, self.last_name)
                return full_name.strip()

        def get_short_name(self):
                """Return the short name for the user."""
                return self.first_name

        def email_user(self, subject, message, from_email=None, **kwargs):
                """Send an email to this user."""
                send_mail(subject, message, from_email, [self.email], **kwargs)

        def has_role(self, role: UserRolesEnum):
                return role in self.roles

        def __str__(self) -> str:
                return f"{self.id} - {self.phone_number}"

class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
   

