from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=60) #list aliases?
    min_points = models.CharField(max_length=10)
    live_points = models.CharField(max_length=10)
    last_updated = models.DateField(auto_now=True)
    #age = models.CharField(max_length=10)
    #license_country = models.CharField(max_length=30)
    #years_racing = models.CharField(max_length=10)
    #about = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    indexes = [
           models.Index(fields=['name',]),
           models.Index(fields=['live_points',]),
    ]

class RacingSeries(models.Model):
    year = models.IntegerField()
    series_name = models.CharField(max_length = 40)
    points = models.IntegerField()
    finish = models.IntegerField()
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE)