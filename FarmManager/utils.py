# farm_management/utils.py
"""
FarmManager Utilities

This module contains utility functions for the Farm Manager application.

Note: The messaging functionality has been moved to services.py under MessagingService.
The functions below are deprecated and should not be used in new code.
"""

import warnings
from .services import MessagingService
from .constants import MessageTypes


def send_doctor_alert(message, schedule_time=None):
    """
    DEPRECATED: Use MessagingService.send_notification_with_message_record() instead
    
    Legacy function for sending doctor alerts. This function is deprecated
    and will be removed in a future version.
    """
    warnings.warn(
        "send_doctor_alert is deprecated. Use MessagingService.send_notification_with_message_record() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # Logic moved to MessagingService
    pass


def send_farmer_alert(message, farm, schedule_time=None):
    """
    DEPRECATED: Use MessagingService.send_notification_with_message_record() instead
    
    Legacy function for sending farmer alerts. This function is deprecated
    and will be removed in a future version.
    """
    warnings.warn(
        "send_farmer_alert is deprecated. Use MessagingService.send_notification_with_message_record() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # Logic moved to MessagingService
    pass


# Example of how to use the new messaging service:
# 
# from .services import MessagingService
# from .constants import MessageTypes
# 
# # Send a notification with message record
# success, message = MessagingService.send_notification_with_message_record(
#     phone_number=doctor.phone_number,
#     message_text="Your alert message here",
#     message_type=MessageTypes.DOCTOR_ALERT,
#     farm=farm,
#     cow=cow,  # optional
#     log_prefix="Doctor alert:"
# )
