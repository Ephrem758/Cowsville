from django.contrib import admin
from .models import Farm, Cow, Health, Reproduction

# Register your models here.
admin.site.register(Farm)
admin.site.register(Cow)
admin.site.register(Health)
admin.site.register(Reproduction)
