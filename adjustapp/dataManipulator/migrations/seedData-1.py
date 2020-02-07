from django.db import migrations
import csv
import datetime
from dataManipulator.models import PerformanceMetricItem

def seedInitialData(apps, schema_editor):
    with open('dataManipulator/seedData/initialSeedData.csv', 'r') as csvData:
        reader = csv.reader(csvData)
        for row in list(reader)[1:]:
            newMetricItem, created = PerformanceMetricItem.objects.get_or_create(
                date=row[0],
                channel=row[1],
                country=row[2],
                os=row[3],
                impressions=row[4],
                clicks=row[5],
                installs=row[6],
                spend=row[7],
                revenue=row[8],
            )

    print('--- SEEDING COMPLETE ---')

class Migration(migrations.Migration):

    dependencies = [
        ('dataManipulator', '0001_initial'),
        ('dataManipulator', '0002_auto_20200205_1329'),
    ]

    operations = [
        migrations.RunPython(seedInitialData),
    ]
