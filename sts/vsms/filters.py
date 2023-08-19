import django_filters
from .models import vehicle,status

class VehicleFilter(django_filters.FilterSet):

    class Meta:
        model = vehicle
        fields = {
            'name':['icontains'],
        'model':['icontains']
        }
