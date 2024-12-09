from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from apps.accounts.managers import CustomUserManager

from apps.common.models import IsDeletedModel
from core import settings

ACCOUNT_TYPE_CHOICES = (
    ("SELLER", "SELLER"),
    ("BUYER", "BUYER"),
)


class User(AbstractBaseUser, IsDeletedModel):
    """
    Custom user model extending AbstractBaseUser.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user, used as the username field.
        avatar (ImageField): The avatar image of the user.
        is_staff (bool): Designates whether the user can log into this admin site.
        is_active (bool): Designates whether this user should be treated as active.
        account_type (str): The type of account (SELLER or BUYER).

    Methods:
        full_name(): Returns the full name of the user.
        __str__(): Returns the string representation of the user.

    """

    first_name = models.CharField(verbose_name="First name", max_length=25, null=True)
    last_name = models.CharField(verbose_name="Last name", max_length=25, null=True)
    email = models.EmailField(verbose_name="Email address", unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, default=settings.DEFAULT_AVATAR_URL)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=6, choices=ACCOUNT_TYPE_CHOICES, default="BUYER")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def full_name(self):
        """
        Returns the full name of the user by combining the first name and last name.

        Returns:
            str: The full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Returns the string representation of the user, which is their full name.

        Returns:ч
            str: The full name of the user.
        """
        return self.full_name
