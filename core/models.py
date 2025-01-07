from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from core.choices import UserTypeChoices, OtpType, BloodGroups, UserGender
from core.managers import CustomUserManager

from shared.base_model import BaseModel

# from versatileimagefield.fields import VersatileImageField


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Users model in the System"""

    email = models.EmailField(
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.LEARNER
    )

    # Add the email field as the USERNAME_FIELD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    # Define the custom user manager
    objects = CustomUserManager()

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"

    def __str__(self):
        return self.email

    def is_activated(self):
        # Check user is activated by otp
        try:
            return self.userotp.is_activated
        except UserOtp.DoesNotExist:
            return False


def default_profile_photo():
    return "images/profile/default_profile.jpg"


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=UserGender.choices, null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=10, choices=BloodGroups.choices, null=True, blank=True
    )
    bio = models.TextField(null=True, blank=True)
    # photo = VersatileImageField(
    #     "profile_image", upload_to="images/profile/", default=default_profile_photo
    # )
    full_address = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=12, decimal_places=8, null=True, blank=True
    )
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    linkedin_link = models.CharField(max_length=255, null=True, blank=True)
    github_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"user- {self.user.get_username()}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profile"


class UserOtp(BaseModel):
    """Otp model for user otp verifations"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    otp_type = models.CharField(
        max_length=20,
        choices=OtpType.choices,
        default=OtpType.UNDEFINED,
    )
    otp = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
    )
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"user : {self.user.get_username()} , otp : {self.otp}, activated : {self.is_activated}"

    def is_expired(self):
        # Calculate the expiration time (5 minutes from the last update)
        expiration_time = self.updated_at + timezone.timedelta(minutes=5)

        # Compare the current time with the calculated expiration time
        current_time = timezone.now()
        return current_time > expiration_time

    class Meta:
        verbose_name = "User Otp"
        verbose_name_plural = "Users Otp"
