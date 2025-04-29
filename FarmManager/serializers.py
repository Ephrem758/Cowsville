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
from decimal import Decimal
from datetime import datetime


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['farm_id', 'owner_name', 'address', 'telephone_number']


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
    # Use PrimaryKeyRelatedField for inputting related objects by ID
    breed = serializers.PrimaryKeyRelatedField(queryset=BreedType.objects.all())
    gynecological_status = serializers.PrimaryKeyRelatedField(queryset=GynecologicalStatus.objects.all())
    # ... include other writable fields ...
    class Meta:
        model = Cow
        fields = [
             'farm_id_input', 'cow_id_input', 'breed', 'date_of_birth', 'sex', 'parity', 
             'body_weight', 'bcs', 'gynecological_status', 'lactation_number', 
             'days_in_milk', 'average_daily_milk', 'cow_inseminated_before', 
             'last_date_insemination', 'number_of_inseminations', 'id_or_breed_bull_used', 
             'last_calving_date', 'has_lameness', 'reproductive_health', 'metabolic_disease',
             'is_vaccinated', 'vaccination_date', 'vaccination_type', 'has_deworming',
             'deworming_date', 'deworming_type'
             # Add other writable fields as needed
        ]
        
    def create(self, validated_data):
         # Pop the input-only fields before calling super().create
        farm_id = validated_data.pop('farm_id', None) 
        cow_id = validated_data.pop('cow_id', None) 

        if not farm_id:
             raise serializers.ValidationError({'farm_id_input': 'This field is required.'})

        try:
            farm = Farm.objects.get(farm_id=farm_id)
            validated_data['farm'] = farm
            if cow_id:
                 validated_data['cow_id'] = cow_id
            
            # Create the cow instance
            instance = super().create(validated_data)
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


class InseminatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inseminator
        fields = "__all__"


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
    doctor_id = serializers.IntegerField(required=True)
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

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            doctor = Doctor.objects.get(id=data['doctor_id'])

            if not doctor.is_active:
                raise serializers.ValidationError("Doctor is not active")

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
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found")


class MonitorHeatSignSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True, help_text="Farm identifier")
    cow_id = serializers.CharField(required=True, help_text="Cow identifier")
    inseminated_now = serializers.CharField(required=True, help_text="Is the cow Inseminated?")
    date_of_insemination = serializers.DateField(required=True, help_text="Date of Insemination")
    insemination_number = serializers.CharField(required=True, help_text="How many times was the cow Inseminated so far?")
    lactation_no = serializers.CharField(required=True, help_text="What is the lactation number for the cow?")

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

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
