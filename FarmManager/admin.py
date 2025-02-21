from django.contrib import admin
from .models import (
    Farm, Cow, Health, Reproduction,
    HousingType, FloorType, FeedingFrequency, WaterSource,
    BreedType, GynecologicalStatus, UdderHealthStatus,
    MastitisStatus, GeneralHealthStatus, Message,
    Inseminator
)

# Register all models
admin.site.register(Farm)
admin.site.register(Cow)
admin.site.register(Health)
admin.site.register(Reproduction)

# Register choice models
admin.site.register(HousingType)
admin.site.register(FloorType)
admin.site.register(FeedingFrequency)
admin.site.register(WaterSource)
admin.site.register(BreedType)
admin.site.register(GynecologicalStatus)
admin.site.register(UdderHealthStatus)
admin.site.register(MastitisStatus)
admin.site.register(GeneralHealthStatus)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('farm', 'cow', 'message_type', 'sent_date', 'is_sent')
    list_filter = ('message_type', 'is_sent', 'sent_date')
    search_fields = ('farm__farm_id', 'cow__cow_id', 'message_text')

@admin.register(Inseminator)
class InseminatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone_number', 'address')
