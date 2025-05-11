from django.db import models
from django.contrib.auth.models import AbstractUser


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=64)

    def __str__(self):
        return self.name