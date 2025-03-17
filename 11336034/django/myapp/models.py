from django.db import models

class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    kpi_name = models.CharField(max_length=100)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.name
 