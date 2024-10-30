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



# def farm_details(request):
#     farms = Farm.objects.all()  # Get all farms for the dropdown
#     farm = None
#     cows = None
#     cow_details = None
#     cow_id = None

#     if request.method == 'GET':
#         farm_id = request.GET.get('farm_id', None)
#         cow_id = request.GET.get('cow_id', None)
        
#         if farm_id:
#             farm = get_object_or_404(Farm, id=farm_id)
#             cows = Animal.objects.filter(farm=farm)
        
#         if cow_id:
#             cow_details = get_object_or_404(Animal, cow_id=cow_id)

#     return render(request, 'farm_details.html', {
#         'farms': farms,
#         'farm': farm,
#         'cows': cows,
#         'cow_details': cow_details,
#         'cow_id': cow_id
#     })

from django.shortcuts import render, get_object_or_404
from .models import Farm


# used to handle the search but not for the table

# def search_farm(request):
#     farm = None
#     if 'farm_id' in request.GET:
#         farm_id = request.GET['farm_id']
#         try:
#             farm = Farm.objects.get(farm_id=farm_id)
#         except Farm.DoesNotExist:
#             farm = None
    
#     return render(request, 'dashboard.html', {'farm': farm})




def search_farm(request):
    farm = None
    animal = []  # Use `animal` as the key to match other pages
    if 'farm_id' in request.GET:
        farm_id = request.GET['farm_id']
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            # Fetch all animals related to this farm
            animal = list(Animal.objects.filter(farm_id=farm))
        except Farm.DoesNotExist:
            farm = None

    # Determine the page to render based on a query parameter (default to dashboard)
    page = request.GET.get('page', 'dashboard')
    template_name = 'tables.html' if page == 'tables' else 'dashboard.html'

    return render(request, template_name, {'farm': farm, 'animal': animal})




# itterable
# def search_animal(request):
#     animal = None
    
#     # Check if a specific cow_id is provided
#     if 'cow_id' in request.GET and request.GET['cow_id']:
#         cow_id = request.GET['cow_id']
#         try:
#             animal = [Animal.objects.get(cow_id=cow_id)]  # Wrap in a list to make it iterable
#         except Animal.DoesNotExist:
#             animal = []  # Empty list if no matching animal is found
#     else:
#         # If no cow_id is provided, retrieve all animals
#         animal = list(Animal.objects.all())
    
#     return render(request, 'dashboard.html', {'animal': animal})



# both iterable and non-iterable
# def search_animal(request):
#     animal = []
    
#     # Check if a specific cow_id is provided
#     if 'cow_id' in request.GET and request.GET['cow_id']:
#         cow_id = request.GET['cow_id']
#         try:
#             # Retrieve a single animal object and wrap it in a list to make it iterable
#             animal_instance = Animal.objects.get(cow_id=cow_id)
#             animal = [animal_instance]
#         except Animal.DoesNotExist:
#             animal = []  # Empty list if no matching animal is found
#     else:
#         # If no cow_id is provided, retrieve all animals
#         animal = list(Animal.objects.all())
    
#     return render(request, 'dashboard.html', {'animal': animal})



# non-iterable
def search_animal(request):
    animal = None
    if 'cow_id' in request.GET:
        cow_id = request.GET['cow_id']
        try:
            animal = Animal.objects.get(cow_id=cow_id)
        except Animal.DoesNotExist:
            animal = None
    return render(request, 'dashboard.html', {'animal': animal})



# def search_view(request):
#     query = request.GET.get('q')  # Get the search input
#     # For now, we're not filtering anything, but you can store the query for later use
#     context = {
#         'query': query,
#         'total_sales': 10000,  # Example existing data
#         'growth_rate': 12,     # Example existing data
#         # Add all other existing context data here
#     }
#
 #   return render(request, 'your_template.html', context)

