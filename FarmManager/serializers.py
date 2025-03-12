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


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"


class CowSerializer(serializers.ModelSerializer):
    farm_id = serializers.CharField(write_only=True)
    body_weight = serializers.DecimalField(max_digits=6, decimal_places=2)
    bcs = serializers.DecimalField(max_digits=2, decimal_places=1)
    average_daily_milk = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Cow
        fields = [
            'farm_id',
            'cow_id',
            'breed',
            'age_in_days',
            'sex',
            'parity',
            'body_weight',
            'bcs',
            'gynecological_status',
            'lactation_number',
            'days_in_milk',
            'average_daily_milk',
            'cow_inseminated_before',
            'last_date_insemination',
            'number_of_inseminations',
            'id_or_breed_bull_used',
            'last_calving_date'
        ]
        swagger_schema_fields = {
            "example": {
                "farm_id": "FARM001",
                "cow_id": "COW001",
                "breed": 1,
                "age_in_days": 730,
                "sex": "F",
                "parity": 2,
                "body_weight": "450.00",
                "bcs": "3.5",
                "gynecological_status": 1,
                "lactation_number": 1,
                "days_in_milk": 150,
                "average_daily_milk": "40.00",
                "cow_inseminated_before": False,
                "last_date_insemination": None,
                "number_of_inseminations": 0,
                "id_or_breed_bull_used": "",
                "last_calving_date": None
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['farm_id'] = instance.farm.farm_id
        return data

    def create(self, validated_data):
        farm_id = validated_data.pop('farm_id')
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            validated_data['farm'] = farm
            return super().create(validated_data)
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
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    is_pregnant = serializers.BooleanField(required=True)
    lactation_number = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        swagger_schema_fields = {
            "example": {
                "farm_id": "FARM001",
                "cow_id": "COW001",
                "is_pregnant": True,
                "lactation_number": 2
            }
        }

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
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    is_inseminated = serializers.BooleanField(required=False)
    inseminated_now = serializers.CharField(required=False)
    inseminated_time = serializers.CharField(required=False)
    insemination_time = serializers.TimeField(required=False, allow_null=True)
    insemination_count = serializers.IntegerField(required=False, min_value=0)
    insemination_number = serializers.CharField(required=False)
    lactation_number = serializers.IntegerField(required=False, min_value=0)
    lactation_no = serializers.CharField(required=False)

    def validate(self, data):
        try:
            if 'inseminated_now' in data:
                data['is_inseminated'] = data['inseminated_now'].lower() == 'yes'
            
            if 'inseminated_time' in data:
                time_str = data['inseminated_time'].split('.')[0]
                data['insemination_time'] = time_str
            
            if 'insemination_number' in data:
                data['insemination_count'] = int(data['insemination_number'])
            
            if 'lactation_no' in data:
                data['lactation_number'] = int(data['lactation_no'])

            if 'is_inseminated' not in data:
                raise serializers.ValidationError("Either is_inseminated or inseminated_now is required")
            if 'lactation_number' not in data:
                raise serializers.ValidationError("Either lactation_number or lactation_no is required")

            cow = Cow.objects.get(farm__farm_id=data['farm_id'], cow_id=data['cow_id'])
            
            if not cow.farm.inseminator:
                raise serializers.ValidationError("No inseminator assigned to this farm")
                
            if not cow.farm.inseminator.is_active:
                raise serializers.ValidationError("Assigned inseminator is not active")

            if data['is_inseminated']:
                if not data.get('insemination_time') and not data.get('inseminated_time'):
                    raise serializers.ValidationError(
                        "Insemination time is required when cow is inseminated"
                    )
                if not data.get('insemination_count'):
                    raise serializers.ValidationError(
                        "Insemination count is required when cow is inseminated"
                    )

            data['cow'] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
