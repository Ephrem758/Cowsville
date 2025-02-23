from django.contrib import admin
from .models import (
    Farm, Cow, Doctor, Inseminator, Message,
    BreedType, HousingType, FloorType,
    FeedingFrequency, WaterSource,
    GynecologicalStatus, UdderHealthStatus,
    MastitisStatus, GeneralHealthStatus,
    MedicalAssessment, InseminationRecord,
    FarmerMedicalReport
)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('farm_id', 'owner_name', 'telephone_number', 'doctor', 'inseminator')
    search_fields = ('farm_id', 'owner_name', 'address')
    list_filter = ('type_of_housing', 'type_of_floor', 'source_of_water')

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('cow_id', 'farm', 'breed', 'age_in_days', 'sex')
    search_fields = ('cow_id', 'farm__farm_id')
    list_filter = ('breed', 'sex', 'gynecological_status')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_active', 'license_number')
    search_fields = ('name', 'phone_number', 'license_number')
    list_filter = ('is_active',)

@admin.register(Inseminator)
class InseminatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_active')
    search_fields = ('name', 'phone_number')
    list_filter = ('is_active',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('farm', 'cow', 'message_type', 'sent_date', 'is_sent')
    search_fields = ('farm__farm_id', 'cow__cow_id', 'message_text')
    list_filter = ('message_type', 'is_sent', 'sent_date')

@admin.register(MedicalAssessment)
class MedicalAssessmentAdmin(admin.ModelAdmin):
    list_display = ('farm', 'cow', 'assessed_by', 'assessment_date', 'is_cow_sick')
    search_fields = ('farm__farm_id', 'cow__cow_id', 'assessed_by__name')
    list_filter = ('is_cow_sick', 'sickness_type', 'is_cow_vaccinated', 'has_deworming')
    date_hierarchy = 'assessment_date'

@admin.register(InseminationRecord)
class InseminationRecordAdmin(admin.ModelAdmin):
    list_display = ('farm', 'cow', 'inseminator', 'is_inseminated', 'recorded_date')
    search_fields = ('farm__farm_id', 'cow__cow_id', 'inseminator__name')
    list_filter = ('is_inseminated',)
    date_hierarchy = 'recorded_date'

@admin.register(FarmerMedicalReport)
class FarmerMedicalReportAdmin(admin.ModelAdmin):
    list_display = ('farm', 'cow', 'reported_date', 'is_reviewed')
    search_fields = ('farm__farm_id', 'cow__cow_id', 'sickness_description')
    list_filter = ('is_reviewed',)
    date_hierarchy = 'reported_date'

# Register choice models
admin.site.register(BreedType)
admin.site.register(HousingType)
admin.site.register(FloorType)
admin.site.register(FeedingFrequency)
admin.site.register(WaterSource)
admin.site.register(GynecologicalStatus)
admin.site.register(UdderHealthStatus)
admin.site.register(MastitisStatus)
admin.site.register(GeneralHealthStatus)
