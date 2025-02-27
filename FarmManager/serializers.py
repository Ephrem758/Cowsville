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


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


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


class PregnancyMonitorSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    is_pregnant = serializers.BooleanField(required=True)
    lactation_number = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])
            data["cow"] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")


class FarmerMedicalAssessmentSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    sickness_description = serializers.CharField(required=True)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])
            if not cow.farm.doctor:
                raise serializers.ValidationError("No doctor assigned to this farm")
            if not cow.farm.doctor.is_active:
                raise serializers.ValidationError("Assigned doctor is not active")
            data["cow"] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")


class DoctorAssessmentSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    doctor_id = serializers.IntegerField(required=True)
    is_cow_sick = serializers.BooleanField(required=True)
    general_health = serializers.IntegerField(required=True)
    udder_health = serializers.IntegerField(required=True)
    mastitis = serializers.IntegerField(required=True)
    body_condition_score = serializers.DecimalField(
        max_digits=3, decimal_places=1, required=True
    )
    reproductive_health = serializers.CharField(required=True)
    metabolic_disease = serializers.CharField(required=False, allow_blank=True)

    # Optional fields
    sickness_type = serializers.CharField(required=False, allow_blank=True)
    is_cow_vaccinated = serializers.BooleanField(required=False)
    vaccination_date = serializers.DateField(required=False, allow_null=True)
    vaccination_type = serializers.CharField(required=False, allow_blank=True)
    has_deworming = serializers.BooleanField(required=False)
    deworming_date = serializers.DateField(required=False, allow_null=True)
    deworming_type = serializers.CharField(required=False, allow_blank=True)
    diagnosis = serializers.CharField(required=False, allow_blank=True)
    treatment = serializers.CharField(required=False, allow_blank=True)
    prescription = serializers.CharField(required=False, allow_blank=True)
    next_assessment_date = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])
            doctor = Doctor.objects.get(id=data["doctor_id"])

            if not doctor.is_active:
                raise serializers.ValidationError("Doctor is not active")

            if data["is_cow_sick"] and not data.get("sickness_type"):
                raise serializers.ValidationError(
                    "Sickness type is required when cow is sick"
                )

            data["cow"] = cow
            data["doctor"] = doctor
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found")


class HeatSignMonitorSerializer(serializers.Serializer):
    farm_id = serializers.CharField(required=True)
    cow_id = serializers.CharField(required=True)
    is_inseminated = serializers.BooleanField(required=True)
    insemination_time = serializers.TimeField(required=False, allow_null=True)
    insemination_count = serializers.IntegerField(required=False, allow_null=True)
    lactation_number = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            cow = Cow.objects.get(farm__farm_id=data["farm_id"], cow_id=data["cow_id"])

            if not cow.farm.inseminator:
                raise serializers.ValidationError(
                    "No inseminator assigned to this farm"
                )

            if not cow.farm.inseminator.is_active:
                raise serializers.ValidationError("Assigned inseminator is not active")

            if data["is_inseminated"] and not data.get("insemination_time"):
                raise serializers.ValidationError(
                    "Insemination time is required when cow is inseminated"
                )

            data["cow"] = cow
            return data
        except Cow.DoesNotExist:
            raise serializers.ValidationError("Cow not found")
