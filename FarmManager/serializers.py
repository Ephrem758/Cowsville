from rest_framework import serializers
from .models import (
    Farm, Cow, Doctor, Inseminator, Message,
    BreedType, HousingType, FloorType, FeedingFrequency,
    WaterSource, GynecologicalStatus, UdderHealthStatus,
    MastitisStatus, GeneralHealthStatus, MedicalAssessment,
    InseminationRecord, FarmerMedicalReport
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