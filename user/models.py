from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .utils import *
from .managers import CustomUserManager



class BaseModel(models.Model):
    """abstract base model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class CustomUser(AbstractUser):
    email = LowercaseEmailField(unique=True)
    dialing_code = models.CharField(
        _('Country Dialing Code'),
        default = "+91",
        max_length=10)
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=20,
        validators = [phone_validator],
        null=True, blank=True
    )
    password = models.CharField(
        _("Password"), max_length=128, validators=[password_validator]
    )
    name = models.CharField(
        _("Full Name"), max_length=100, validators=[name_validator]
    )
    otp = models.CharField(max_length=8, null=True, blank=True)
    image = models.ImageField(
        default="default.png",
        upload_to="user/image/",
        verbose_name="User Profile Image",
    )
    login_method = models.CharField(
        verbose_name="Login Throgh",
        max_length=10,
        choices=[
            ("SITE", "SITE"),
            ("FACEBOOK", "FACEBOOK"),
            ("GOOGLE", "GOOGLE")
        ],
        default="SITE"
    )
    social_id = models.CharField(
        max_length=100,
        verbose_name="User Facebook/Google Id",
        null=True, blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('name',)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.name)+" - "+str(self.mobile_number)
   
    def save(self, *args, **kwargs):
        """ This method is used to modify the password field
        converting text into hashed key"""
        if len(self.password) < 30:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    @property
    def mobile(self):
        if self.mobile_number:
            return "{}-{}".format(self.dialing_code, self.mobile_number)
        return ""



""" Country Code model. """
class CountryCode(models.Model):
    name = models.CharField(_('Country Name'), max_length=150 ,unique=True)
    dialing_code = models.CharField(_('Country Dialing Code'), max_length=10)
    country_code = models.CharField(_('Country Short Code'), max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} --> {self.dialing_code}"
