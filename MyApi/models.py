from django.db import models
from django.utils import timezone
from datetime import timedelta


class Person(models.Model):
    Name = models.CharField(max_length=20, null=True)
    Address = models.CharField(max_length=200, null=True)
    Phonenumber = models.IntegerField(null=True , blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    # tabletype=models.CharField(max_length=100, null=True, blank=True)
    tabletype=models.ForeignKey('Table',null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.email
    


class Table(models.Model):

    table_type= models.CharField(max_length=100, null=True)
    persondetail=models.ForeignKey(Person,null=True, on_delete=models.SET_NULL)
    rate=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    price=models.DecimalField(max_digits=7,decimal_places=2,null=True , blank=True) 
    start_time = models.DateTimeField(null=True, blank=True)
    is_running = models.BooleanField(default=False)
    # time=models.DecimalField(max_digits=7,decimal_places=2,null=True , blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    frame=models.IntegerField(null=True , blank=True)
    frame_time_limit=models.TimeField(null=True, blank=True)
    ac=models.BooleanField(default=False)
    button=models.BooleanField(default=False)
    inactive=models.BooleanField(default=False)

    def __str__(self):
        return str(self.table_type)

    
