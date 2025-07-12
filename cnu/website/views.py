from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'cnu/index.html')


def calendar(request):
    return render(request, 'cnu/calendar.html')