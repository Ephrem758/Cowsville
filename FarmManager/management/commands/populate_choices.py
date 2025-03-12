from django.core.management.base import BaseCommand
from FarmManager.models import (
    HousingType, FloorType, WaterSource, FeedingFrequency,
    BreedType, GynecologicalStatus, UdderHealthStatus,
    MastitisStatus, GeneralHealthStatus
)

class Command(BaseCommand):
    help = 'Populate choice models with initial data'

    def handle(self, *args, **kwargs):
        # Housing Types
        housing_types = [
            ("freestall", "Free Stall"),
            ("tiestall", "Tie Stall"),
            ("traditional", "Traditional"),
        ]
        for name, display_name in housing_types:
            HousingType.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created housing types'))

        # Floor Types
        floor_types = [
            ("concrete", "Concrete"),
            ("stone", "Stone"),
            ("soil", "Soil"),
            ("mat_bedding", "Mat/Other Bedding"),
        ]
        for name, display_name in floor_types:
            FloorType.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created floor types'))

        # Water Sources
        water_sources = [
            ("tap_water", "Tap Water"),
            ("wells", "Wells"),
        ]
        for name, display_name in water_sources:
            WaterSource.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created water sources'))

        # Feeding Frequencies
        feeding_frequencies = [
            ("once", "Once Daily"),
            ("twice", "Twice Daily"),
            ("thrice", "Three Times Daily"),
        ]
        for name, display_name in feeding_frequencies:
            FeedingFrequency.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created feeding frequencies'))

        # Breed Types
        breed_types = [
            ("hf", "HF"),
            ("zebu", "Zebu"),
            ("hf_zebu_cross", "HF*Zebu Cross"),
            ("other", "Other"),
        ]
        for name, display_name in breed_types:
            BreedType.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created breed types'))

        # Gynecological Status
        gynecological_statuses = [
            ("estrus", "Estrus"),
            ("ai", "AI"),
            ("pregnant", "Pregnant"),
            ("abortion", "Abortion"),
            ("fresh", "Fresh"),
            ("birth", "Birth"),
        ]
        for name, display_name in gynecological_statuses:
            GynecologicalStatus.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created gynecological statuses'))

        # Udder Health Status
        udder_health_statuses = [
            ("4qt_normal", "4qt Normal"),
            ("3qt_normal", "3qt Normal"),
            ("2qt_normal", "2qt Normal"),
            ("1qt_normal", "1qt Normal"),
        ]
        for name, display_name in udder_health_statuses:
            UdderHealthStatus.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created udder health statuses'))

        # Mastitis Status
        mastitis_statuses = [
            ("negative", "Negative"),
            ("clinical_mastitis", "Clinical Mastitis"),
            ("cmt_plus", "CMT +"),
            ("cmt_plus_plus", "CMT ++"),
            ("cmt_plus_plus_plus", "CMT +++"),
        ]
        for name, display_name in mastitis_statuses:
            MastitisStatus.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created mastitis statuses'))

        # General Health Status
        general_health_statuses = [
            ("normal", "Normal"),
            ("sick", "Sick"),
        ]
        for name, display_name in general_health_statuses:
            GeneralHealthStatus.objects.get_or_create(name=name, display_name=display_name)
        self.stdout.write(self.style.SUCCESS('Successfully created general health statuses'))

        self.stdout.write(self.style.SUCCESS('All choice models have been populated successfully')) 