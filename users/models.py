from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = str(self.email.split('@')[0])
        super(User, self).save(*args, **kwargs)


class PasswordReset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
