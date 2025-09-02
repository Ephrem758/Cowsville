"""
Business logic services for the Farm Manager application
"""

import logging
from typing import Optional, Tuple, Dict, Any
from django.db import transaction

from AlertSystem.sendMesage import send_alert
from .models import Message, Doctor, GeneralHealthStatus, UdderHealthStatus, MastitisStatus
from .constants import MessageTemplates, MessageTypes, DefaultHealthStatus


logger = logging.getLogger(__name__)


class MessagingService:
    """Service class to handle all messaging and notifications"""
    
    @staticmethod
    def send_notification_with_message_record(
        phone_number: str, 
        message_text: str, 
        message_type: str,
        farm, 
        cow=None,
        log_prefix: str = ""
    ) -> Tuple[bool, str]:
        """
        Send a notification and create a message record
        
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            response = send_alert(phone_number, message_text)
            is_sent = response.get("status") == "success"
            
            if is_sent:
                logger.info(f"{log_prefix} Alert sent successfully")
            else:
                logger.warning(f"{log_prefix} Failed to send alert")
            
            # Create message record regardless of send status
            Message.objects.create(
                farm=farm,
                cow=cow,
                message_text=message_text,
                message_type=message_type,
                is_sent=is_sent
            )
            
            return is_sent, ""
            
        except Exception as e:
            error_msg = f"Error sending notification: {str(e)}"
            logger.error(f"{log_prefix} {error_msg}")
            return False, error_msg

    @staticmethod
    def send_heat_sign_notifications(cow, heat_signs: str) -> Dict[str, bool]:
        """
        Send heat sign notifications to both inseminator and farmer
        
        Returns:
            Dict with 'inseminator_sent' and 'farmer_sent' keys
        """
        results = {'inseminator_sent': False, 'farmer_sent': False}
        
        # Prepare messages
        inseminator_message = MessageTemplates.insemination_alert(
            cow.farm.farm_id, cow.farm.owner_name, cow.farm.address,
            cow.farm.telephone_number, cow.cow_id, heat_signs
        )
        
        farmer_message = MessageTemplates.farmer_heat_notification(
            cow.cow_id, cow.farm.inseminator.name
        )
        
        # Send to inseminator
        if cow.farm.inseminator:
            inseminator_sent, _ = MessagingService.send_notification_with_message_record(
                cow.farm.inseminator.phone_number,
                inseminator_message,
                MessageTypes.INSEMINATION_ALERT,
                cow.farm,
                cow,
                f"Inseminator notification for cow {cow.cow_id}:"
            )
            results['inseminator_sent'] = inseminator_sent
        
        # Send to farmer
        farmer_sent, _ = MessagingService.send_notification_with_message_record(
            cow.farm.telephone_number,
            farmer_message,
            MessageTypes.INSEMINATION_ALERT,
            cow.farm,
            cow,
            f"Farmer notification for cow {cow.cow_id}:"
        )
        results['farmer_sent'] = farmer_sent
        
        return results

    @staticmethod
    def send_staff_change_notifications(
        farm, 
        staff_type: str, 
        old_staff, 
        new_staff,
        message_type: str
    ) -> Dict[str, bool]:
        """
        Send notifications for staff changes
        
        Returns:
            Dict with notification results
        """
        results = {}
        
        # Notify old staff if exists
        if old_staff:
            old_message = MessageTemplates.staff_unassignment_notice(
                farm.farm_id, farm.owner_name
            )
            old_staff_sent, _ = MessagingService.send_notification_with_message_record(
                old_staff.phone_number,
                old_message,
                message_type,
                farm,
                None,
                f"Old {staff_type} notification:"
            )
            results['old_staff_sent'] = old_staff_sent
        
        # Notify new staff
        new_message = MessageTemplates.staff_assignment_notice(
            staff_type, farm.farm_id, farm.owner_name, 
            farm.address, farm.telephone_number
        )
        new_staff_sent, _ = MessagingService.send_notification_with_message_record(
            new_staff.phone_number,
            new_message,
            message_type,
            farm,
            None,
            f"New {staff_type} notification:"
        )
        results['new_staff_sent'] = new_staff_sent
        
        # Notify farmer about doctor change
        if staff_type == "doctor":
            farmer_message = MessageTemplates.doctor_change_farmer_notice(
                new_staff.name, new_staff.phone_number
            )
            farmer_sent, _ = MessagingService.send_notification_with_message_record(
                farm.telephone_number,
                farmer_message,
                message_type,
                farm,
                None,
                "Farmer doctor change notification:"
            )
            results['farmer_sent'] = farmer_sent
        
        return results


class HealthService:
    """Service class to handle health-related operations"""
    
    @staticmethod
    def get_default_health_statuses() -> Tuple[Optional[Any], Optional[Any], Optional[Any]]:
        """
        Get default health status objects
        
        Returns:
            Tuple of (general_health, udder_health, mastitis) objects
        """
        try:
            general_health = GeneralHealthStatus.objects.get(
                name=DefaultHealthStatus.GENERAL_HEALTH_NORMAL
            )
            udder_health = UdderHealthStatus.objects.get(
                name=DefaultHealthStatus.UDDER_HEALTH_NORMAL
            )
            mastitis = MastitisStatus.objects.get(
                name=DefaultHealthStatus.MASTITIS_CLINICAL
            )
            return general_health, udder_health, mastitis
        except Exception as e:
            logger.error(f"Could not find default health status: {str(e)}")
            # Fallback to first available
            general_health = GeneralHealthStatus.objects.first()
            udder_health = UdderHealthStatus.objects.first()
            mastitis = MastitisStatus.objects.first()
            return general_health, udder_health, mastitis

    @staticmethod
    def get_doctor_for_assessment(farm) -> Optional[Doctor]:
        """
        Get a doctor for medical assessment - prefer farm's doctor, fallback to active doctor
        
        Returns:
            Doctor instance or None
        """
        assessed_by = farm.doctor
        if not assessed_by:
            # Try to get the first available active doctor
            assessed_by = Doctor.objects.filter(is_active=True).first()
            if not assessed_by:
                # If no active doctors, get any doctor
                assessed_by = Doctor.objects.first()
                
            if assessed_by:
                logger.info(f"No doctor assigned to farm, using fallback doctor: {assessed_by.name}")
            else:
                logger.warning("No doctors available in the system")
                
        return assessed_by


class ValidationService:
    """Service class for common validation operations"""
    
    @staticmethod
    def convert_yes_no_to_boolean(value, default: bool = False) -> bool:
        """
        Convert 'yes'/'no' string to boolean
        
        Args:
            value: The value to convert (can be bool, str, or None)
            default: Default value if conversion fails
            
        Returns:
            Boolean value
        """
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            normalized = value.lower().strip()
            if normalized in ['yes', 'true', '1', 'y', 'yes_sick']:
                return True
            elif normalized in ['no', 'false', '0', 'n', 'no_sick']:
                return False
            else:
                return default
        else:
            return default

    @staticmethod
    def safe_int_conversion(value, default: int = 0) -> int:
        """
        Safely convert value to integer
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            Integer value
        """
        try:
            return int(float(value)) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def format_ethiopian_phone_number(value):
        """
        Helper method to format Ethiopian phone numbers by adding +251 prefix
        
        Args:
            value: Phone number string to format
            
        Returns:
            Formatted phone number string
        """
        if not value:
            return value
            
        # Remove any spaces, dashes, or other formatting
        cleaned_number = ''.join(filter(str.isdigit, value.replace('+', '')))
        
        # If number already starts with +251, return as is
        if value.startswith('+251'):
            return value
            
        # If number starts with 251, add + prefix
        if cleaned_number.startswith('251'):
            return f'+{cleaned_number}'
            
        # If number starts with 0 (Ethiopian local format), replace with +251
        if cleaned_number.startswith('0') and len(cleaned_number) == 10:
            return f'+251{cleaned_number[1:]}'
            
        # If number is 9 digits (Ethiopian mobile without 0), add +251
        if len(cleaned_number) == 9 and cleaned_number[0] in ['9']:
            return f'+251{cleaned_number}'
            
        # If none of the above, return original value (will be caught by model validation)
        return value
    
    @staticmethod
    def map_hygiene_score(value):
        """
        Map hygiene score text to number
        
        Args:
            value: Hygiene score value (string or number)
            
        Returns:
            Integer hygiene score (1-4)
        """
        if not value:
            return 2  # Default value
            
        hygiene_mapping = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4,
            '1': 1, '2': 2, '3': 3, '4': 4
        }
        return hygiene_mapping.get(str(value).lower(), 2)  # Default to 2


class LoggingMixin:
    """Mixin to provide consistent logging patterns"""
    
    def get_logger(self):
        """Get logger instance for the class"""
        return logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
    
    def log_request_received(self, operation: str, data=None):
        """Log incoming request"""
        logger = self.get_logger()
        if data:
            logger.info(f"Received {operation} request with data: {data}")
        else:
            logger.info(f"Received {operation} request")
    
    def log_operation_success(self, operation: str, identifier: str = ""):
        """Log successful operation"""
        logger = self.get_logger()
        if identifier:
            logger.info(f"Successfully {operation} {identifier}")
        else:
            logger.info(f"Successfully {operation}")
    
    def log_operation_error(self, operation: str, error: Exception, identifier: str = ""):
        """Log operation error"""
        logger = self.get_logger()
        if identifier:
            logger.error(f"Error {operation} {identifier}: {str(error)}", exc_info=True)
        else:
            logger.error(f"Error {operation}: {str(error)}", exc_info=True)
    
    def log_validation_error(self, operation: str, errors):
        """Log validation errors"""
        logger = self.get_logger()
        logger.warning(f"Invalid {operation} data: {errors}")


class ResponseService:
    """Service class for standardized API responses"""
    
    @staticmethod
    def success_response(message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a standardized success response
        
        Args:
            message: Success message
            data: Additional data to include
            
        Returns:
            Response dictionary
        """
        response = {"message": message}
        if data:
            response.update(data)
        return response
    
    @staticmethod
    def error_response(message: str, status_code: int = 500) -> Tuple[Dict[str, str], int]:
        """
        Create a standardized error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        return {"error": message}, status_code 