from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
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
    



class ContactForm(models.Model):
    name = models.CharField(max_length=256)
    message = models.TextField(blank=False)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} a trimis un mesaj la {self.created_at.strftime('%H:%M:%S')}"


class Categorie(models.Model):
    nume = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nume

class Anunt(models.Model):
    STATUS_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
    titlu = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='public', choices=STATUS_CHOICES)
    username = models.CharField(max_length=64)
    Important = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    continut = RichTextUploadingField()
    data_publicare = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.titlu} - ID: {self.id}, incarcat de: {self.username}"