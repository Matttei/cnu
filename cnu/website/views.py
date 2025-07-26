import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import AnuntForm
from .models import Events, ContactForm, Anunt
# Create your views here.

def index(request):
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    all_events = Events.objects.all()
    latest_events = []
    all_pinned = Anunt.objects.filter(Important=True).order_by('-data_publicare')[:3]
    if (len(all_pinned) == 3):
        latest_events = []
    else:
        latest_events = Events.objects.filter(startDateTime__gte=seven_days_ago)[:3]  
    return render(request, 'cnu/index.html', {
        'all_pinned': all_pinned,
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

        ContactForm.objects.create(name=name, email=email, message=message)

        # Compose email
        subject = f"Mesaj nou de la {name}"
        body = f"""
        Ai primit un mesaj nou de pe formularul de contact.

        📧 Email: {email}
        📝 Mesaj:{message}
        """
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,           # from email
            ['mateidorcea@gmail.com'],          # to email (cnunirea.licee@yahoo.com)
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': 'Mesajul a fost trimis, o să vă contactăm în cel mai scurt timp posibil! ✅'})

    return JsonResponse({'error': 'Metodă neacceptată.'}, status=400)

def orar(request):
    clase = []
    litere = ['IX', 'X', 'XI', 'XII']
    for an in litere:
        for litera in ['A', 'B', 'C', 'D', 'E']:
            clase.append({
                'value': f"{an}{litera}",
                'label': f"Clasa a {an}-a {litera}"
            })
    return render(request, 'cnu/orar.html', {'clase': clase})



def custom_404_view(request, exception):
    return render(request, 'cnu/404.html', status=404)


@login_required
def admin_cnu(request):
    if request.method == 'POST':
        form = AnuntForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/?success=1')
    else:
        form = AnuntForm()
    pinned_things = Anunt.objects.filter(Important=True)
    return render(request, 'cnu/admin.html', {
        'form': form,
        'pinned': pinned_things
        })


def publicatii(request):
    # For now the news will be only the annouces 
    all_news = Anunt.objects.all().order_by('-data_publicare')
    p = Paginator(all_news, 9)
    page_number = int(request.GET.get('page', 1))
    page_obj = p.get_page(page_number)
    return render(request, 'cnu/publicatii.html', {
        'news': page_obj,
    })

def noutati(request):
    noutati = Anunt.objects.filter(categorie__nume='Noutati').order_by('-data_publicare')
    return render(request, 'cnu/noutati.html',{
        'noutati': noutati
    })


def activitati(request):
    activitati = Anunt.objects.filter(categorie__nume='Activități').order_by('-data_publicare')
    return render(request, 'cnu/activitati.html',{
        'activitati': activitati
    })
def proiecte(request):
    proiecte = Anunt.objects.filter(categorie__nume='Proiecte').order_by('-data_publicare')
    return render(request, 'cnu/proiecte.html',{
        'proiecte': proiecte
    })

@login_required
def unpin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event = Anunt.objects.get(pk=data.get('id'))
            user = request.user
            if event.Important:
                event.Important = False
                event.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Actiune realizata cu succes!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Acest anunt nu era Pinned!'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.',
    }, status=405)
            


def publicatie(request, publicatie_id):
    publicatie = Anunt.objects.get(pk=publicatie_id)
    publicatie.views += 1
    publicatie.save()
    return render(request, 'cnu/publicatie.html', {
        'publicatie': publicatie,
    })


def bacalaureat(request):
    return render(request, 'cnu/bacalaureat.html')


def personal_didactic(request):
    categories = [
        ('Limba și literatura română', ['Prof. Mariana Adelina ELS', 'Prof. Elena Daniela NICA', 'Prof. Elena ȘERBĂNESCU', 'Prof. Monica CRISTEA']),
        ('Limba engleză', ['Prof. Crina Ionela DORCEA', 'Prof. Daniela Sonia PLOCON', 'Prof. Răzvan Delcea VASILE']),
        ('Limba franceză', ['Prof. Andreea Cristina BĂLAȘA', 'Prof. Mircea TATARICI', 'Prof. Geanina Petruța SAVA']),
        ('Matematică', ['Prof. Florin ORIȚĂ', 'Prof. Irina PETREANU', 'Prof. Mariana TUDOR', 'Prof. Rodica Argentina IONESCU']),
        ('Fizică', ['Prof. Mihai CĂLIN', 'Prof. Marinela DIEACONU']),
        ('Chimie', ['Prof. Ioan Fernand CARAGEA', 'Prof. Nicoleta Claudia DRĂGULEASA']),
        ('Biologie', ['Prof. Daniela GRASU', 'Prof. Mihaela NEACȘU']),
        ('Istorie', ['Prof. Vasile MĂRCUȘU', 'Prof. Ștefănel VIPIE', 'Prof. Ramona Elena STĂNESCU']),
        ('Geografie', ['Prof. Violeta DIMA', 'Prof. Daniela Rodica VASILE']),
        ('Științe socio-umane', ['Prof. Nicolae Alin ALEXE', 'Consilier Georgeta FUNARU']),
        ('Educație vizuală', ['Prof. Ovidiu Nicolae ORBEȘTEANU']),
        ('Educație fizică și sport', ['Prof. Mădălin BARBU']),
        ('Informatică și TIC', ['Prof. Miruna GRUIA', 'Prof. Nicoleta MARINESCU', 'Prof. Gabriel DEFTA']),
        ('Religie', ['Prof. Constantin COJOACĂ', 'Prof. Constantin COJOACĂ']),
    ]
    return render(request, 'cnu/personal_didactic.html', {
        'categories': categories,
    })

def personal_auxiliar(request):
    return render(request, 'cnu/personal_auxiliar.html')