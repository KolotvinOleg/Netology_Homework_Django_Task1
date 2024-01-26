from django.conf import settings
import csv

with open(settings.BUS_STATION_CSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)