from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    FarmViewSet, CowViewSet, HealthViewSet, ReproductionViewSet,
    DoctorViewSet, InseminatorViewSet, MessageViewSet,
    BreedTypeViewSet, HousingTypeViewSet, FloorTypeViewSet,
    FeedingFrequencyViewSet, WaterSourceViewSet,
    GynecologicalStatusViewSet, UdderHealthStatusViewSet,
    MastitisStatusViewSet, GeneralHealthStatusViewSet
)

router = DefaultRouter()

# Main model endpoints
router.register(r'farms', FarmViewSet)
router.register(r'cows', CowViewSet)
router.register(r'health', HealthViewSet)
router.register(r'reproduction', ReproductionViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'inseminators', InseminatorViewSet)
router.register(r'messages', MessageViewSet)

# Choice model endpoints
router.register(r'breedtypes', BreedTypeViewSet)
router.register(r'housingtypes', HousingTypeViewSet)
router.register(r'floortypes', FloorTypeViewSet)
router.register(r'feedingfrequencies', FeedingFrequencyViewSet)
router.register(r'watersources', WaterSourceViewSet)
router.register(r'gynecologicalstatuses', GynecologicalStatusViewSet)
router.register(r'udderhealthstatuses', UdderHealthStatusViewSet)
router.register(r'mastitisstatuses', MastitisStatusViewSet)
router.register(r'generalhealthstatuses', GeneralHealthStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
