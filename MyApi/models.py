from django.db import models
from django.utils import timezone
from datetime import timedelta


class Person(models.Model):
    Name = models.CharField(max_length=20, null=True)
    Address = models.CharField(max_length=200, null=True)
    Phonenumber = models.IntegerField(null=True , blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    def __str__(self):
        return self.email



class Table(models.Model):
    TYPE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )
    table_type= models.CharField(max_length=200, null=True, choices=TYPE_CHOICES)
    person=models.ForeignKey(Person,null=True, on_delete=models.SET_NULL)
    price=models.CharField(max_length=10, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_running = models.BooleanField(default=False)
    time=models.DecimalField(max_digits=7,decimal_places=2,null=True , blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.table_type)

    
