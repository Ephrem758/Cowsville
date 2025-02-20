from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
# import requests
from .models import Farm, Cow
from datetime import timedelta, timezone

from django.views.decorators.csrf import csrf_exempt
import json
# farm_management/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cow

from django.shortcuts import render, get_object_or_404
from .models import Farm
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from .serializers import FarmSerializer, CowSerializer  # You'll need to create these

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    return render(request, 'tables.html')

   
def notifications(request):
    return render(request, 'notifications.html')


def search_farm(request):
    farm = None
    Cow = []
    all_farms = Farm.objects.all().order_by('owner_name')  # Sort farms alphabetically by owner_name

    if 'farm_id' in request.GET and request.GET['farm_id']:
        farm_id = request.GET['farm_id']
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            Cow = list(Cow.objects.filter(farm_id=farm))
        except Farm.DoesNotExist:
            farm = None

    page = request.GET.get('page', 'dashboard')
    template_name = 'tables.html' if page == 'tables' else 'dashboard.html'

    return render(request, template_name, {'farm': farm, 'Cow': Cow, 'all_farms': all_farms})


# non-iterable
def search_animal(request):
    Cow = None
    if 'cow_id' in request.GET:
        cow_id = request.GET['cow_id']
        try:
            Cow = Cow.objects.get(cow_id=cow_id)
        except Cow.DoesNotExist:
            Cow = None
    return render(request, 'dashboard.html', {'Cow': Cow})



# retrieve both Cow and farm
def dashboard(request):
    farm = None
    Cow = None
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
            Cow = Cow.objects.get(cow_id=cow_id)
        except Cow.DoesNotExist:
            Cow = None

    # Render the template with both farm and Cow data
    return render(request, 'dashboard.html', {
        'farm': farm,
        'Cow': Cow,
        'all_farms': all_farms,
        'farm_id': farm_id,
        'cow_id': cow_id,
    })


def average_statistics(request):
    cows = Cow.objects.all()
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

    for cow in cows:
        for key in stats.keys():
            value = getattr(cow, key, 0)
            stats[key] += value
            if value:
                counts[key] += 1

    averages = {key: (stats[key] / counts[key] if counts[key] > 0 else 0) for key in stats.keys()}
    return Response({"averages": averages})


class ReportHeatSignView(APIView):
    def post(self, request, cow_id):
        # Retrieve the cow using the provided cow_id
        try:
            Cow = Cow.objects.get(cow_id=cow_id)
        except Cow.DoesNotExist:
            return Response({"error": "Cow not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve heat signs reported by the farmer
        farmer_message = request.data.get('signs')
        if not farmer_message:
            return Response({"error": "No signs provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Trigger the insemination alert sequence
        alert_insemination_sequence(Cow, {"signs": farmer_message}) # type: ignore

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
                    Cow = Cow.objects.get(cow_id=cow_id)
                    Cow.last_heat_sign = timezone.now().date()  # Update with the current date
                    Cow.save()  # Save changes to the database
                    
                    # Trigger the initial alert task
                    send_initial_alert.delay(cow_id)

                except Cow.DoesNotExist:
                    print(f"Cow with ID {cow_id} not found.")

# Function to check and send heat sign alerts
def check_heat_sign_alerts():
    today = timezone.now().date()
    Cows = Cow.objects.filter(pd_status='non_pregnant')
    print(Cows)

    for Cow in Cows:
        if Cow.last_heat_sign:
            days_since_last_heat = (today - Cow.last_heat_sign).days
            if 19 <= days_since_last_heat <= 24:
                # Send daily alert for 5 days within this range
                print("hi")
                send_alert_message.delay(Cow.farm.telephone, f"Reminder: Check cow {Cow.cow_id} for heat signs.")
                print("hi")
                # print(result.result)
        
        # Further logic to stop alert if the farmer sends a heat sign detected message (handled separately)
        # After checking alerts, process API-based alerts if a heat sign is detected
        # process_heat_sign_alerts_from_api()


# Function to send vaccine reminder for pregnant cows at the 7th month
def check_vaccine_reminder_for_pregnant_cows():
    today = timezone.now().date()
    Cows = Cow.objects.filter(pd_status='pregnant')

    for Cow in Cows:
        if Cow.days_to_calving and Cow.days_to_calving <= 90:  # Roughly the 7th month (90 days to calving)
            send_alert_message(
                Cow.farm.telephone,
                f"Reminder: Cow {Cow.cow_id} is 7 months pregnant. Schedule a vaccine check-up."
            )

# Endpoint to trigger alerts manually (for testing)
def trigger_alerts(request):
    check_heat_sign_alerts()
    
    # check_vaccine_reminder_for_pregnant_cows()
    return render(request, 'alerts_triggered.html')



@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process your data here
            print(data)
            return JsonResponse({'message': 'Data received successfully!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all().order_by('owner_name')
    serializer_class = FarmSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request):
        farm_id = request.query_params.get('farm_id')
        if farm_id:
            try:
                farm = Farm.objects.get(farm_id=farm_id)
                cows = Cow.objects.filter(farm=farm)
                farm_data = self.get_serializer(farm).data
                cow_data = CowSerializer(cows, many=True).data
                return Response({
                    'farm': farm_data,
                    'cows': cow_data
                })
            except Farm.DoesNotExist:
                return Response({'error': 'Farm not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No farm_id provided'}, status=status.HTTP_400_BAD_REQUEST)

class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request):
        cow_id = request.query_params.get('cow_id')
        if cow_id:
            try:
                cow = Cow.objects.get(cow_id=cow_id)
                return Response(self.get_serializer(cow).data)
            except Cow.DoesNotExist:
                return Response({'error': 'Cow not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No cow_id provided'}, status=status.HTTP_400_BAD_REQUEST)
