import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from django.utils.timezone import now
from FarmManager.models import Reproduction, Message
from .sendMesage import send_alert

logging.basicConfig(level=logging.INFO)


def check_heat_sign_alerts():
    """Checks cows for heat sign alerts and sends notifications if necessary"""
    today = now().date()
    threshold_days = 18  # Days before sending an alert

    # Get cows that are NOT pregnant
    cows = Reproduction.objects.filter(is_cow_pregnant=False)

    for cow in cows:
        if cow.heat_sign_start:
            days_since_last_heat = (today - cow.heat_sign_start.date()).days
            if days_since_last_heat >= threshold_days:
                message_text = f"Heat Sign Alert: Cow {cow.cow.id} has not shown heat signs for {days_since_last_heat} days. Please check!"

                # Send alert first
                alert_response = send_alert(cow.farm.telephone_number, message_text)

                # Create message record only if alert was sent successfully
                if alert_response.get("status") == "success":
                    Message.objects.create(
                        farm=cow.farm,
                        cow=cow.cow,
                        message_text=message_text,
                        message_type="heat_alert",
                        is_sent=True,
                    )
                    logging.info(
                        f"✅ Heat Sign Alert sent and recorded for Cow {cow.cow.id}"
                    )
                else:
                    logging.error(
                        f"❌ Failed to send alert for Cow {cow.cow.id}: {alert_response.get('message')}"
                    )

    return f"Checked {len(cows)} cows for heat sign alerts"


def start():
    """Start APScheduler for heat sign alerts every 24 hours"""
    jobstores = {"default": MemoryJobStore()}
    executors = {"default": ThreadPoolExecutor(2)}
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)

    # Schedule the task to run every 24 hours
    scheduler.add_job(check_heat_sign_alerts, "interval", hours=24)

    logging.info("✅ APScheduler started for heat sign alerts (every 24 hours)")
    scheduler.start()
