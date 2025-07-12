from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class Events(models.Model):
    CLASE = [
        ('toate', 'IX-XII'),
        ('cls 9', 'IX'),
        ('cls 10', 'X'),
        ('cls 11', 'XI'),
        ('cls 12', 'XII'),
    ]

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    isPinned = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    startDateTime = models.DateTimeField(null=True, blank=True)
    endDateTime = models.DateTimeField(null=True, blank=True)

    
    classes = models.CharField(max_length=20, choices=CLASE, default='toate')

    def __str__(self):
        return f"{self.title} ({self.startDateTime} - {self.endDateTime})"