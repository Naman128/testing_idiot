from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """
    Custom user manager that uses phone_number as the unique identifier.
    """

    def create_user(self, phone_number, name, password=None, **extra_fields):
        """
        Create and return a regular user with the given phone number and name.
        """
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            phone_number=phone_number,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, **extra_fields):
        """
        Create and return a superuser with the given phone number and name.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with phone_number as the unique identifier.
    """
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    phone_number = models.CharField(
        max_length=17,
        unique=True,
        validators=[phone_regex],
        help_text='Required. Unique phone number for authentication.',
        error_messages={
            'unique': 'A user with that phone number already exists.',
        },
    )
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
