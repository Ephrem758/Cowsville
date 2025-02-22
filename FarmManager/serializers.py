from rest_framework import serializers
from .models import Farm, Cow, Message, Inseminator, Health, Reproduction, BreedType, HousingType, FloorType, FeedingFrequency, WaterSource, GynecologicalStatus, UdderHealthStatus, MastitisStatus, GeneralHealthStatus

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class InseminatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inseminator
        fields = '__all__'

class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = '__all__'

class ReproductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reproduction
        fields = '__all__'

# Choice Model Serializers
class BreedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedType
        fields = ['id', 'name', 'display_name']

class HousingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingType
        fields = ['id', 'name', 'display_name']

class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        fields = ['id', 'name', 'display_name']

class FeedingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingFrequency
        fields = ['id', 'name', 'display_name']

class WaterSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSource
        fields = ['id', 'name', 'display_name']

class GynecologicalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GynecologicalStatus
        fields = ['id', 'name', 'display_name']

class UdderHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdderHealthStatus
        fields = ['id', 'name', 'display_name']

class MastitisStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MastitisStatus
        fields = ['id', 'name', 'display_name']

class GeneralHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHealthStatus
        fields = ['id', 'name', 'display_name'] 