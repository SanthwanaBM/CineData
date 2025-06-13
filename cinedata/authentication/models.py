from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin','Admin'

    USER = 'User','User'


class Profile(AbstractBaseUser):

    role = models.CharField(max_length=10,choices=RoleChoices.choices)

    def __str__(self):
        return self.email


    class Meta:

        verbose_name = 'profile'

        verbose_name_plural = 'profile'
            