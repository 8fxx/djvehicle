from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
class Unit(models.Model):
    unit_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.unit_name
    def get_absolute_url(self):
        return reverse('Index')

class Brand(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.brand_name
    def get_absolute_url(self):
        return reverse('Index')

class Type(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.brand_name
    def get_absolute_url(self):
        return reverse('Index')

class vehicle(models.Model):
    VEHICLETYPES = [
    ('Vehicle', 'Vehicle'),
    ('Vessel', 'Vessel'),
    ('Motorcycle','Motorcycle')
    ]
    createdby = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    createddate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='vphotos/', blank=True)
    transmission = models.CharField(max_length=100, choices=[('Automatic','Automatic'),('Manual','Manual')])
    inventorynumber = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    enginetype = models.CharField(max_length=100)
    enginenumber = models.CharField(max_length=100)
    enginecc = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    dateofimport = models.DateField(null=True)
    fuelcapacity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    tonage = models.IntegerField(null=True)
    lastlocation = models.CharField(max_length=100, blank=True, null=True)
    laststatus = models.CharField(max_length=100, blank=True)
    servicedate = models.DateField(null=True)
    issuedtounit = models.ForeignKey(Unit,related_name='vehicleunit',on_delete=models.CASCADE, null=True)
    def approve_allotment(self):
        return self.allotment.filter(allotmentapproved = True)
    def approve_status(self):
        return self.status.filter(statusapproved = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})

class status(models.Model):
    STATUSCHOICES = [
    ('Running', 'Running'),
    ('Grounded', 'Grounded'),]

    STATUSTYPES = [
    ('Allotment', 'Allotment'),
    ('Maintenance', 'Maintenance'),]

    vehicle = models.ForeignKey(vehicle,related_name='status',on_delete=models.CASCADE, null=True)
    update = models.CharField(max_length=100,choices=STATUSCHOICES, default='Running')
    type = models.CharField(max_length=100,choices=STATUSTYPES, default='Running')
    remarks = models.TextField(max_length=255,null=True)
    createddate = models.DateTimeField(default=timezone.now)
    createdby = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    statusapproved = models.BooleanField(default=False)
    allotmentunit = models.ForeignKey(Unit,related_name='statusunit',on_delete=models.CASCADE, null=True)
    allotmentlocation = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.update
    def get_absolute_url(self):
        return reverse('Index')
    def approvestatus(self):
        self.statusapproved = True
        self.save()
    
#  f'{self.update} {self.allotmentlocation} {self.allotmentunit}'