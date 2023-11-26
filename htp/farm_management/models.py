from django.db import models
from enum import Enum

class Farm(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    total_area = models.FloatField()
    compliance_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FarmActivity(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    area_covered = models.FloatField()
    details = models.TextField()

    def __str__(self):
        return f"{self.farm.name} - {self.activity_type} on {self.date_time}"


class SensorType(Enum):
    WATER_LEVEL = 'Water Level'
    PH = 'pH'
    TEMPERATURE = 'Temperature'
    TURBIDITY = 'Turbidity'
    CONDUCTIVITY = 'Conductivity'
    DISSOLVED_OXYGEN = 'Dissolved Oxygen'
    NITRATE = 'Nitrate'
    OTHER = 'Other'


class Measurement(models.Model):
    date_time = models.DateTimeField()
    detected_number = models.IntegerField()
    sensor_type = models.CharField(
        max_length=20,
        choices=[(sensor_type.value, sensor_type.name) for sensor_type in SensorType],
        default=SensorType.WATER_LEVEL.value
    )

    def __str__(self):
        return f"{self.get_sensor_type_display()} Measurement at {self.date_time}: " \
               f"{self.detected_number}"
