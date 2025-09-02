import logging
import atexit
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from django.utils.timezone import now
from FarmManager.models import Reproduction, Message
from FarmManager.constants import MessageTypes, MessageTemplates
from .sendMesage import send_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None

def check_heat_sign_alerts():
    """Checks non-pregnant cows for heat sign alerts and sends notifications if necessary"""
    today = now().date()
    threshold_days = 18  # Days before sending an alert
    alert_count = 0

    # Get cows that are NOT pregnant
    cows = Reproduction.objects.filter(is_cow_pregnant=False)

    for cow_reproduction in cows:
        if cow_reproduction.heat_sign_start:
            days_since_last_heat = (today - cow_reproduction.heat_sign_start.date()).days
            
            if days_since_last_heat >= threshold_days:
                # Check if we already sent an alert recently (within last 7 days)
                recent_alert = Message.objects.filter(
                    farm=cow_reproduction.farm,
                    cow=cow_reproduction.cow,
                    message_type=MessageTypes.HEAT_MONITORING_ALERT,
                    sent_date__gte=today - timedelta(days=7)
                ).exists()
                
                if not recent_alert:
                    # Use new message template
                    message_text = MessageTemplates.heat_monitoring_reminder(
                        cow_reproduction.cow.cow_id,
                        days_since_last_heat,
                        cow_reproduction.heat_sign_start.strftime('%Y-%m-%d')
                    )

                    # Send alert first
                    alert_response = send_alert(cow_reproduction.farm.telephone_number, message_text)

                    # Create message record only if alert was sent successfully
                    if alert_response.get("status") == "success":
                        Message.objects.create(
                            farm=cow_reproduction.farm,
                            cow=cow_reproduction.cow,
                            message_text=message_text,
                            message_type=MessageTypes.HEAT_MONITORING_ALERT,
                            is_sent=True,
                        )
                        alert_count += 1
                        logger.info(
                            f"✅ Heat monitoring alert sent for Cow {cow_reproduction.cow.cow_id} "
                            f"({days_since_last_heat} days since last heat)"
                        )
                    else:
                        logger.error(
                            f"❌ Failed to send heat alert for Cow {cow_reproduction.cow.cow_id}: "
                            f"{alert_response.get('message')}"
                        )

    logger.info(f"Heat sign check complete: {alert_count} alerts sent out of {len(cows)} non-pregnant cows")
    return f"Checked {len(cows)} non-pregnant cows, sent {alert_count} heat monitoring alerts"


def check_pregnancy_alerts():
    """Checks pregnant cows for calving alerts (2 months, 1 month, and due date)"""
    today = now().date()
    alert_count = 0

    # Get pregnant cows with expected calving dates
    pregnant_cows = Reproduction.objects.filter(
        is_cow_pregnant=True,
        calving_date__isnull=False
    )

    for cow_reproduction in pregnant_cows:
        expected_calving_date = cow_reproduction.calving_date
        days_until_calving = (expected_calving_date - today).days
        
        # Determine which alert to send based on days until calving
        alert_type = None
        message_template = None
        
        if 58 <= days_until_calving <= 62:  # 2 months (around 60 days)
            alert_type = MessageTypes.CALVING_2_MONTHS_ALERT
            message_template = MessageTemplates.calving_2_months_alert
        elif 28 <= days_until_calving <= 32:  # 1 month (around 30 days)
            alert_type = MessageTypes.CALVING_1_MONTH_ALERT
            message_template = MessageTemplates.calving_1_month_alert
        elif -2 <= days_until_calving <= 2:  # Due date (±2 days)
            alert_type = MessageTypes.CALVING_DUE_ALERT
            message_template = MessageTemplates.calving_due_alert
        
        if alert_type and message_template:
            # Check if we already sent this type of alert for this cow
            existing_alert = Message.objects.filter(
                farm=cow_reproduction.farm,
                cow=cow_reproduction.cow,
                message_type=alert_type,
                sent_date__gte=today - timedelta(days=7)  # Within last 7 days
            ).exists()
            
            if not existing_alert:
                # Create the alert message
                message_text = message_template(
                    cow_reproduction.cow.cow_id,
                    expected_calving_date.strftime('%Y-%m-%d'),
                    cow_reproduction.cow.lactation_number or 1
                )
                
                # Send alert first
                alert_response = send_alert(cow_reproduction.farm.telephone_number, message_text)
                
                # Create message record only if alert was sent successfully
                if alert_response.get("status") == "success":
                    Message.objects.create(
                        farm=cow_reproduction.farm,
                        cow=cow_reproduction.cow,
                        message_text=message_text,
                        message_type=alert_type,
                        is_sent=True,
                    )
                    alert_count += 1
                    
                    alert_description = {
                        MessageTypes.CALVING_2_MONTHS_ALERT: "2-month calving reminder",
                        MessageTypes.CALVING_1_MONTH_ALERT: "1-month calving reminder", 
                        MessageTypes.CALVING_DUE_ALERT: "calving due date alert"
                    }
                    
                    logger.info(
                        f"✅ {alert_description[alert_type]} sent for Cow {cow_reproduction.cow.cow_id} "
                        f"(due in {days_until_calving} days)"
                    )
                else:
                    logger.error(
                        f"❌ Failed to send pregnancy alert for Cow {cow_reproduction.cow.cow_id}: "
                        f"{alert_response.get('message')}"
                    )

    logger.info(f"Pregnancy check complete: {alert_count} alerts sent out of {len(pregnant_cows)} pregnant cows")
    return f"Checked {len(pregnant_cows)} pregnant cows, sent {alert_count} pregnancy alerts"


def run_daily_checks():
    """Run all daily monitoring checks"""
    logger.info("🔄 Starting daily farm monitoring checks...")
    
    # Run heat sign alerts for non-pregnant cows
    heat_result = check_heat_sign_alerts()
    
    # Run pregnancy monitoring alerts for pregnant cows
    pregnancy_result = check_pregnancy_alerts()
    
    logger.info("✅ Daily farm monitoring checks completed")
    logger.info(f"📊 Summary - Heat: {heat_result} | Pregnancy: {pregnancy_result}")
    
    return f"Daily checks completed - {heat_result} | {pregnancy_result}"

def shutdown():
    """Properly shut down the scheduler"""
    global scheduler
    if scheduler and scheduler.running:
        logger.info("Shutting down APScheduler...")
        scheduler.shutdown()
        logger.info("APScheduler shutdown complete")

def start():
    """Start APScheduler for daily farm monitoring (heat signs and pregnancy alerts)"""
    global scheduler
    
    # Don't start if already running
    if scheduler and scheduler.running:
        logger.warning("APScheduler is already running")
        return

    jobstores = {"default": MemoryJobStore()}
    executors = {"default": ThreadPoolExecutor(2)}
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)

    # Manually trigger the initial check
    logger.info("🚀 Running initial farm monitoring checks...")
    run_daily_checks()

    # Schedule the combined daily checks to run every 24 hours
    scheduler.add_job(
        run_daily_checks, 
        "interval", 
        hours=24,
        id="daily_farm_monitoring"
    )

    # Register the shutdown handler
    atexit.register(shutdown)

    logger.info("✅ APScheduler started for daily farm monitoring (every 24 hours)")
    logger.info("📋 Monitoring: Heat signs for non-pregnant cows & Pregnancy milestones")
    scheduler.start()
