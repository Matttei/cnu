from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('contact/', views.contact, name='contact'),
    path('despre/', views.despre, name='despre'),
    path('admitere/', views.admitere, name='admitere'),
    path('contact/contact-form', views.contact_form, name='contact_form')
]