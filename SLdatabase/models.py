from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=60) #list aliases?
    series = models.CharField (max_length=3000)
    min_points = models.CharField(max_length=10)
    live_points = models.CharField(max_length=10)
    last_updated = models.DateField(auto_now=True)
    def __str__(self):
        return self.name
    indexes = [
           models.Index(fields=['name',]),
           models.Index(fields=['live_points',]),
    ]
