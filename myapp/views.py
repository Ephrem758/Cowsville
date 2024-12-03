from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import requests
from .models import Farm, Animal
from datetime import timedelta, timezone

# farm_management/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animal
from .tasks import send_initial_alert, send_alert_message


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




# def search_farm(request):
#     farm = None
#     animal = []  # Use `animal` as the key to match other pages
#     if 'farm_id' in request.GET:
#         farm_id = request.GET['farm_id']
#         try:
#             farm = Farm.objects.get(farm_id=farm_id)
#             # Fetch all animals related to this farm
#             animal = list(Animal.objects.filter(farm_id=farm))
#         except Farm.DoesNotExist:
#             farm = None

#     # Determine the page to render based on a query parameter (default to dashboard)
#     page = request.GET.get('page', 'dashboard')
#     template_name = 'tables.html' if page == 'tables' else 'dashboard.html'

#     return render(request, template_name, {'farm': farm, 'animal': animal})



# to fecth all farms
def search_farm(request):
    farm = None
    animal = []
    all_farms = Farm.objects.all().order_by('owner_name')  # Sort farms alphabetically by owner_name

    if 'farm_id' in request.GET and request.GET['farm_id']:
        farm_id = request.GET['farm_id']
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            animal = list(Animal.objects.filter(farm_id=farm))
        except Farm.DoesNotExist:
            farm = None

    page = request.GET.get('page', 'dashboard')
    template_name = 'tables.html' if page == 'tables' else 'dashboard.html'

    return render(request, template_name, {'farm': farm, 'animal': animal, 'all_farms': all_farms})




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



# retrieve both animal and farm
def dashboard(request):
    farm = None
    animal = None
    all_farms = Farm.objects.all().order_by('owner_name')  # Retrieve all farms for dropdown

    # Get query parameters
    farm_id = request.GET.get('farm_id', None)
    cow_id = request.GET.get('cow_id', None)

    # Handle farm ID search
    if farm_id:
        try:
            farm = Farm.objects.get(farm_id=farm_id)
        except Farm.DoesNotExist:
            farm = None

    # Handle cow ID search
    if cow_id:
        try:
            animal = Animal.objects.get(cow_id=cow_id)
        except Animal.DoesNotExist:
            animal = None

    # Render the template with both farm and animal data
    return render(request, 'dashboard.html', {
        'farm': farm,
        'animal': animal,
        'all_farms': all_farms,
        'farm_id': farm_id,
        'cow_id': cow_id,
    })




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



from django.shortcuts import render
from .models import Animal

def average_statistics(request):
    # Collect all animals
    animals = Animal.objects.all()

    # Initialize variables to store sums and counts
    stats = {
        "insemination_after_calving": 0,
        "calving_interval": 0,
        "heat_after_calving": 0,
        "cows_return_heat_60days": 0,
        "inseminations_per_conception": 0,
        "heifers_pregnant_after_01_service": 0,
        "mature_cows_pregnant_after_01_service": 0,
        "mature_cows_03_services": 0,
        "dry_period_days": 0,
        "cows_pregnancy_interval": 0,
        "pregnancy_interval_days": 0,
    }
    counts = {key: 0 for key in stats.keys()}

    # Process each animal to calculate totals
    for animal in animals:
        for key in stats.keys():
            # Use getattr to get the attribute value or default to 0
            value = getattr(animal, key, 0)
            stats[key] += value
            if value:  # Increment count only if the value is non-zero
                counts[key] += 1

    # Calculate averages
    averages = {key: (stats[key] / counts[key] if counts[key] > 0 else 0) for key in stats.keys()}

    context = {"averages": averages}
    return render(request, "average_statistics.html", context)


class ReportHeatSignView(APIView):
    def post(self, request, cow_id):
        # Retrieve the cow using the provided cow_id
        try:
            animal = Animal.objects.get(cow_id=cow_id)
        except Animal.DoesNotExist:
            return Response({"error": "Animal not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve heat signs reported by the farmer
        farmer_message = request.data.get('signs')
        if not farmer_message:
            return Response({"error": "No signs provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Trigger the insemination alert sequence
        alert_insemination_sequence(animal, {"signs": farmer_message}) # type: ignore

        # Respond with a success message
        return Response({"status": "Alert sequence initiated for insemination."}, status=status.HTTP_200_OK)


# Alert system

HEAT_SIGN_API_URL = 'https://example.com/api/heat-sign-detection/'
PREGNANCY_CHECK_API_URL = 'https://example.com/api/pregnancy-check/'


def fetch_heat_sign_data():
    try:
        response = requests.get(HEAT_SIGN_API_URL)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        data = response.json()
        return data  # Assuming the data is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Error fetching heat sign data: {e}")
        return None

# Function to handle alerts when heat signs are detected by an external API
def process_heat_sign_alerts_from_api():
    data = fetch_heat_sign_data()
    if data:
        for entry in data:  # Assuming each entry contains `cow_id` and `heat_detected`
            cow_id = entry.get('cow_id')
            heat_detected = entry.get('heat_detected')

            if heat_detected:
                try:
                    # Retrieve the cow object and update its last_heat_sign date
                    animal = Animal.objects.get(cow_id=cow_id)
                    animal.last_heat_sign = timezone.now().date()  # Update with the current date
                    animal.save()  # Save changes to the database
                    
                    # Trigger the initial alert task
                    send_initial_alert.delay(cow_id)

                except Animal.DoesNotExist:
                    print(f"Cow with ID {cow_id} not found.")

# Function to check and send heat sign alerts
def check_heat_sign_alerts():
    today = timezone.now().date()
    animals = Animal.objects.filter(pd_status='non_pregnant')

    for animal in animals:
        if animal.last_heat_sign:
            days_since_last_heat = (today - animal.last_heat_sign).days
            if 19 <= days_since_last_heat <= 24:
                # Send daily alert for 5 days within this range
                send_alert_message.delay(animal.farm.telephone, f"Reminder: Check cow {animal.cow_id} for heat signs.")
        
        # Further logic to stop alert if the farmer sends a heat sign detected message (handled separately)
        # After checking alerts, process API-based alerts if a heat sign is detected
        process_heat_sign_alerts_from_api()


# Function to send vaccine reminder for pregnant cows at the 7th month
def check_vaccine_reminder_for_pregnant_cows():
    today = timezone.now().date()
    animals = Animal.objects.filter(pd_status='pregnant')

    for animal in animals:
        if animal.days_to_calving and animal.days_to_calving <= 90:  # Roughly the 7th month (90 days to calving)
            send_alert_message(
                animal.farm.telephone,
                f"Reminder: Cow {animal.cow_id} is 7 months pregnant. Schedule a vaccine check-up."
            )

# Endpoint to trigger alerts manually (for testing)
def trigger_alerts(request):
    check_heat_sign_alerts()
    check_vaccine_reminder_for_pregnant_cows()
    return render(request, 'alerts_triggered.html')


# Update when pregnant
# Function to fetch and process pregnancy data from the API
def process_pregnancy_check_from_api():
    try:
        # Fetch data from the API
        response = requests.get(PREGNANCY_CHECK_API_URL)
        response.raise_for_status()  # Raises an exception for bad responses (4xx or 5xx)
        data = response.json()  # Assuming the response is in JSON format

        for entry in data:  # Assuming each entry contains `cow_id`, `is_pregnant`, `delivered`, and `delivery_date`
            cow_id = entry.get('cow_id')
            is_pregnant = entry.get('is_pregnant')  # Indicates if the cow is currently pregnant
            delivered = entry.get('delivered')  # Indicates if the cow has delivered
            delivery_date = entry.get('delivery_date')  # Date when the cow delivered, if applicable

            try:
                # Retrieve the cow object
                animal = Animal.objects.get(cow_id=cow_id)

                if delivered and delivery_date:
                    # Update fields when the cow has delivered a calf
                    delivery_date_parsed = timezone.datetime.strptime(delivery_date, '%Y-%m-%d').date()
                    animal.pd_status = 'non_pregnant'  # Set pregnancy status to non-pregnant
                    animal.days_after_calving = (timezone.now().date() - delivery_date_parsed).days  # Calculate days after calving

                elif is_pregnant:
                    # Update fields when the cow is pregnant
                    animal.pd_status = 'pregnant'
                    # Set the expected calving date to now + 280 days if no specific date is provided
                    animal.date_of_calving = timezone.now().date() + timedelta(days=280)

                else:
                    # If the cow is not pregnant and has not delivered, ensure status is set correctly
                    animal.pd_status = 'non_pregnant'

                animal.save()  # Save changes to the database

            except Animal.DoesNotExist:
                print(f"Cow with ID {cow_id} not found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching pregnancy data: {e}")