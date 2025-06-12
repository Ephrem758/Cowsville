from rest_framework import serializers
from .models import (
    Farm,
    Cow,
    Doctor,
    Inseminator,
    Message,
    BreedType,
    HousingType,
    FloorType,
    FeedingFrequency,
    WaterSource,
    GynecologicalStatus,
    UdderHealthStatus,
    MastitisStatus,
    GeneralHealthStatus,
    MedicalAssessment,
    InseminationRecord,
    FarmerMedicalReport,
    Reproduction,
)
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import models
import logging

logger = logging.getLogger(__name__)


class FarmSerializer(serializers.ModelSerializer):
    # Include nested serialization for related fields
    type_of_housing_name = serializers.CharField(source='type_of_housing.display_name', read_only=True)
    type_of_floor_name = serializers.CharField(source='type_of_floor.display_name', read_only=True)
    source_of_water_name = serializers.CharField(source='source_of_water.display_name', read_only=True)
    rate_of_cow_feeding_name = serializers.CharField(source='rate_of_cow_feeding.display_name', read_only=True)
    rate_of_water_giving_name = serializers.CharField(source='rate_of_water_giving.display_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True, allow_null=True)
    inseminator_name = serializers.CharField(source='inseminator.name', read_only=True, allow_null=True)
    
    # Field mappings for incoming data
    tel_no = serializers.CharField(write_only=True, required=False)
    fcc_no = serializers.CharField(write_only=True, required=False)
    herd_size = serializers.CharField(write_only=True, required=False)
    calves = serializers.CharField(write_only=True, required=False)
    heifers = serializers.CharField(write_only=True, required=False)
    milking_cows = serializers.CharField(write_only=True, required=False)
    TDM = serializers.CharField(write_only=True, required=False)
    housing = serializers.CharField(write_only=True, required=False)
    floor = serializers.CharField(write_only=True, required=False)
    feed = serializers.CharField(write_only=True, required=False)
    feeding_rate = serializers.CharField(write_only=True, required=False)
    water_source = serializers.CharField(write_only=True, required=False)
    water_rate = serializers.CharField(write_only=True, required=False)
    hygiene_score = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Farm
        fields = [
            # Model fields
            'farm_id', 'owner_name', 'address', 'telephone_number', 'location_gps',
            'fertility_camp_no', 'total_number_of_cows', 'number_of_calves', 
            'number_of_milking_cows', 'total_daily_milk', 'type_of_housing', 
            'type_of_floor', 'main_feed', 'rate_of_cow_feeding', 'source_of_water', 
            'rate_of_water_giving', 'farm_hygiene_score', 'inseminator', 'doctor',
            'is_deleted',
            # Read-only display fields
            'type_of_housing_name', 'type_of_floor_name', 'source_of_water_name',
            'rate_of_cow_feeding_name', 'rate_of_water_giving_name', 'doctor_name', 
            'inseminator_name',
            # Mapping fields (write-only)
            'tel_no', 'fcc_no', 'herd_size', 'calves', 'heifers', 'milking_cows',
            'TDM', 'housing', 'floor', 'feed', 'feeding_rate', 'water_source',
            'water_rate', 'hygiene_score'
        ]
        extra_kwargs = {
            'telephone_number': {'required': False},
            'fertility_camp_no': {'required': False},
            'total_number_of_cows': {'required': False},
            'number_of_calves': {'required': False},
            'number_of_milking_cows': {'required': False},
            'total_daily_milk': {'required': False},
            'main_feed': {'required': False},
            'farm_hygiene_score': {'required': False},
            'type_of_housing': {'required': False},
            'type_of_floor': {'required': False},
            'rate_of_cow_feeding': {'required': False},
            'source_of_water': {'required': False},
            'rate_of_water_giving': {'required': False},
        }
        
    def _format_phone_number(self, value):
        """
        Helper method to format Ethiopian phone numbers by adding +251 prefix
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
        
    def validate_telephone_number(self, value):
        """
        Automatically format Ethiopian phone numbers by adding +251 prefix
        """
        return self._format_phone_number(value)
        
    def validate(self, data):
        """
        Handle field mapping from incoming form data to model fields
        """
        # Map tel_no to telephone_number
        if 'tel_no' in data and not data.get('telephone_number'):
            tel_no_value = data.pop('tel_no')
            # Apply phone number formatting
            formatted_phone = self._format_phone_number(tel_no_value)
            data['telephone_number'] = formatted_phone
            
        # Map fcc_no to fertility_camp_no
        if 'fcc_no' in data and not data.get('fertility_camp_no'):
            try:
                data['fertility_camp_no'] = int(data.pop('fcc_no'))
            except (ValueError, TypeError):
                data['fertility_camp_no'] = 1  # Default value
                
        # Map herd_size to total_number_of_cows
        if 'herd_size' in data and not data.get('total_number_of_cows'):
            try:
                data['total_number_of_cows'] = int(data.pop('herd_size'))
            except (ValueError, TypeError):
                data['total_number_of_cows'] = 0
                
        # Map calves to number_of_calves
        if 'calves' in data and not data.get('number_of_calves'):
            try:
                data['number_of_calves'] = int(data.pop('calves'))
            except (ValueError, TypeError):
                data['number_of_calves'] = 0
                
        # Map milking_cows to number_of_milking_cows
        if 'milking_cows' in data and not data.get('number_of_milking_cows'):
            try:
                data['number_of_milking_cows'] = int(data.pop('milking_cows'))
            except (ValueError, TypeError):
                data['number_of_milking_cows'] = 0
                
        # Map TDM to total_daily_milk
        if 'TDM' in data and not data.get('total_daily_milk'):
            try:
                data['total_daily_milk'] = int(float(data.pop('TDM')))
            except (ValueError, TypeError):
                data['total_daily_milk'] = 0
                
        # Map feed to main_feed
        if 'feed' in data and not data.get('main_feed'):
            data['main_feed'] = data.pop('feed')
            
        # Map hygiene_score text to number
        if 'hygiene_score' in data and not data.get('farm_hygiene_score'):
            hygiene_mapping = {
                'one': 1, 'two': 2, 'three': 3, 'four': 4,
                '1': 1, '2': 2, '3': 3, '4': 4
            }
            hygiene_value = data.pop('hygiene_score').lower()
            data['farm_hygiene_score'] = hygiene_mapping.get(hygiene_value, 2)  # Default to 2
            
        # Handle housing type mapping
        if 'housing' in data and not data.get('type_of_housing'):
            try:
                from .models import HousingType
                housing_name = data.pop('housing').replace('_', ' ').title()
                housing_type = HousingType.objects.filter(
                    models.Q(name__icontains=housing_name) | 
                    models.Q(display_name__icontains=housing_name)
                ).first()
                if housing_type:
                    data['type_of_housing'] = housing_type  # Assign the object, not the ID
                else:
                    # Get first available housing type as fallback
                    first_housing = HousingType.objects.first()
                    if first_housing:
                        data['type_of_housing'] = first_housing  # Assign the object, not the ID
            except Exception:
                pass
                
        # Handle floor type mapping
        if 'floor' in data and not data.get('type_of_floor'):
            try:
                from .models import FloorType
                floor_name = data.pop('floor').replace('_', ' ').title()
                floor_type = FloorType.objects.filter(
                    models.Q(name__icontains=floor_name) | 
                    models.Q(display_name__icontains=floor_name)
                ).first()
                if floor_type:
                    data['type_of_floor'] = floor_type  # Assign the object, not the ID
                else:
                    # Get first available floor type as fallback
                    first_floor = FloorType.objects.first()
                    if first_floor:
                        data['type_of_floor'] = first_floor  # Assign the object, not the ID
            except Exception:
                pass
                
        # Handle feeding rate mapping
        if 'feeding_rate' in data and not data.get('rate_of_cow_feeding'):
            try:
                from .models import FeedingFrequency
                feeding_name = data.pop('feeding_rate').replace('_', ' ').title()
                feeding_freq = FeedingFrequency.objects.filter(
                    models.Q(name__icontains=feeding_name) | 
                    models.Q(display_name__icontains=feeding_name)
                ).first()
                if feeding_freq:
                    data['rate_of_cow_feeding'] = feeding_freq  # Assign the object, not the ID
                else:
                    # Get first available feeding frequency as fallback
                    first_feeding = FeedingFrequency.objects.first()
                    if first_feeding:
                        data['rate_of_cow_feeding'] = first_feeding  # Assign the object, not the ID
            except Exception:
                pass
                
        # Handle water source mapping
        if 'water_source' in data and not data.get('source_of_water'):
            try:
                from .models import WaterSource
                water_name = data.pop('water_source').replace('_', ' ').title()
                water_src = WaterSource.objects.filter(
                    models.Q(name__icontains=water_name) | 
                    models.Q(display_name__icontains=water_name)
                ).first()
                if water_src:
                    data['source_of_water'] = water_src  # Assign the object, not the ID
                else:
                    # Get first available water source as fallback
                    first_water = WaterSource.objects.first()
                    if first_water:
                        data['source_of_water'] = first_water  # Assign the object, not the ID
            except Exception:
                pass
                
        # Handle water rate mapping
        if 'water_rate' in data and not data.get('rate_of_water_giving'):
            try:
                from .models import FeedingFrequency
                water_rate_name = data.pop('water_rate').replace('_', ' ').title()
                water_freq = FeedingFrequency.objects.filter(
                    models.Q(name__icontains=water_rate_name) | 
                    models.Q(display_name__icontains=water_rate_name)
                ).first()
                if water_freq:
                    data['rate_of_water_giving'] = water_freq  # Assign the object, not the ID
                else:
                    # Get first available feeding frequency as fallback
                    first_feeding = FeedingFrequency.objects.first()
                    if first_feeding:
                        data['rate_of_water_giving'] = first_feeding  # Assign the object, not the ID
            except Exception:
                pass
                
        # Clean up any remaining unmapped fields
        fields_to_remove = ['heifers']  # Fields that don't map to anything
        for field in fields_to_remove:
            data.pop(field, None)
            
        # Auto-assign first available doctor and inseminator if not provided
        if not data.get('doctor'):
            try:
                from .models import Doctor
                first_doctor = Doctor.objects.filter(is_active=True).first()
                if first_doctor:
                    data['doctor'] = first_doctor
                    logger.info(f"Auto-assigned doctor: {first_doctor.name} (ID: {first_doctor.id}) to farm {data.get('farm_id', 'Unknown')}")
                else:
                    # Try to get any doctor (even inactive) as fallback
                    fallback_doctor = Doctor.objects.first()
                    if fallback_doctor:
                        data['doctor'] = fallback_doctor
                        logger.warning(f"No active doctors found. Auto-assigned inactive doctor: {fallback_doctor.name} (ID: {fallback_doctor.id}) to farm {data.get('farm_id', 'Unknown')}")
                    else:
                        logger.warning(f"No doctors found in database. Farm {data.get('farm_id', 'Unknown')} will be created without a doctor.")
            except Exception as e:
                logger.error(f"Could not auto-assign doctor to farm {data.get('farm_id', 'Unknown')}: {e}")
                
        if not data.get('inseminator'):
            try:
                from .models import Inseminator
                first_inseminator = Inseminator.objects.filter(is_active=True).first()
                if first_inseminator:
                    data['inseminator'] = first_inseminator
                    logger.info(f"Auto-assigned inseminator: {first_inseminator.name} (ID: {first_inseminator.id}) to farm {data.get('farm_id', 'Unknown')}")
                else:
                    # Try to get any inseminator (even inactive) as fallback
                    fallback_inseminator = Inseminator.objects.first()
                    if fallback_inseminator:
                        data['inseminator'] = fallback_inseminator
                        logger.warning(f"No active inseminators found. Auto-assigned inactive inseminator: {fallback_inseminator.name} (ID: {fallback_inseminator.id}) to farm {data.get('farm_id', 'Unknown')}")
                    else:
                        logger.warning(f"No inseminators found in database. Farm {data.get('farm_id', 'Unknown')} will be created without an inseminator.")
            except Exception as e:
                logger.error(f"Could not auto-assign inseminator to farm {data.get('farm_id', 'Unknown')}: {e}")
            
        # Ensure required fields have values
        if not data.get('telephone_number'):
            raise serializers.ValidationError({'telephone_number': 'This field is required.'})
        if not data.get('fertility_camp_no'):
            raise serializers.ValidationError({'fertility_camp_no': 'This field is required.'})
        if not data.get('total_number_of_cows'):
            raise serializers.ValidationError({'total_number_of_cows': 'This field is required.'})
        if not data.get('number_of_calves'):
            raise serializers.ValidationError({'number_of_calves': 'This field is required.'})
        if not data.get('number_of_milking_cows'):
            raise serializers.ValidationError({'number_of_milking_cows': 'This field is required.'})
        if not data.get('total_daily_milk'):
            raise serializers.ValidationError({'total_daily_milk': 'This field is required.'})
        if not data.get('main_feed'):
            raise serializers.ValidationError({'main_feed': 'This field is required.'})
        if not data.get('farm_hygiene_score'):
            raise serializers.ValidationError({'farm_hygiene_score': 'This field is required.'})
        if not data.get('type_of_housing'):
            raise serializers.ValidationError({'type_of_housing': 'This field is required.'})
        if not data.get('type_of_floor'):
            raise serializers.ValidationError({'type_of_floor': 'This field is required.'})
        if not data.get('rate_of_cow_feeding'):
            raise serializers.ValidationError({'rate_of_cow_feeding': 'This field is required.'})
        if not data.get('source_of_water'):
            raise serializers.ValidationError({'source_of_water': 'This field is required.'})
        if not data.get('rate_of_water_giving'):
            raise serializers.ValidationError({'rate_of_water_giving': 'This field is required.'})
            
        return data


class CowSerializer(serializers.ModelSerializer):
    """Serializer focused on READING Cow data with all fields."""
    
    # Customize representation of related fields (optional - show names instead of IDs)
    breed_name = serializers.CharField(source='breed.display_name', read_only=True)
    gynecological_status_name = serializers.CharField(source='gynecological_status.display_name', read_only=True)
    
    # Explicitly include nested farm details
    farm = FarmSerializer(read_only=True)

    class Meta:
        model = Cow
        fields = '__all__' # Include all model fields
        # Add 'breed_name', 'gynecological_status_name' to the output list if defined above
        # The actual FK fields ('breed', 'gynecological_status') will still be included by __all__ (as IDs)
        # If you ONLY want the names, list fields explicitly instead of using '__all__'
        # Example of explicit listing:
        # fields = [
        #     'id', 'farm', 'cow_id', 'breed_name', 'date_of_birth', 'sex', 'parity', 
        #     'body_weight', 'bcs', 'gynecological_status_name', 'lactation_number', 
        #     # ... list all other desired model fields (excluding FKs if replaced by names) ...
        #     'is_deleted'
        # ]

# --- Serializers primarily for INPUT --- 
# (Keep these separate if complex validation/mapping is needed for create/update)

# Example: A separate serializer for creating cows might look like this
class CowCreateUpdateSerializer(serializers.ModelSerializer):
    farm_id_input = serializers.CharField(write_only=True, source='farm_id')
    cow_id_input = serializers.CharField(write_only=True, source='cow_id')
    
    # Fields that need conversion
    breed = serializers.CharField(write_only=True)
    gynecological_status_name = serializers.CharField(write_only=True, required=False)
    gynecological_status = serializers.PrimaryKeyRelatedField(queryset=GynecologicalStatus.objects.all(), required=False)
    has_lameness = serializers.CharField(required=False)
    cow_inseminated_before = serializers.CharField(required=False)
    is_vaccinated = serializers.CharField(required=False)
    
    # Override BCS field to accept string input
    bcs = serializers.CharField(required=False)
    
    # Fields to handle yes/no
    deworming = serializers.CharField(required=False)
    
    # These fields don't exist in the Cow model but are used in create
    reproductive_health = serializers.CharField(required=False, write_only=True)
    metabolic_disease = serializers.CharField(required=False, write_only=True)
    is_pregnant = serializers.CharField(required=False, write_only=True)
    
    # Vaccination fields
    vaccination_date = serializers.DateField(required=False, write_only=True)
    vaccination_type = serializers.CharField(required=False, write_only=True)
    
    # Deworming fields
    deworming_date = serializers.DateField(required=False, write_only=True)
    deworming_type = serializers.CharField(required=False, write_only=True)
    
    # Heat sign fields for Reproduction model
    heat_start_date = serializers.DateTimeField(required=False, write_only=True)
    heat_end_date = serializers.DateTimeField(required=False, write_only=True)
    heat_signs = serializers.CharField(required=False, write_only=True)
    
    class Meta:
        model = Cow
        fields = [
             'farm_id_input', 'cow_id_input', 'breed', 'date_of_birth', 'sex', 'parity', 
             'body_weight', 'bcs', 'gynecological_status', 'gynecological_status_name', 'lactation_number', 
             'days_in_milk', 'average_daily_milk', 'cow_inseminated_before', 
             'last_date_insemination', 'number_of_inseminations', 'id_or_breed_bull_used', 
             'last_calving_date', 'has_lameness', 'reproductive_health', 'metabolic_disease',
             'is_vaccinated', 'vaccination_date', 'vaccination_type', 'deworming',
             'deworming_date', 'deworming_type', 'is_pregnant', 'heat_start_date', 
             'heat_end_date', 'heat_signs'
        ]
        
    def to_internal_value(self, data):
        """Custom field processing before validation"""
        # Handle lactation_number conversion
        if 'lactation_number' in data and data['lactation_number']:
            try:
                # Convert to float first, then to int
                data = data.copy()
                data['lactation_number'] = int(float(data['lactation_number']))
            except (ValueError, TypeError):
                # Let the field validator handle this error
                pass
                
        return super().to_internal_value(data)
        
    def validate_bcs(self, value):
        """Convert string BCS to a valid choice"""
        try:
            # Convert to float
            bcs_float = float(value)
            
            # Clamp to valid range
            if bcs_float < 1.0:
                bcs_float = 1.0
            elif bcs_float > 5.0:
                bcs_float = 5.0
                
            # Round to nearest 0.5
            rounded = round(bcs_float * 2) / 2
            
            # Get valid choices from model
            valid_choices = [x / 2 for x in range(2, 11)]  # [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
            
            # Find closest valid choice
            valid_bcs = min(valid_choices, key=lambda x: abs(x - rounded))
            
            # Return as Decimal with str conversion for exact representation
            return Decimal(str(valid_bcs))
        except (ValueError, TypeError, InvalidOperation):
            raise serializers.ValidationError("BCS must be a number between 1.0 and 5.0")

    def validate_lactation_number(self, value):
        """Convert lactation number to integer"""
        try:
            # Convert to float first to handle cases like "2.5"
            float_value = float(value)
            # Convert to integer
            return int(float_value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Lactation number must be a valid number")

    def validate_has_lameness(self, value):
        """Convert yes/no string to boolean"""
        return value.lower() == 'yes'
        
    def validate_cow_inseminated_before(self, value):
        """Convert yes/no string to boolean"""
        return value.lower() == 'yes'
        
    def validate_is_vaccinated(self, value):
        """Convert yes/no string to boolean"""
        return value.lower() == 'yes'
        
    def validate_deworming(self, value):
        """Convert yes/no string to boolean"""
        return value.lower() == 'yes'
        
    def validate(self, data):
        """Handle breed and gynecological_status lookups by name"""
        try:
            # Handle breed lookup
            breed_name = data.pop('breed', None)
            if breed_name:
                try:
                    # Try exact match on name
                    breed = BreedType.objects.get(name__iexact=breed_name)
                except BreedType.DoesNotExist:
                    # Try partial match on name or display_name
                    breed = BreedType.objects.filter(
                        models.Q(name__icontains=breed_name) | 
                        models.Q(display_name__icontains=breed_name)
                    ).first()
                    
                    if not breed:
                        raise serializers.ValidationError({'breed': f'Breed "{breed_name}" not found'})
                        
                data['breed'] = breed
                
            # Handle gynecological status lookup if name provided
            gyn_status_name = data.pop('gynecological_status_name', None)
            if gyn_status_name and 'gynecological_status' not in data:
                try:
                    # Try exact match on name
                    gyn_status = GynecologicalStatus.objects.get(name__iexact=gyn_status_name)
                except GynecologicalStatus.DoesNotExist:
                    # Try partial match on name or display_name
                    gyn_status = GynecologicalStatus.objects.filter(
                        models.Q(name__icontains=gyn_status_name) | 
                        models.Q(display_name__icontains=gyn_status_name)
                    ).first()
                    
                    if not gyn_status:
                        raise serializers.ValidationError(
                            {'gynecological_status': f'Status "{gyn_status_name}" not found'}
                        )
                        
                data['gynecological_status'] = gyn_status
                
            # Move deworming boolean to has_deworming
            if 'deworming' in data:
                data['has_deworming'] = data.pop('deworming')
                
            return data
        except Exception as e:
            raise serializers.ValidationError(f"Error validating data: {str(e)}")
        
    def create(self, validated_data):
        # Pop the input-only fields before calling super().create
        farm_id = validated_data.pop('farm_id', None) 
        cow_id = validated_data.pop('cow_id', None) 

        if not farm_id:
            raise serializers.ValidationError({'farm_id_input': 'This field is required.'})

        try:
            # Get farm
            farm = Farm.objects.get(farm_id=farm_id)
            validated_data['farm'] = farm
            if cow_id:
                validated_data['cow_id'] = cow_id
            
            # Extract non-Cow model fields for later use
            medical_fields = {}
            reproduction_fields = {}
            
            # Fields for Medical Assessment
            for field in ['has_lameness', 'reproductive_health', 'metabolic_disease', 
                          'is_vaccinated', 'vaccination_date', 'vaccination_type',
                          'deworming_date', 'deworming_type', 'has_deworming']:
                if field in validated_data:
                    medical_fields[field] = validated_data.pop(field)
            
            # Fields for Reproduction
            if 'is_pregnant' in validated_data:
                reproduction_fields['is_pregnant'] = validated_data.pop('is_pregnant')
            
            # Create the cow instance with only valid Cow model fields
            instance = super().create(validated_data)
            
            # Save extracted data in view's perform_create method
            self.context['medical_fields'] = medical_fields
            self.context['reproduction_fields'] = reproduction_fields
            
            return instance
        except Farm.DoesNotExist:
            raise serializers.ValidationError({'farm_id_input': f'Farm with ID {farm_id} not found'})
        except Exception as e:
            raise serializers.ValidationError(f"Error creating cow: {str(e)}")


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        swagger_schema_fields = {
            "example": {
                "name": "Dr. John Smith",
                "phone_number": "+251912345678",
                "address": "Addis Ababa",
                "is_active": True,
                "specialization": "Veterinary Medicine",
                "license_number": "VET123"
            }
        }
        
    def _format_phone_number(self, value):
        """
        Helper method to format Ethiopian phone numbers by adding +251 prefix
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
        
    def validate_phone_number(self, value):
        """
        Automatically format Ethiopian phone numbers by adding +251 prefix
        """
        return self._format_phone_number(value)


class InseminatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inseminator
        fields = "__all__"
        
    def _format_phone_number(self, value):
        """
        Helper method to format Ethiopian phone numbers by adding +251 prefix
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
        
    def validate_phone_number(self, value):
        """
        Automatically format Ethiopian phone numbers by adding +251 prefix
        """
        return self._format_phone_number(value)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MedicalAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAssessment
        fields = "__all__"


class InseminationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InseminationRecord
        fields = "__all__"


class FarmerMedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerMedicalReport
        fields = "__all__"


class BreedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedType
        fields = "__all__"


class HousingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingType
        fields = "__all__"


class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        fields = "__all__"


class FeedingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingFrequency
        fields = "__all__"


class WaterSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSource
        fields = "__all__"


class GynecologicalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GynecologicalStatus
        fields = "__all__"


class UdderHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdderHealthStatus
        fields = "__all__"


class MastitisStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MastitisStatus
        fields = "__all__"


class GeneralHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHealthStatus
        fields = "__all__"


class ReproductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reproduction
        fields = "__all__"


class StaffAssignmentSerializer(serializers.ModelSerializer):
    staff_id = serializers.IntegerField(required=True)

    class Meta:
        abstract = True

    def validate(self, attrs):
        return NotImplementedError("child classes must implement this method")


class InseminatorAssignmentSerializer(StaffAssignmentSerializer):
    staff_id = serializers.IntegerField(required=True, source="inseminator_id")

    def validate_staff_id(self, value):
        try:
            inseminator = Inseminator.objects.get(id=value)
            if not inseminator.is_active:
                raise serializers.ValidationError("Inseminator is not active")
            return value
        except Inseminator.DoesNotExist:
            raise serializers.ValidationError("Inseminator Not Found")


class DoctorAssignmentSerializer(StaffAssignmentSerializer):
    staff_id = serializers.IntegerField(required=True, source="doctor_id")

    def validate_staff_id(self, value):
        try:
            doctor = Doctor.objects.get(id=value)
            if not doctor.is_active:
                raise serializers.ValidationError("Doctor is not active")
            return value
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor Not Found")


class HeatSignRecordSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    heat_signs = serializers.CharField(required=False, default="", allow_blank=True)
    heat_start_time = serializers.DateTimeField(required=True)
    heat_sign_recorded_at = serializers.DateTimeField(required=False, allow_null=True)

    def to_internal_value(self, data):
        """
        Override to handle custom datetime parsing for heat_start_time
        """
        logger.info(f"to_internal_value called with data: {data}")
        
        if 'heat_start_time' in data and isinstance(data['heat_start_time'], str):
            logger.info(f"Processing heat_start_time: '{data['heat_start_time']}'")
            # Parse different datetime formats
            datetime_str = data['heat_start_time']
            parsed_datetime = None
            
            # List of common datetime formats to try
            datetime_formats = [
                '%Y-%m-%dT%H:%M:%S.%f+03:00',  # 2025-05-21T12:06:00.000+03:00 (specific timezone)
                '%Y-%m-%dT%H:%M:%S.%f%z',      # 2025-05-21T12:06:00.000+0300 (timezone offset)
                '%Y-%m-%dT%H:%M:%S%z',         # 2025-05-21T12:06:00+0300 (timezone offset)
                '%Y-%m-%dT%H:%M:%S.%fZ',       # 2025-05-28T09:47:42.988Z
                '%Y-%m-%dT%H:%M:%SZ',          # 2025-05-28T09:47:42Z
                '%Y-%m-%dT%H:%M:%S',           # 2025-05-28T09:47:42
                '%Y-%m-%d %H:%M:%S.%f',        # 2025-05-28 09:47:42.988
                '%Y-%m-%d %H:%M:%S',           # 2025-05-28 09:47:42
                '%Y-%m-%d %H:%M',              # 2025-05-28 09:47
                '%d/%m/%Y %H:%M:%S',           # 28/05/2025 09:47:42
                '%d/%m/%Y %H:%M',              # 28/05/2025 09:47
                '%m/%d/%Y %H:%M:%S',           # 05/28/2025 09:47:42
                '%m/%d/%Y %H:%M',              # 05/28/2025 09:47
                '%Y-%m-%d',                    # 2025-05-28 (will add current time)
                '%H:%M:%S.%f+03:00',           # 12:45:00.000+03:00 (time only - will add today's date)
                '%H:%M:%S.%f%z',               # 12:45:00.000+0300 (time only with timezone)
                '%H:%M:%S%z',                  # 12:45:00+0300 (time only with timezone)
            ]
            
            for fmt in datetime_formats:
                try:
                    from datetime import datetime
                    parsed_datetime = datetime.strptime(datetime_str, fmt)
                    logger.info(f"Successfully parsed datetime with format '{fmt}': {parsed_datetime}")
                    
                    # If only date was provided, use current time
                    if fmt == '%Y-%m-%d':
                        from datetime import time
                        now = datetime.now()
                        parsed_datetime = datetime.combine(parsed_datetime.date(), now.time())
                        logger.info(f"Combined with current time: {parsed_datetime}")
                    
                    # If only time was provided (with timezone), use today's date
                    elif fmt in ['%H:%M:%S.%f+03:00', '%H:%M:%S.%f%z', '%H:%M:%S%z']:
                        from datetime import date
                        today = date.today()
                        parsed_datetime = datetime.combine(today, parsed_datetime.time())
                        logger.info(f"Combined time with today's date: {parsed_datetime}")
                    
                    # Convert to ISO format that Django expects
                    iso_format = parsed_datetime.isoformat()
                    data['heat_start_time'] = iso_format
                    logger.info(f"Converted to ISO format: {iso_format}")
                    break
                except ValueError as e:
                    logger.debug(f"Format '{fmt}' failed: {e}")
                    continue
            
            if parsed_datetime is None:
                logger.warning(f"Failed to parse datetime '{datetime_str}' with any format")
                # If all parsing attempts failed, let Django handle it and show proper error
                pass
        else:
            logger.info(f"heat_start_time not found or not a string: {data.get('heat_start_time')}")
        
        logger.info(f"Calling super().to_internal_value with data: {data}")
        return super().to_internal_value(data)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])
            if not cow.farm.inseminator:
                raise serializers.ValidationError("No inseminator assigned to this farm")
            if not cow.farm.inseminator.is_active:
                raise serializers.ValidationError("Assigned inseminator is not active")
            data["cow"] = cow
            if 'heat_sign_recorded_at' not in data or data['heat_sign_recorded_at'] is None:
                 data['heat_sign_recorded_at'] = datetime.now()
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow {data['cow_id']} not found in farm {data['farm_id']}")
        except Exception as e:
             raise serializers.ValidationError(f"Validation Error: {str(e)}")


class MonitorPregnancySerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True, help_text="This identifies where the cow belongs (This is initially given to you)")
    cow_id = serializers.CharField(required=True, help_text="Identification number for the cow")
    pregnancy_date = serializers.DateField(required=True, help_text="Date of the pregnancy")
    days_until_calving = serializers.IntegerField(required=True, help_text="The number of days until expected date of calving")
    service_per_conception = serializers.IntegerField(required=True, help_text="Number of service per conception")
    lactation_number = serializers.IntegerField(required=True, help_text="What is the number of lactation for the cow so far?")

    def to_internal_value(self, data):
        """
        Handle field mapping and data conversion
        """
        logger.info(f"MonitorPregnancySerializer received data: {data}")
        
        # Create a copy of data to avoid modifying the original
        processed_data = data.copy()
        
        # Handle potential field name variations
        field_mappings = {
            'farmid': 'farm_id',
            'farm': 'farm_id',
            'cowid': 'cow_id',
            'cow': 'cow_id',
            'Date_of_the_pregnancy': 'pregnancy_date',  # Added exact frontend field name
            'pregnancy': 'pregnancy_date',
            'date_pregnancy': 'pregnancy_date',
            'until_claving': 'days_until_calving',  # Added exact frontend field name
            'days_until_calving_date': 'days_until_calving',
            'days_to_calving': 'days_until_calving',
            'nsc': 'service_per_conception',  # Added exact frontend field name
            'services_per_conception': 'service_per_conception',
            'service_count': 'service_per_conception',
            'lactation_no': 'lactation_number',  # Added exact frontend field name
            'lactation': 'lactation_number',
            'lactation_num': 'lactation_number',
        }
        
        for old_name, new_name in field_mappings.items():
            if old_name in processed_data and new_name not in processed_data:
                processed_data[new_name] = processed_data.pop(old_name)
                logger.info(f"Mapped field {old_name} to {new_name}: {processed_data[new_name]}")
        
        # Handle date parsing if it comes as datetime string
        if 'pregnancy_date' in processed_data:
            pregnancy_date_value = processed_data['pregnancy_date']
            if isinstance(pregnancy_date_value, str):
                try:
                    from datetime import datetime
                    # Try to parse datetime string and extract date
                    if 'T' in pregnancy_date_value:
                        parsed_datetime = datetime.fromisoformat(pregnancy_date_value.replace('Z', '+00:00'))
                        processed_data['pregnancy_date'] = parsed_datetime.date()
                        logger.info(f"Converted datetime to date: {processed_data['pregnancy_date']}")
                except Exception as e:
                    logger.warning(f"Could not parse pregnancy_date: {e}")
                    # Let the normal validation handle it
        
        # Handle numeric fields that might come as strings
        numeric_fields = ['days_until_calving', 'service_per_conception', 'lactation_number']
        for field in numeric_fields:
            if field in processed_data and isinstance(processed_data[field], str):
                try:
                    # Handle decimal values by converting to int
                    processed_data[field] = int(float(processed_data[field]))
                    logger.info(f"Converted {field} to integer: {processed_data[field]}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not convert {field} to integer: {e}")
                    # Let the normal validation handle it
        
        logger.info(f"Processed pregnancy data: {processed_data}")
        return super().to_internal_value(processed_data)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")


class FarmerMedicalAssessmentSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    sickness_description = serializers.CharField(required=True)

    class Meta:
        swagger_schema_fields = {
            "example": {
                "farm_id": "FARM001",
                "cow_id": "COW001",
                "sickness_description": "Reduced appetite and lethargy"
            },
            "request_body": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "farm_id": {
                                    "type": "string",
                                    "description": "Farm identifier"
                                },
                                "cow_id": {
                                    "type": "string",
                                    "description": "Cow identifier"
                                },
                                "sickness_description": {
                                    "type": "string",
                                    "description": "Description of observed health issues"
                                }
                            },
                            "required": ["farm_id", "cow_id", "sickness_description"]
                        }
                    }
                }
            }
        }

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            if not cow.farm.doctor:
                raise serializers.ValidationError("No doctor assigned to this farm")
            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")


class DoctorMedicalAssessmentSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    doctor_id = serializers.IntegerField(required=False)  # Make this optional since we'll use farm.doctor
    is_cow_sick = serializers.BooleanField(required=True)
    sickness_type = serializers.ChoiceField(
        choices=['infectious', 'non_infectious'],
        required=False,
        allow_blank=True
    )
    general_health = serializers.IntegerField(required=True)
    udder_health = serializers.IntegerField(required=True)
    mastitis = serializers.IntegerField(required=True)
    has_lameness = serializers.BooleanField(default=False)
    body_condition_score = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=Decimal('1.0'), # Ensure Decimal type for validation
        max_value=Decimal('5.0'),
        required=True
    )
    reproductive_health = serializers.CharField(required=True)
    metabolic_disease = serializers.CharField(required=False, allow_blank=True)
    
    is_cow_vaccinated = serializers.BooleanField(default=False)
    vaccination_date = serializers.DateField(required=False, allow_null=True)
    vaccination_type = serializers.CharField(required=False, allow_blank=True)
    
    has_deworming = serializers.BooleanField(default=False)
    deworming_date = serializers.DateField(required=False, allow_null=True)
    deworming_type = serializers.CharField(required=False, allow_blank=True)
    
    diagnosis = serializers.CharField(required=False, allow_blank=True)
    treatment = serializers.CharField(required=False, allow_blank=True)
    prescription = serializers.CharField(required=False, allow_blank=True)
    next_assessment_date = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def to_internal_value(self, data):
        """
        Handle field mapping and data conversion from frontend format
        """
        logger.info(f"DoctorMedicalAssessmentSerializer received data: {data}")
        
        # Create a copy of data to avoid modifying the original
        processed_data = data.copy()
        
        # Field mappings
        field_mappings = {
            'cow_sick': 'is_cow_sick',
            'bcs': 'body_condition_score',
            'is_vaccinated': 'is_cow_vaccinated',
        }
        
        for old_name, new_name in field_mappings.items():
            if old_name in processed_data and new_name not in processed_data:
                processed_data[new_name] = processed_data.pop(old_name)
                logger.info(f"Mapped field {old_name} to {new_name}: {processed_data[new_name]}")
        
        # Convert yes/no strings to booleans
        boolean_fields = ['is_cow_sick', 'is_cow_vaccinated', 'has_deworming']
        for field in boolean_fields:
            if field in processed_data and isinstance(processed_data[field], str):
                if processed_data[field].lower() in ['yes', 'yes_sick']:
                    processed_data[field] = True
                elif processed_data[field].lower() in ['no', 'no_sick']:
                    processed_data[field] = False
                logger.info(f"Converted {field} to boolean: {processed_data[field]}")
        
        # Convert deworming field specifically
        if 'deworming' in processed_data:
            processed_data['has_deworming'] = processed_data.pop('deworming').lower() == 'yes'
            logger.info(f"Converted deworming to has_deworming: {processed_data['has_deworming']}")
        
        # Convert health status names to IDs
        health_status_mappings = {
            'general_health': {
                'normal': 'Normal',
                'poor': 'Poor',
                'good': 'Good',
                'excellent': 'Excellent'
            },
            'udder_health': {
                '4qt': '4qt normal',
                '4qt_normal': '4qt normal',
                '3qt': '3qt normal',
                '2qt': '2qt normal',
                '1qt': '1qt normal'
            },
            'mastitis': {
                'clinical_mastitis': 'Clinical mastitis',
                'subclinical_mastitis': 'Subclinical mastitis',
                'no_mastitis': 'No mastitis'
            }
        }
        
        for field, mapping in health_status_mappings.items():
            if field in processed_data and isinstance(processed_data[field], str):
                status_name = mapping.get(processed_data[field].lower(), processed_data[field])
                try:
                    if field == 'general_health':
                        status_obj = GeneralHealthStatus.objects.get(name=status_name)
                    elif field == 'udder_health':
                        status_obj = UdderHealthStatus.objects.get(name=status_name)
                    elif field == 'mastitis':
                        status_obj = MastitisStatus.objects.get(name=status_name)
                    
                    processed_data[field] = status_obj.id
                    logger.info(f"Converted {field} '{processed_data[field]}' to ID: {status_obj.id}")
                except Exception as e:
                    logger.warning(f"Could not find {field} status '{status_name}': {e}")
                    # Try to get the first available status as fallback
                    try:
                        if field == 'general_health':
                            fallback = GeneralHealthStatus.objects.first()
                        elif field == 'udder_health':
                            fallback = UdderHealthStatus.objects.first()
                        elif field == 'mastitis':
                            fallback = MastitisStatus.objects.first()
                        
                        if fallback:
                            processed_data[field] = fallback.id
                            logger.info(f"Using fallback {field} ID: {fallback.id}")
                    except Exception as fallback_error:
                        logger.error(f"Could not get fallback for {field}: {fallback_error}")
        
        # Auto-assign doctor - always use farm's doctor
        try:
            # Get the farm's assigned doctor
            farm = Farm.objects.get(farm_id=processed_data['farm_id'])
            if farm.doctor:
                processed_data['doctor_id'] = farm.doctor.id
                logger.info(f"Using farm's assigned doctor ID: {farm.doctor.id}")
            else:
                # If no doctor assigned to farm, raise an error
                logger.error(f"No doctor assigned to farm {processed_data['farm_id']}")
                raise serializers.ValidationError("No doctor assigned to this farm")
        except Farm.DoesNotExist:
            logger.error(f"Farm {processed_data['farm_id']} not found")
            raise serializers.ValidationError("Farm not found")
        except Exception as e:
            logger.error(f"Error getting farm's doctor: {e}")
            raise serializers.ValidationError("Error retrieving farm's doctor")
        
        logger.info(f"Processed data: {processed_data}")
        return super().to_internal_value(processed_data)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            
            # Use the farm's assigned doctor
            doctor = cow.farm.doctor
            if not doctor:
                raise serializers.ValidationError("No doctor assigned to this farm")

            if not doctor.is_active:
                raise serializers.ValidationError("Farm's assigned doctor is not active")

            if data['is_cow_sick'] and not data.get('sickness_type'):
                raise serializers.ValidationError(
                    "Sickness type is required when cow is sick"
                )

            if data.get('is_cow_vaccinated') and not data.get('vaccination_date'):
                raise serializers.ValidationError(
                    "Vaccination date is required when cow is vaccinated"
                )

            if data.get('has_deworming') and not data.get('deworming_date'):
                raise serializers.ValidationError(
                    "Deworming date is required when cow has deworming"
                )

            data['cow'] = cow
            data['doctor'] = doctor
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")

    class Meta:
        swagger_schema_fields = {
            "example": {
                "farm_id": "FARM001",
                "cow_id": "COW001",
                "doctor_id": 1,
                "is_cow_sick": True,
                "sickness_type": "infectious",
                "general_health": 1,
                "udder_health": 1,
                "mastitis": 1,
                "has_lameness": False,
                "body_condition_score": 3.5,
                "reproductive_health": "Normal cycling",
                "metabolic_disease": "None observed",
                "is_cow_vaccinated": True,
                "vaccination_date": "2024-03-21",
                "vaccination_type": "FMD Vaccine",
                "has_deworming": True,
                "deworming_date": "2024-03-21",
                "deworming_type": "Albendazole",
                "diagnosis": "Mild infection",
                "treatment": "Antibiotics prescribed",
                "prescription": "Medication details",
                "next_assessment_date": "2024-04-21",
                "notes": "Follow up required"
            }
        }


class MonitorHeatSignSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True, help_text="Farm identifier")
    cow_id = serializers.CharField(required=True, help_text="Cow identifier")
    inseminated_now = serializers.CharField(required=True, help_text="Is the cow Inseminated?")
    date_of_insemination = serializers.DateField(required=False, help_text="Date of Insemination")
    insemination_number = serializers.CharField(required=True, help_text="How many times was the cow Inseminated so far?")
    lactation_no = serializers.CharField(required=True, help_text="What is the lactation number for the cow?")

    def to_internal_value(self, data):
        """
        Handle field mapping and data conversion
        """
        logger.info(f"MonitorHeatSignSerializer received data: {data}")
        
        # Create a copy of data to avoid modifying the original
        processed_data = data.copy()
        
        # Handle potential field name variations
        field_mappings = {
            'insemination_date': 'date_of_insemination',
            'inseminated_date': 'date_of_insemination',
            'date_insemination': 'date_of_insemination',
            'Date_of_Insemination': 'date_of_insemination',  # Added this mapping
        }
        
        for old_name, new_name in field_mappings.items():
            if old_name in processed_data and new_name not in processed_data:
                processed_data[new_name] = processed_data.pop(old_name)
                logger.info(f"Mapped field {old_name} to {new_name}: {processed_data[new_name]}")
        
        # Special handling: If we have both date and time in separate fields, combine them
        if 'date_of_insemination' in processed_data and 'inseminated_time' in processed_data:
            try:
                from datetime import datetime, date
                
                # Parse the date
                if isinstance(processed_data['date_of_insemination'], str):
                    insemination_date = datetime.strptime(processed_data['date_of_insemination'], '%Y-%m-%d').date()
                else:
                    insemination_date = processed_data['date_of_insemination']
                
                # Parse the time (keeping only the date, ignoring time for DateField)
                # Since date_of_insemination is a DateField, we only need the date part
                processed_data['date_of_insemination'] = insemination_date
                
                # Remove the time field since we don't need it for the DateField
                processed_data.pop('inseminated_time', None)
                
                logger.info(f"Combined date and time into date_of_insemination: {processed_data['date_of_insemination']}")
                
            except Exception as e:
                logger.error(f"Error combining date and time fields: {e}")
                # If parsing fails, let the normal validation handle it
        
        return super().to_internal_value(processed_data)

    def validate(self, data):
        try:
            data['is_inseminated'] = data['inseminated_now'].lower() == 'yes'
            data['insemination_count'] = int(data['insemination_number'])
            data['lactation_number'] = int(data['lactation_no'])

            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            
            if not cow.farm.inseminator:
                raise serializers.ValidationError("No inseminator assigned to this farm")
                
            if not cow.farm.inseminator.is_active:
                raise serializers.ValidationError("Assigned inseminator is not active")

            # If cow is inseminated, date_of_insemination should be provided
            if data['is_inseminated'] and not data.get('date_of_insemination'):
                raise serializers.ValidationError("Date of insemination is required when cow is inseminated")

            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
        except ValueError:
            raise serializers.ValidationError("Invalid number format for insemination count or lactation number")


class MonitorBirthSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True, help_text="This identifies where the cow belongs (This is initially given to you)")
    cow_id = serializers.CharField(required=True, help_text="Identification number for the cow")
    calving_date = serializers.DateField(required=True, help_text="Date of Calving")
    last_calving_date = serializers.DateField(required=True, help_text="Date of last calving")
    calf_sex = serializers.ChoiceField(choices=['M', 'F'], required=True, help_text="What is the Sex of the Calf?")

    def to_internal_value(self, data):
        """
        Handle field mapping and data conversion
        """
        logger.info(f"MonitorBirthSerializer received data: {data}")
        
        # Create a copy of data to avoid modifying the original
        processed_data = data.copy()
        
        # Handle potential field name variations
        field_mappings = {
            'farmid': 'farm_id',
            'farm': 'farm_id',
            'cowid': 'cow_id',
            'cow': 'cow_id',
            'calving': 'calving_date',
            'birth_date': 'calving_date',
            'date_of_calving': 'calving_date',
            'Date_of_Calving': 'calving_date',  # Added exact frontend field name
            'last_calving': 'last_calving_date',
            'previous_calving_date': 'last_calving_date',
            'Date_of_last_calving': 'last_calving_date',  # Added exact frontend field name
            'sex': 'calf_sex',
            'calf_gender': 'calf_sex',
            'gender': 'calf_sex',
            'What_is_the_Sex_of_the_Calf': 'calf_sex',  # Added exact frontend field name
        }
        
        for old_name, new_name in field_mappings.items():
            if old_name in processed_data and new_name not in processed_data:
                processed_data[new_name] = processed_data.pop(old_name)
                logger.info(f"Mapped field {old_name} to {new_name}: {processed_data[new_name]}")
        
        # Handle sex field normalization
        if 'calf_sex' in processed_data:
            sex_value = str(processed_data['calf_sex']).upper()
            if sex_value in ['MALE', 'BULL', 'BOY']:
                processed_data['calf_sex'] = 'M'
            elif sex_value in ['FEMALE', 'COW', 'GIRL']:
                processed_data['calf_sex'] = 'F'
            logger.info(f"Normalized calf_sex to: {processed_data['calf_sex']}")
        
        logger.info(f"Processed birth data: {processed_data}")
        return super().to_internal_value(processed_data)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
