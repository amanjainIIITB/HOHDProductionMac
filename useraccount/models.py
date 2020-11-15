# /Users/ajain00/Desktop/self/27-sep-2020-HOHDProductionMac/HOHDProductionMac/useraccount/Loinform.py


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError('The given phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.phone

    def get_phone_number(self):
        return self.phone

class OwnerRegistration(models.Model):
    phone = models.CharField(max_length=15, null=True)
    ownerID = models.CharField(max_length=10, null=True)
    Name = models.CharField(max_length=50, null=True)
    shop_list = models.TextField(null=True, blank='', default='')

    def __str__(self):
        return str(self.ownerID)

    def get_username(self):
        return self.phone

    def get_name(self):
        return self.Name

    def get_ownerID(self):
        return self.ownerID

    def get_contact_number(self):
        return self.phone

    def get_shop_list(self):
        return self.shop_list

class Access(models.Model):
    regID = models.CharField(max_length=10, null=True)
    shopID = models.CharField(max_length=10, null=True)
    isowner = models.BooleanField(default=False)
    page_list = models.TextField(null=True, blank='', default='')

    def __str__(self):
        return str(self.regID) + " " + str(self.shopID)