from django.db import models
import random
import string
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class AccessKey(models.Model):
    KEY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    
    key_value = models.CharField(max_length=16, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=KEY_STATUS_CHOICES, default='active')
    date_procured = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(editable=True)

    def __str__(self):
        return self.key_value
    
    def save(self, *args, **kwargs):
        if self.status == 'active':
            AccessKey.objects.filter(user=self.user, status='active').update(status='expired')
        if not self.key_value:
            characters = string.ascii_letters + string.digits
            key = ''.join(random.choice(characters) for _ in range(16))
            self.key_value = key
        super().save(*args, **kwargs)