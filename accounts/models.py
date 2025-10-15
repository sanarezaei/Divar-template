import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone(value: str) -> None:
    if not value:
        raise ValidationError("The phone number cannot be empty!!")
    if not re.match(r"^09\d{9}$", value):
        raise ValidationError(
            "Your phone number must start with 09 and be 11 digits long."
        )


class User(AbstractUser):
    pass


class Profile(models.Model):
    CITY_CHOICES = [
        ("Tehran", "Tehran"),
        ("Kermanshah", "Kermanshah"),
        ("Mashhad", "Mashhad"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(validators=[validate_phone], max_length=11, unique=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
