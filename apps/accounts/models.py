from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# -------------------------------------------------
# Custom User Model
# -------------------------------------------------
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_dealer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# -------------------------------------------------
# Address Model (Consolidated Version)
# -------------------------------------------------
class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.full_name if self.full_name else self.user.username
        return f"{name} - {self.city}"
