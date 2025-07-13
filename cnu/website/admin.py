from django.contrib import admin
from .models import User, Events, ContactForm
# Register your models here.
admin.site.register(Events)
admin.site.register(ContactForm)
