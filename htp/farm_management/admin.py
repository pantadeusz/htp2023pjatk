from django.contrib import admin
from .models import Farm, FarmActivity, Measurement, Enum


# Register your models here.
admin.site.register(Farm)
admin.site.register(FarmActivity)
admin.site.register(Measurement)
admin.site.register(Enum)
