from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.db import models
from .managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
ZIP_MSG = _(u'Must be valid zipcode in formats 12345 or 12345-1234')
PHONE_REGEX_MSG = _("Phone number must be entered in the format: '(999) 999-9999'. Up to 15 digits allowed")

zip_regex = RegexValidator(
    regex=r'^(^[0-9]{6}(?:-[0-9]{4})?$|^$)',
    message=ZIP_MSG
)

phone_regex = RegexValidator(
    regex=r'^\s*(?:\+?(\d{1,3}))?[- (]*(\d{3})[- )]*(\d{3})[- ]*(\d{4})(?: *[x/#]{1}(\d+))?\s*$',
    message=PHONE_REGEX_MSG
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    mobile_phone = models.CharField(max_length=12, validators=[phone_regex], null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, null=True)
    last_login = models.DateTimeField(null=True)
    address = models.CharField(default="", max_length=50, blank=True, null=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True, validators=[zip_regex], default="")
    country = models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
