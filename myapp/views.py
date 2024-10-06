from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Farm, Animal

# Create your views here.

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    return render(request, 'tables.html')

def billing(request):
    return render(request, 'billing.html')

def virtual_reality(request):
    return render(request, 'virtual-reality.html')

def rtl(request):
    return render(request, 'rtl.html')

def notifications(request):
    return render(request, 'notifications.html')

def profile(request):
    return render(request, 'profile.html')

def sign_in(request):
    return render(request, 'sign-in.html')

def sign_up(request):
    return render(request, 'sign-up.html')


def farm_details(request):
    farms = Farm.objects.all()  # Get all farms for the dropdown
    farm = None
    cows = None
    cow_details = None
    cow_id = None

    if request.method == 'GET':
        farm_id = request.GET.get('farm_id', None)
        cow_id = request.GET.get('cow_id', None)
        
        if farm_id:
            farm = get_object_or_404(Farm, id=farm_id)
            cows = Animal.objects.filter(farm=farm)
        
        if cow_id:
            cow_details = get_object_or_404(Animal, cow_id=cow_id)

    return render(request, 'farm_details.html', {
        'farms': farms,
        'farm': farm,
        'cows': cows,
        'cow_details': cow_details,
        'cow_id': cow_id
    })
