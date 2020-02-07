from django.db import models
from decimal import *

class PerformanceMetricItem(models.Model):
    date = models.DateField()
    channel = models.TextField()
    country = models.CharField(max_length=2)
    os = models.TextField()
    impressions = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    installs = models.PositiveIntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()

    def __unicode__(self):
        return u"%s" % self.name

    def getCPI(self):
        return round(Decimal(self.spend / self.installs), 2)
