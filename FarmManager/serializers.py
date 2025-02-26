from rest_framework import serializers
from .models import (
    Farm, Cow, Doctor, Inseminator, Message,
    BreedType, HousingType, FloorType, FeedingFrequency,
    WaterSource, GynecologicalStatus, UdderHealthStatus,
    MastitisStatus, GeneralHealthStatus, MedicalAssessment,
    InseminationRecord, FarmerMedicalReport, Reproduction
)

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class InseminatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inseminator
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MedicalAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAssessment
        fields = '__all__'

class InseminationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InseminationRecord
        fields = '__all__'

class FarmerMedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerMedicalReport
        fields = '__all__'

# Choice model serializers
class BreedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedType
        fields = '__all__'

class HousingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingType
        fields = '__all__'

class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        fields = '__all__'

class FeedingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingFrequency
        fields = '__all__'

class WaterSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSource
        fields = '__all__'

class GynecologicalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GynecologicalStatus
        fields = '__all__'

class UdderHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdderHealthStatus
        fields = '__all__'

class MastitisStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MastitisStatus
        fields = '__all__'

class GeneralHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHealthStatus
        fields = '__all__'

class ReproductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reproduction
        fields = '__all__' 
        

class StaffAssignmentSerializer(serializers.ModelSerializer):
    staff_id = serializers.IntegerField(required=True)
    
    class Meta:
        abstract = True
        
    def validate(self, attrs):
        return NotImplementedError("child classes must implement this method")


class InseminatorAssignmentSerializer(StaffAssignmentSerializer):
    staff_id = serializers.IntegerField(required=True, source='inseminator_id')

    def validate_staff_id(self, value):
        try:
            inseminator = Inseminator.objects.get(id=value)
            if not inseminator.is_active:
                raise serializers.ValidationError("Inseminator is not active")
            return value
        except Inseminator.DoesNotExist:
            raise serializers.ValidationError("Inseminator Not Found")


class DoctorAssignmentSerializer(StaffAssignmentSerializer):
    staff_id = serializers.IntegerField(required=True, source='doctor_id')

    def validate_staff_id(self, value):
        try:
            doctor = Doctor.objects.get(id=value)
            if not doctor.is_active:
                raise serializers.ValidationError("Doctor is not active")
            return value
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor Not Found")
