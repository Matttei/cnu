from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Events, ContactForm
# Create your views here.

def index(request):
    return render(request, 'cnu/index.html')


def calendar(request):
    current_date = timezone.now()
    active_events = []
    expired_events = []
    events = Events.objects.all()
    for event in events:
        if event.endDateTime < current_date:
            expired_events.append(event)
        else:
            active_events.append(event)
    return render(request, 'cnu/calendar.html', {
        'current_date': current_date,
        'active_events': active_events,
        'expired_events': expired_events,
    })


def contact(request):
    return render(request, 'cnu/contact.html')


def despre(request):
    return render(request, 'cnu/despre.html')

def admitere(request):
    return render(request, 'cnu/admitere.html')

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        created_at = timezone.now()
        contact_form = ContactForm.objects.create(name=name, email=email, message=message, created_at=created_at)
        return JsonResponse({'success': True, 'message': 'Mesajul a fost trimis, o sa va contactam in cel mai scurt timp posibil!'})
    return render(request, 'cnu/contact.html')

