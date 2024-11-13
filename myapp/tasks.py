from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Animal

@shared_task
def send_alert_message(recipient, message):
    # Replace this with your actual integration logic to send alerts
    print(f"Sending alert to {recipient}: {message}")


@shared_task
def send_initial_alert(cow_id):
    try:
        animal = Animal.objects.get(cow_id=cow_id)
        if animal.pd_status == 'non_pregnant':
            message = f"Heat detected for cow {animal.cow_id}. For the next 6 hours, the cow should be given AI."
            send_alert_message(animal.farm.telephone, message)
            send_alert_message("doctor@example.com", f"Heat detected for cow {animal.cow_id}. {message}")
            
            # Schedule follow-up tasks
            send_high_probability_alert.apply_async((cow_id,), countdown=6*3600)
            send_low_probability_alert.apply_async((cow_id,), countdown=12*3600)

    except Animal.DoesNotExist:
        print(f"Cow with ID {cow_id} not found.")

@shared_task
def send_high_probability_alert(cow_id):
    try:
        animal = Animal.objects.get(cow_id=cow_id)
        if animal.pd_status == 'non_pregnant':
            message = f"This is her high probability for pregnancy now to 6 hours from now."
            send_alert_message(animal.farm.telephone, message)
            send_alert_message("doctor@example.com", f"High probability alert for cow {animal.cow_id}. {message}")
    except Animal.DoesNotExist:
        print(f"Cow with ID {cow_id} not found.")

@shared_task
def send_low_probability_alert(cow_id):
    try:
        animal = Animal.objects.get(cow_id=cow_id)
        if animal.pd_status == 'non_pregnant':
            message = f"This is her low probability for pregnancy to 6 hours from now."
            send_alert_message(animal.farm.telephone, message)
            send_alert_message("doctor@example.com", f"Low probability alert for cow {animal.cow_id}. {message}")
    except Animal.DoesNotExist:
        print(f"Cow with ID {cow_id} not found.")
