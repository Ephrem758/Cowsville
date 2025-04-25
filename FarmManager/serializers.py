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
        fields = "__all__"


class CowSerializer(serializers.ModelSerializer):
    farm_id = serializers.CharField(write_only=True)
    cow_id = serializers.CharField(write_only=True)
    breed = serializers.PrimaryKeyRelatedField(queryset=BreedType.objects.all())
    other_breed = serializers.CharField(write_only=True, required=False)
    cow_age = serializers.IntegerField(write_only=True, source='age_in_days')
    sex = serializers.CharField(write_only=True)
    parity = serializers.IntegerField(write_only=True)
    body_weight = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True)
    bcs = serializers.DecimalField(max_digits=2, decimal_places=1, write_only=True)
    gyn_status = serializers.CharField(write_only=True, source='gynecological_status')
    lactation_no = serializers.IntegerField(write_only=True, source='lactation_number')
    milk_days = serializers.IntegerField(write_only=True, source='days_in_milk')
    daily_milk = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True, source='average_daily_milk')
    inseminated_before = serializers.BooleanField(write_only=True)
    ai_date = serializers.DateField(write_only=True, source='last_date_insemination', input_formats=['%Y-%m-%d', '%b %d, %Y'])
    insemination_no = serializers.IntegerField(write_only=True, source='number_of_inseminations')
    sire_breed = serializers.CharField(write_only=True, source='id_or_breed_bull_used')
    after_calving = serializers.IntegerField(write_only=True, source='days_after_last_calving')
    is_pregnant = serializers.BooleanField(write_only=True)
    until_claving = serializers.IntegerField(write_only=True, source='days_until_calving')
    heat_shown = serializers.BooleanField(write_only=True, required=False)
    heat_start_date = serializers.DateField(write_only=True, required=False)
    heat_end_date = serializers.DateField(write_only=True, required=False)
    heat_signs = serializers.CharField(write_only=True, required=False)
    nsc = serializers.IntegerField(write_only=True, source='service_per_conception')
    udder_health = serializers.CharField(write_only=True)
    mastitis = serializers.CharField(write_only=True)
    general_health = serializers.CharField(write_only=True)
    reproductive_health = serializers.CharField(write_only=True)
    other_reproductive_health = serializers.CharField(write_only=True, required=False)
    metabolic_disease = serializers.CharField(write_only=True)
    other_metabolic_disease = serializers.CharField(write_only=True, required=False)
    is_vaccinated = serializers.BooleanField(write_only=True)
    vaccination_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d', '%b %d, %Y'])
    vaccination_type = serializers.CharField(write_only=True)
    deworming = serializers.BooleanField(write_only=True)
    deworming_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d', '%b %d, %Y'])
    deworming_type = serializers.CharField(write_only=True)

    class Meta:
        model = Cow
        fields = [
            'farm_id', 'cow_id', 'breed', 'other_breed', 'cow_age', 'sex', 'parity', 
            'body_weight', 'bcs', 'gyn_status', 'lactation_no', 'milk_days', 'daily_milk', 
            'inseminated_before', 'ai_date', 'insemination_no', 'sire_breed', 'after_calving', 
            'is_pregnant', 'until_claving', 'heat_shown', 'heat_start_date', 'heat_end_date', 
            'heat_signs', 'nsc', 'udder_health', 'mastitis', 'general_health', 
            'reproductive_health', 'other_reproductive_health', 'metabolic_disease', 
            'other_metabolic_disease', 'is_vaccinated', 'vaccination_date', 
            'vaccination_type', 'deworming', 'deworming_date', 'deworming_type'
        ]
        swagger_schema_fields = {
            "example": {
                "farm_id": "12",
                "cow_id": "34",
                "breed": "HF",
                "cow_age": 34,
                "sex": "F",
                "parity": 6,
                "body_weight": "350.0",
                "bcs": "3",
                "gyn_status": "AI",
                "lactation_number": 6,
                "days_in_milk": 2,
                "daily_milk": "10.0",
                "cow_inseminated_before": True,
                "last_date_insemination": "2024-11-21",
                "number_of_inseminations": 2,
                "id_or_breed_bull_used": "345",
                "last_calving_date": None,
                "is_pregnant": True,
                "until_calving": 6,
                "heat_shown": False,
                "heat_start_date": None,
                "heat_end_date": None,
                "heat_signs": None,
                "service_per_conception": 3,
                "reproductive_health": "Abortion",
                "metabolic_disease": "Hypocalcemia",
                "udder_health": "4qt normal",
                "mastitis": "Clinical mastitis",
                "general_health": "Normal",
                "is_vaccinated": True,
                "vaccination_date": "2024-11-05",
                "vaccination_type": "LSD",
                "deworming": True,
                "deworming_date": "2024-11-10",
                "deworming_type": "Albendazole"
            }
        }

    def validate_sex(self, value):
        """Convert 'Milking Cow' to 'F' for female"""
        if value.lower() == 'milking cow':
            return 'F'
        return value.upper()

    def validate_breed(self, value):
        """Handle breed name to ID conversion"""
        try:
            if isinstance(value, str):
                # Try exact match first
                try:
                    breed = BreedType.objects.get(name__iexact=value)
                    return breed.id
                except BreedType.DoesNotExist:
                    # Try common variations
                    breed_map = {
                        'hf': 'hf',
                        'holstein': 'hf',
                        'holstein friesian': 'hf',
                        'zebu': 'zebu',
                        'cross': 'hf_zebu_cross',
                        'crossbreed': 'hf_zebu_cross',
                        'other': 'other'
                    }
                    normalized_value = value.lower().strip()
                    if normalized_value in breed_map:
                        breed = BreedType.objects.get(name=breed_map[normalized_value])
                        return breed.id
                    raise serializers.ValidationError(
                        f"Invalid breed type. Valid options are: HF, Zebu, HF*Zebu Cross, Other"
                    )
            return value
        except BreedType.DoesNotExist:
            raise serializers.ValidationError(
                f"Invalid breed type. Valid options are: HF, Zebu, HF*Zebu Cross, Other"
            )

    def validate_gyn_status(self, value):
        """Handle gynecological status name to ID conversion"""
        try:
            if isinstance(value, str):
                # Try exact match first
                try:
                    status = GynecologicalStatus.objects.get(name__iexact=value)
                    return status.id
                except GynecologicalStatus.DoesNotExist:
                    # Try common variations
                    status_map = {
                        'estrus': 'estrus',
                        'heat': 'estrus',
                        'ai': 'ai',
                        'artificial insemination': 'ai',
                        'pregnant': 'pregnant',
                        'pregnancy': 'pregnant',
                        'abortion': 'abortion',
                        'fresh': 'fresh',
                        'birth': 'birth',
                        'calving': 'birth'
                    }
                    normalized_value = value.lower().strip()
                    if normalized_value in status_map:
                        status = GynecologicalStatus.objects.get(name=status_map[normalized_value])
                        return status.id
                    raise serializers.ValidationError(
                        f"Invalid gynecological status. Valid options are: Estrus, AI, Pregnant, Abortion, Fresh, Birth"
                    )
            return value
        except GynecologicalStatus.DoesNotExist:
            raise serializers.ValidationError(
                f"Invalid gynecological status. Valid options are: Estrus, AI, Pregnant, Abortion, Fresh, Birth"
            )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['farm_id'] = instance.farm.farm_id
        return data

    def create(self, validated_data):
        farm_id = validated_data.pop('farm_id')
        
        # Remove additional fields that aren't part of the Cow model
        reproduction_data = {
            'is_pregnant': validated_data.pop('is_pregnant', False),
            'until_calving': validated_data.pop('until_calving', None),
            'heat_shown': validated_data.pop('heat_shown', False),
            'heat_start_date': validated_data.pop('heat_start_date', None),
            'heat_end_date': validated_data.pop('heat_end_date', None),
            'heat_signs': validated_data.pop('heat_signs', None),
            'service_per_conception': validated_data.pop('service_per_conception', None)
        }
        
        medical_data = {
            'reproductive_health': validated_data.pop('reproductive_health', 'Normal'),
            'metabolic_disease': validated_data.pop('metabolic_disease', 'Normal'),
            'udder_health': validated_data.pop('udder_health', '4qt normal'),
            'mastitis': validated_data.pop('mastitis', 'Negative'),
            'general_health': validated_data.pop('general_health', 'Normal'),
            'is_vaccinated': validated_data.pop('is_vaccinated', False),
            'vaccination_date': validated_data.pop('vaccination_date', None),
            'vaccination_type': validated_data.pop('vaccination_type', None),
            'deworming': validated_data.pop('deworming', False),
            'deworming_date': validated_data.pop('deworming_date', None),
            'deworming_type': validated_data.pop('deworming_type', None)
        }
        
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            validated_data['farm'] = farm
            instance = super().create(validated_data)
            
            # Add the data back to validated_data for the ViewSet to use
            validated_data.update(reproduction_data)
            validated_data.update(medical_data)
            
            return instance
        except Farm.DoesNotExist:
            raise serializers.ValidationError({'farm_id': f'Farm with ID {farm_id} not found'})


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


# Choice model serializers
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
    heat_signs = serializers.CharField(required=False, default="")
    heat_start_time = serializers.DateTimeField(required=True)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])
            if not cow.farm.inseminator:
                raise serializers.ValidationError(
                    "No inseminator assigned to this farm"
                )
            if not cow.farm.inseminator.is_active:
                raise serializers.ValidationError("Assigned inseminator is not active")
            data["cow"] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")


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
    body_condition_score = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=1.0,
        max_value=5.0,
        required=True
    )
    reproductive_health = serializers.CharField(required=True)
    metabolic_disease = serializers.CharField(required=False, allow_blank=True)
    
    # Vaccination fields
    is_cow_vaccinated = serializers.BooleanField(default=False)
    vaccination_date = serializers.DateField(required=False, allow_null=True)
    vaccination_type = serializers.CharField(required=False, allow_blank=True)
    
    # Deworming fields
    has_deworming = serializers.BooleanField(default=False)
    deworming_date = serializers.DateField(required=False, allow_null=True)
    deworming_type = serializers.CharField(required=False, allow_blank=True)
    
    # Assessment details
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
            # Convert yes/no to boolean
            data['is_inseminated'] = data['inseminated_now'].lower() == 'yes'
            
            # Convert string numbers to integers
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
