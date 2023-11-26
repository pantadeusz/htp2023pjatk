from django.db import models

# Create your models here.


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

