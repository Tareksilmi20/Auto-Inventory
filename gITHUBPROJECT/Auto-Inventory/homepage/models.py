from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    def create_user(self, username, useremail, password=None, **extra_fields):
        if not useremail:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(useremail)
        user = self.model(username=username, useremail=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, useremail, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, useremail, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    useremail = models.EmailField(unique=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    verification_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['useremail']

    def __str__(self):
        return self.username

    def is_email_verified(self):
        return self.verification_status