from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
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
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    all_events = Events.objects.all()
    latest_events = []
    latest_events = Events.objects.filter(startDateTime__gte=seven_days_ago)[:3]  
    return render(request, 'cnu/index.html', {
        'latest_events': latest_events
    })


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
        contact_form = ContactForm.objects.create(name=name, email=email, message=message)
        return JsonResponse({'success': True, 'message': 'Mesajul a fost trimis, o să vă contactăm în cel mai scurt timp posibil! ✅'})
    return JsonResponse({'error': 'Metodă neacceptată.'}, status=400)

