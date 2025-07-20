from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('contact/', views.contact, name='contact'),
    path('despre/', views.despre, name='despre'),
    path('admitere/', views.admitere, name='admitere'),
    path('contact/contact-form', views.contact_form, name='contact_form'),
    path('orar/', views.orar, name='orar'),
    path('admin_cnu/', views.admin_cnu, name='cnu_admin'),
    path('publicatii/', views.publicatii, name='publicatii'),
    path('publicatii/noutati/', views.noutati, name='noutati'),
    path('publicatii/activitati', views.activitati, name='activitati'),
    path('publicatii/proiecte/', views.proiecte, name='proiecte')
]