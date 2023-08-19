from django.contrib import admin
from vsms.models import Unit, Brand, status, vehicle,Type

# Register your models here.
admin.site.register(Unit)
admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(status)
admin.site.register(vehicle)
