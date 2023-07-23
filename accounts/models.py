# --------------------------------------------------------------------------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self, mobile, password, **extra_fields):
        
        if not mobile:
            raise ValueError(_("The Mobile must be set"))
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(mobile, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    image = models.ImageField(
        default='user_avatar/default_avatar.png',
        upload_to='user_avatar/%Y%m%d'
    ) 
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    mobile = models.CharField(
        max_length=50,
        unique=True
    )

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.username:
            return self.username
        elif self.mobile:
            return self.mobile
        else:
            return self.email